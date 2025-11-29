"""MCP proxy server implemented in Python.

This script exposes Model Context Protocol (MCP) endpoints over HTTP (/mcp)
or stdio and forwards all requests to a Nest MCP backend (default
http://localhost:8080/mcp)."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict
from urllib import error, request


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def _format_content(data: Any) -> str:
    if isinstance(data, (dict, list)):
        return json.dumps(data, ensure_ascii=False, indent=2)
    return str(data)


@dataclass
class ProxyConfig:
    backend_host: str
    timeout: int = 30

    def __post_init__(self) -> None:
        self.backend_host = self.backend_host.rstrip("/")

    @property
    def mcp_url(self) -> str:
        return f"{self.backend_host}/mcp"

    @property
    def health_url(self) -> str:
        return f"{self.backend_host}/mcp/health"


class MCPProxyServer:
    """Core MCP proxy logic shared between HTTP and stdio transports."""

    def __init__(self, config: ProxyConfig) -> None:
        self.config = config

    # ------------------------------------------------------------------ #
    # JSON-RPC handlers
    # ------------------------------------------------------------------ #

    def handle_jsonrpc(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            return self._forward_jsonrpc(payload)
        except RuntimeError as exc:
            request_id = payload.get("id")
            return self._error(request_id, -32000, "Backend request failed", str(exc))

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _wrap(self, request_id: Any, result: Any) -> Dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    def _error(self, request_id: Any, code: int, message: str, data: Any = None) -> Dict[str, Any]:
        err: Dict[str, Any] = {"code": code, "message": message}
        if data is not None:
            err["data"] = data
        return {"jsonrpc": "2.0", "id": request_id, "error": err}

    def _forward_jsonrpc(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        req = request.Request(self.config.mcp_url, data=data, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=self.config.timeout) as resp:
                raw = resp.read().decode("utf-8")
                if resp.headers.get("Content-Type", "").startswith("application/json"):
                    return json.loads(raw) if raw else {}
                return json.loads(raw) if raw else {}
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8")
            raise RuntimeError(f"{exc.code} {exc.reason}: {detail or 'no body'}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Cannot reach backend: {exc.reason}") from exc


# ---------------------------------------------------------------------- #
# HTTP server implementation
# ---------------------------------------------------------------------- #


class _MCPHTTPRequestHandler(BaseHTTPRequestHandler):
    proxy: MCPProxyServer

    def _send_json(self, status: int, payload: Dict[str, Any]) -> None:
        encoded = _json_dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/mcp/health":
            try:
                req = request.Request(self.proxy.config.health_url, headers={"Accept": "application/json"})
                with request.urlopen(req, timeout=self.proxy.config.timeout) as resp:
                    body = resp.read().decode("utf-8")
                    payload = json.loads(body) if body else {}
            except Exception as exc:  # noqa: BLE001
                payload = {"status": "degraded", "error": str(exc)}
                self._send_json(502, payload)
                return
            self._send_json(200, payload)
            return
        self.send_error(404, "Not Found")

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/mcp":
            self.send_error(404, "Not Found")
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            self.send_error(400, "Invalid Content-Length")
            return
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON payload"})
            return

        response = self.proxy.handle_jsonrpc(payload)
        self._send_json(200, response)

    def log_message(self, fmt: str, *args: Any) -> None:  # noqa: A003
        # Suppress default logging; uncomment for debugging
        return


class MCPHTTPServer(HTTPServer):
    def __init__(self, host: str, port: int, proxy: MCPProxyServer) -> None:
        handler = _MCPHTTPRequestHandler
        handler.proxy = proxy
        super().__init__((host, port), handler)


# ---------------------------------------------------------------------- #
# stdio mode
# ---------------------------------------------------------------------- #


def run_stdio(proxy: MCPProxyServer) -> None:
    """Expose MCP over stdin/stdout."""
    for line in sys.stdin:
        data = line.strip()
        if not data:
            continue
        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            response = proxy._error(None, -32700, "Parse error")
        else:
            response = proxy.handle_jsonrpc(payload)
        sys.stdout.write(_json_dumps(response) + "\n")
        sys.stdout.flush()


# ---------------------------------------------------------------------- #
# CLI entrypoint
# ---------------------------------------------------------------------- #


def main() -> None:
    parser = argparse.ArgumentParser(description="External MCP proxy server")
    parser.add_argument("--backend", default="http://localhost:8080", help="Nest MCP backend base URL (without /mcp)")
    parser.add_argument("--mode", choices=["http", "stdio"], default="http", help="Transport to expose")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host for HTTP mode")
    parser.add_argument("--port", type=int, default=9000, help="Bind port for HTTP mode")
    parser.add_argument("--timeout", type=int, default=30, help="Backend request timeout seconds")
    args = parser.parse_args()

    proxy = MCPProxyServer(ProxyConfig(backend_host=args.backend, timeout=args.timeout))

    if args.mode == "stdio":
        run_stdio(proxy)
        return

    server = MCPHTTPServer(args.host, args.port, proxy)
    print(f"[MCP proxy] HTTP mode listening on http://{args.host}:{args.port}/mcp (backend={proxy.config.backend_host})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[MCP proxy] shutting down...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
