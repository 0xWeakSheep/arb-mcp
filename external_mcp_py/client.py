"""Simple MCP client for testing the Python proxy server."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from typing import Any, Dict, List, Optional
from urllib import request


def _json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


def _build_requests(tool: str, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {
            "jsonrpc": "2.0",
            "id": "init-1",
            "method": "initialize",
            "params": {
                "clientInfo": {"name": "external-mcp-py-client", "version": "0.1.0"},
                "capabilities": {"tools": {}},
            },
        },
        {"jsonrpc": "2.0", "id": "tools-1", "method": "tools/list"},
        {
            "jsonrpc": "2.0",
            "id": "call-1",
            "method": "tools/call",
            "params": {"name": tool, "arguments": arguments},
        },
    ]


def _http_request(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})
    with request.urlopen(req) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def _run_http(url: str, requests_: List[Dict[str, Any]]) -> None:
    for payload in requests_:
        response = _http_request(url, payload)
        print(f"\n>>> {payload['method']}")
        print(_json(response))


def _run_stdio(command: str, requests_: List[Dict[str, Any]]) -> None:
    proc = subprocess.Popen(
        shlex.split(command),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    assert proc.stdin and proc.stdout
    try:
        for payload in requests_:
            line = json.dumps(payload)
            proc.stdin.write(line + "\n")
            proc.stdin.flush()
            response = proc.stdout.readline()
            print(f"\n>>> {payload['method']}")
            print(response.strip())
    finally:
        proc.stdin.close()
        proc.terminate()
        proc.wait(timeout=2)


def _parse_arguments(data: Optional[str]) -> Dict[str, Any]:
    if not data:
        return {}
    return json.loads(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Test MCP proxy client")
    parser.add_argument("--mode", choices=["http", "stdio"], default="http")
    parser.add_argument("--url", default="http://localhost:9000/mcp", help="HTTP MCP endpoint")
    parser.add_argument(
        "--stdio-command",
        default=f"{shlex.quote(sys.executable)} external_mcp_py/server.py --mode stdio",
        help="Command to run the proxy in stdio mode",
    )
    parser.add_argument("--tool", default="get_gas_price", help="Tool name to invoke")
    parser.add_argument("--arguments", help="JSON encoded tool arguments")
    args = parser.parse_args()

    payloads = _build_requests(args.tool, _parse_arguments(args.arguments))

    if args.mode == "http":
        _run_http(args.url, payloads)
        return

    _run_stdio(args.stdio_command, payloads)


if __name__ == "__main__":
    main()
