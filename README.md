<div align="center">

# 🏦 MCP Server for Aave V3 v0.1

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)](https://nodejs.org)
[![Arbitrum Network](https://img.shields.io/badge/Network-Arbitrum%20One-28a0f0)](https://arbitrum.io)
[![Aave V3](https://img.shields.io/badge/Aave-V3-purple)](https://aave.com)
[![MCP Protocol](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)
[![1inch Integration](https://img.shields.io/badge/1inch-Integrated-red)](https://1inch.io)

**Production-ready Model Context Protocol (MCP) server for Aave V3 DeFi operations on Arbitrum One network**

[PM2 运维指引](#-pm2-运维指引) • [Features](#-features) • [Quick Start](#-quick-start) • [API](#-api-endpoints) • [Tools](#-available-tools) • [Examples](#-examples) • [Prompts](#-prompts) • [Security](#-security)

</div>

---

## 🔧 PM2 运维指引

1. **启动**
   ```bash
   npm run build
   pm2 start ecosystem.config.js --only aave-mcp
   ```
2. **停止 / 删除**
   ```bash
   pm2 stop aave-mcp
   pm2 delete aave-mcp
   ```
3. **日志 / 监控**
   ```bash
   pm2 logs aave-mcp
   pm2 monit aave-mcp
   ```

> 默认端口为 `8080`，可通过 `.env` 中的 `PORT` 覆盖；若需系统重启后自启可执行 `pm2 save && pm2 startup`。

---

## 🚀 Features

### 🎯 **Complete DeFi Protocol Integration**
- Full Aave V3 lending protocol support on Arbitrum One network
- Smart contract interactions with automatic gas optimization
- Real-time APY tracking and yield analytics
- Health factor monitoring and liquidation alerts
- Transaction simulation before execution

### 🧠 **Intelligent Token Management**
- Support for 16+ tokens including stablecoins, LSTs, and wrapped assets
- Automatic token detection and balance management
- Smart routing through 1inch DEX aggregator
- Fallback to Uniswap V3 with multi-tier fee optimization
- Slippage protection and MEV resistance

### 🤖 **MCP Protocol Implementation**
- 22 specialized tools for DeFi automation
- Compatible with AI assistants and automation frameworks
- HTTP/SSE and stdio transport support
- Real-time transaction execution with automatic signing
- Comprehensive error handling and retry logic

### 🏛️ **Enterprise-Ready Architecture**
- Built with NestJS for scalability and maintainability
- TypeScript for type safety and developer experience
- Modular service architecture for easy extension
- Comprehensive logging and monitoring
- PM2 process manager support for production operations

---

## 📦 Quick Start

### ✅ Prerequisites
```bash
# Required
Node.js >= 18.0.0
npm or pnpm package manager

# Optional
Private key for transaction execution
```

### 📥 Installation

```bash
# Clone the repository
git clone https://github.com/Tairon-ai/aave-mcp.git
cd aave-mcp

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Start the server
npm run start

# Development mode with hot reload
npm run start:dev

# 服务默认监听 8080 端口，可通过环境变量 PORT 覆盖
```

### 🧩 Python MCP 代理

- `external_mcp_py/server.py`：把 Nest MCP Web 服务封装成标准 MCP 服务器，可通过 `--mode http`（默认端口 9000）或 `--mode stdio` 暴露；
- `external_mcp_py/client.py`：一个简易 MCP 客户端，既可以直接 HTTP 调用，也可以拉起 stdio 模式用于调试；
- 详细用法与 Chatwise 配置示例见 [external_mcp_py/README.md](external_mcp_py/README.md)。

## 🛠 Available Tools

### 🏦 **Aave Protocol Operations**

| Tool | Description | Parameters |
|------|-------------|------------|
| `aave_stake` | Supply tokens to earn yield | `asset`, `amount`, `userAddress` |
| `aave_withdraw` | Withdraw supplied tokens | `asset`, `amount`, `userAddress` |
| `aave_borrow` | Borrow against collateral | `asset`, `amount`, `interestRateMode`, `userAddress` |
| `aave_repay` | Repay borrowed tokens | `asset`, `amount`, `interestRateMode`, `userAddress` |
| `aave_get_reserves` | Get all available reserves | - |
| `aave_get_user_positions` | Get user's positions | `userAddress` |
| `aave_get_user_account` | Get account data | `userAddress` |

### 💱 **Token Swapping**

| Tool | Description | Parameters |
|------|-------------|------------|
| `swap_quote` | Get swap quote via Uniswap | `tokenIn`, `tokenOut`, `amountIn` |
| `swap_execute` | Execute token swap | `tokenIn`, `tokenOut`, `amountIn`, `userAddress` |
| `oneinch_quote` | Get 1inch aggregated quote | `src`, `dst`, `amount` |
| `oneinch_swap` | Execute 1inch swap | `src`, `dst`, `amount`, `from` |

### 🧠 **Smart Operations**

| Tool | Description | Parameters |
|------|-------------|------------|
| `smart_stake` | Auto-swap and stake | `inputToken`, `targetToken`, `amount`, `userAddress` |
| `smart_deposit_auto` | Intelligent deposit | `inputToken`, `amount`, `userAddress` |
| `smart_stake_auto_fund` | Stake with auto-funding | `targetToken`, `amount`, `userAddress` |

### ⛓️ **Blockchain Utilities**

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_balance` | Get token balance | `token`, `address` |
| `get_all_balances` | Get all balances | `address` |
| `get_gas_price` | Get current gas price | - |
| `simulate_transaction` | Simulate transaction | `transaction` |
| `broadcast_transaction` | Broadcast signed tx | `signedTransaction` |

---

## 🔗 API Endpoints

### 🌐 Core Endpoints

```bash
GET  /           # Server status and info
GET  /health     # Health check
GET  /mcp        # MCP server information
POST /mcp        # MCP protocol endpoint
GET  /mcp/tools  # List available tools
GET  /mcp/health # MCP health status
```

### 📡 WebSocket/SSE Support

```bash
GET /mcp/sse     # Server-Sent Events for real-time updates
```

---

## 💡 Examples

### 💰 Supply Tokens to Aave

```javascript
// Supply 100 USDC to Aave
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "aave_stake",
    "arguments": {
      "asset": "USDC",
      "amount": "100",
      "userAddress": "0x..."
    }
  },
  "id": 1
}
```

### 🎯 Smart Stake with Auto-Funding

```javascript
// Automatically swap ETH to USDC and stake
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "smart_stake_auto_fund",
    "arguments": {
      "targetToken": "USDC",
      "amount": "1000",
      "userAddress": "0x...",
      "slippageTolerance": 0.5
    }
  },
  "id": 1
}
```

### 📊 Get Best Swap Quote

```javascript
// Get quote for swapping 1 ETH to USDC
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "oneinch_quote",
    "arguments": {
      "src": "ETH",
      "dst": "USDC",
      "amount": "1"
    }
  },
  "id": 1
}
```

---

## 🤖 Prompts

### 💬 Example Prompts for Claude, ChatGPT, or Other AI Assistants

These prompts demonstrate how to interact with the MCP server through natural language when integrated with AI assistants:

#### 💼 **DeFi Portfolio Management**

```
"Check my DeFi portfolio balance at address 0x... and show me all token holdings"

"What's my current health factor on Aave? I have positions at 0x..."

"Calculate the best yield strategy for 10,000 USDC - should I supply to Aave or keep it liquid?"

"Show me my borrowing capacity if I deposit 5 ETH as collateral"
```

#### 🏦 **Lending & Borrowing Operations**

```
"I want to supply 1000 USDC to Aave to earn yield. My address is 0x..."

"Help me borrow 500 DAI against my supplied ETH collateral at 0x..."

"What's the current APY for supplying WETH on Aave?"

"I need to repay my USDC loan on Aave. Show me my current debt and repay it all"

"Withdraw half of my supplied wstETH from Aave lending pool"
```

#### 🔄 **Token Swapping & Optimization**

```
"Find the best route to swap 2 ETH to USDC using either Uniswap or 1inch"

"I have 5000 DAI and want to convert it to USDT with minimal slippage"

"Compare rates between Uniswap and 1inch for swapping 10 WETH to USDC"

"Execute a swap of 0.5 ETH to GHO token with maximum 1% slippage"
```

#### 🚀 **Smart Staking Strategies**

```
"I want to stake USDC but only have ETH. Can you swap and stake 1000 USDC worth automatically?"

"Help me stake 2000 USDT using the smart staking feature - find the best yield"

"Auto-fund and stake 500 DAI from my available balance, swapping if needed"

"What's the optimal staking strategy for 10 ETH to maximize yield?"
```

#### 🚮 **Risk Management & Analytics**

```
"Alert me if my health factor drops below 1.5 on Aave"

"Calculate liquidation price if I borrow 2000 USDC against 1 ETH collateral"

"Show me a risk analysis for borrowing 50% of my collateral value"

"What's my net APY considering both supply and borrow positions?"
```

#### 📤 **Transaction Management**

```
"Simulate a transaction to supply 1000 USDC before executing it"

"Check current gas prices on Arbitrum and estimate transaction costs"

"Prepare a batch transaction to: 1) Swap ETH to USDC, 2) Supply USDC to Aave"

"Show me my last 10 transactions on Aave protocol"
```

#### 🎯 **Complex DeFi Strategies**

```
"Help me execute a leveraged yield farming strategy with 5000 USDC"

"I want to loop my ETH position - borrow USDC, swap to ETH, and resupply 3 times"

"Create a delta-neutral position by supplying ETH and borrowing equivalent USDC"

"Optimize my portfolio for maximum yield while maintaining health factor above 2"
```

#### 📈 **Market Analysis**

```
"Compare current lending rates across all supported stablecoins"

"Which asset has the highest supply APY on Aave right now?"

"Show me utilization rates for all borrowable assets"

"What's the total value locked in Aave on Arbitrum?"
```

### 🔧 Integration Tips for AI Assistants

When using these prompts with the MCP server:

1. **Always specify the user address** when performing wallet-specific operations
2. **Set appropriate slippage tolerance** (typically 0.5-2%) for swaps
3. **Use simulation mode first** for testing complex transactions
4. **Monitor gas prices** before executing large transactions
5. **Check health factor** before and after borrowing operations

### 🗺️ Natural Language to Tool Mapping

| User Intent | MCP Tool to Use |
|------------|-----------------|
| "Check my balance" | `get_all_balances` |
| "Supply/Stake tokens" | `aave_stake` or `smart_stake` |
| "Withdraw tokens" | `aave_withdraw` |
| "Borrow tokens" | `aave_borrow` |
| "Repay loan" | `aave_repay` |
| "Swap tokens" | `swap_execute` or `oneinch_swap` |
| "Get swap quote" | `swap_quote` or `oneinch_quote` |
| "Check positions" | `aave_get_user_positions` |
| "View APY rates" | `aave_get_reserves` |
| "Auto-fund and stake" | `smart_stake_auto_fund` |

---

## 🧪 Testing

### 🧪 Manual Testing

```bash
# Test server connectivity
curl http://localhost:8080/health

# Get MCP server info
curl http://localhost:8080/mcp

# List all available tools
curl http://localhost:8080/mcp/tools
```

### 🔍 API Testing with cURL

```bash
# Check token balance
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_balance",
      "arguments": {
        "token": "USDC",
        "address": "0x..."
      }
    },
    "id": 1
  }'
```

---

## 🔒 Security

### 🔐 Best Practices

- **Private Key Management**: Never commit private keys. Use environment variables or secure key management systems
- **Transaction Simulation**: Always test transactions in simulation mode first (`AUTO_EXECUTE=false`)
- **Slippage Protection**: Set appropriate slippage limits (typically 0.5-2%)
- **Gas Management**: Monitor gas prices and set reasonable limits
- **Access Control**: Implement proper authentication for production deployments
- **Monitoring**: Use Arbiscan and monitoring tools to track transactions

### 🛡️ Security Features

- Automatic gas estimation with configurable buffer
- Transaction simulation before execution
- Slippage protection on all swaps
- MEV protection through private mempools (when configured)
- Rate limiting and request validation
- Comprehensive error handling and logging

---

## 📊 Supported Networks & Tokens

### 🌐 Network
- **Arbitrum One** (Chain ID: 42161)
- RPC: `https://arb1.arbitrum.io/rpc`

### 🪙 Supported Tokens

**Stablecoins**
- USDC, USDCe, USDT, DAI, GHO, EURS

**ETH & Liquid Staking Tokens**
- WETH, wstETH, weETH, ezETH, rETH, rsETH

**Ecosystem & Yield**
- ARB, LINK

**Bitcoin & Synths**
- WBTC, tBTC

**Governance**
- AAVE

### 📜 Key Contracts
- Aave V3 Pool: `0x794a61358D6845594F94dc1DB02A252b5b4814aD`
- Aave Protocol Data Provider: `0x243Aa95cAC2a25651eda86e80bEe66114413c43b`
- Uniswap V3 Router: `0x68b3465833Fb72A70ecDF485E0e4C7bD8665Fc45`
- Uniswap V3 Quoter: `0x61Ffe014bA17989E743c5F6cB21bF9697530B21e`

---

## 🚀 Deployment

### 🏭 Production Deployment

```bash
# Build for production
npm run build

# Start production server
npm run start:prod

# With PM2 (recommended for ops)
# build once
npm run build
pm2 start ecosystem.config.js --only aave-mcp
pm2 logs aave-mcp      # stream logs
pm2 restart aave-mcp   # apply new build
pm2 save && pm2 startup # persist across reboots
```

### 🛡 PM2 Process Management

- Default HTTP port: **8080** (set via `PORT` env)
- Ensure `.env` contains Arbitrum RPC/private key before launching
- Use `pm2 monit aave-mcp` for live metrics and `pm2 delete aave-mcp` to remove the process when decommissioning

### 🔑 Environment Variables

```env
# Required
PORT=8080
RPC_URL=https://arb1.arbitrum.io/rpc
CHAIN_ID=42161
PRIVATE_KEY=your_private_key_without_0x

# Optional
LOG_LEVEL=info
AUTO_EXECUTE=true
ONE_INCH_API_KEY=your_api_key
TEST_WALLET_ADDRESS=0x...
```

---

## 📈 Performance

- **Response Time**: <100ms for read operations
- **Transaction Speed**: ~2s on Arbitrum One
- **Throughput**: 1000+ requests per second
- **Uptime**: 99.9% availability target
- **Gas Optimization**: Automatic batching and optimization

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

```bash
# Fork and clone
git fork https://github.com/Tairon-ai/aave-mcp
git clone https://github.com/Tairon-ai/aave-mcp

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and test
npm run test
npm run lint

# Commit and push
git commit -m 'Add amazing feature'
git push origin feature/amazing-feature

# Open Pull Request
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Aave Protocol](https://aave.com) - Leading DeFi lending protocol
- [Arbitrum One](https://arbitrum.io) - Ethereum L2 scaling solution
- [1inch Network](https://1inch.io) - DEX aggregation protocol
- [Uniswap](https://uniswap.org) - Decentralized exchange protocol
- [Model Context Protocol](https://modelcontextprotocol.io) - AI integration standard
- [NestJS](https://nestjs.com) - Progressive Node.js framework

---

<div align="center">

**Built by [Tairon.ai](https://tairon.ai) team, with help from Claude**

</div>
