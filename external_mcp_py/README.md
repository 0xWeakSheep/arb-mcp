## external_mcp_py

Python 版 MCP 代理与测试客户端：

- `server.py`：把本地 Nest MCP Web 服务（默认 `http://localhost:8080/mcp`）包装成通用 MCP 服务器，只负责转发 JSON-RPC 请求，不会新增工具；
- `client.py`：极简 MCP 客户端，支持 HTTP 或 stdio，两三条 JSON-RPC 命令即可验证代理是否可用。

### 启动代理（HTTP 模式）

```bash
cd external_mcp_py
python server.py --mode http --port 9000 --backend http://localhost:8080
```

此时 MCP 接口为 `http://localhost:9000/mcp`，健康检查会直接透传 Nest 的 `/mcp/health`。

### 启动代理（stdio 模式）

```bash
python server.py --mode stdio --backend http://localhost:8080
```

### 使用测试客户端

HTTP 模式示例：

```bash
python client.py --mode http --url http://localhost:9000/mcp --tool get_gas_price
```

stdio 模式示例：

```bash
python client.py --mode stdio --tool aave_stake --arguments '{"asset":"USDC","amount":"10","userAddress":"0x..."}'
```

### Chatwise JSON 配置示例

若代理监听 9000 端口，可在 Chatwise 里写：

```json
{
  "mcpServers": {
    "lp_proxy": {
      "transport": "http",
      "url": "http://localhost:9000/mcp",
      "env": {
        "CHATWISE_PROJECT": "lp_proxy_python"
      }
    }
  }
}
```
