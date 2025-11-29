export default () => ({
  port: parseInt(process.env.PORT || "8080", 10),
  blockchain: {
    rpcUrl: process.env.RPC_URL || "https://arb1.arbitrum.io/rpc",
    chainId: parseInt(process.env.CHAIN_ID || "42161", 10), // Arbitrum One
    privateKey: process.env.PRIVATE_KEY || "",
    // autoExecute: process.env.AUTO_EXECUTE === "true",
    autoExecute: true,
  },
  contracts: {
    aavePool: "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
    poolDataProvider: "0x243Aa95cAC2a25651eda86e80bEe66114413c43b",
    uniswapRouter: "0x68b3465833Fb72A70ecDF485E0e4C7bD8665Fc45",
    uniswapQuoter: "0x61Ffe014bA17989E743c5F6cB21bF9697530B21e",
  },
  tokens: {
    // Stablecoins
    USDC: "0xaf88d065e77c8cC2239327C5EDb3A432268e5831", // Native USDC
    USDCe: "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8", // Bridged USDC (USDC.e)
    USDT: "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
    DAI: "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
    GHO: "0x7dfF72693f6A4149b17e7C6314655f6A9F7c8B33",
    EURS: "0xD22a58f79e9481D1a88e00c343885A588b34b68B",

    // ETH and LSTs (Liquid Staking Tokens)
    WETH: "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    wstETH: "0x5979D7b546E38E414F7E9822514be443A4800529",
    weETH: "0x35751007a407ca6fEFFE80b3cB397736D2cf4dbe",
    ezETH: "0x2416092f143378750bb29b79eD961ab195CcEea5",
    rETH: "0xEC70Dcb4A1EFa46b8F2D97C310C9c4790ba5ffA8",
    rsETH: "0x4186BFC76E2E237523CBC30FD220FE055156b41F",

    // Additional majors
    ARB: "0x912CE59144191C1204E64559FE8253a0e49E6548",
    WBTC: "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
    tBTC: "0x6c84a8f1c29108F47a79964b5Fe888D4f4D0dE40",

    // Governance tokens
    AAVE: "0xba5DdD1f9d7F570dc94a51479a000E3BCE967196",
    LINK: "0xf97f4df75117a78c1A5a0DBb814Af92458539FB4",
  },
  uniswap: {
    feeTiers: [100, 500, 3000, 10000], // 0.01%, 0.05%, 0.3%, 1%
    maxSlippage: 1, // 1%
  },
  logging: {
    level: process.env.LOG_LEVEL || "info",
  },
});
