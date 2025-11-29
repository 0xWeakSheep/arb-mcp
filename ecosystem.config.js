module.exports = {
  apps: [
    {
      name: "aave-mcp",
      script: "dist/main.js",
      instances: 1,
      exec_mode: "fork",
      watch: false,
      env: {
        NODE_ENV: "production",
        PORT: process.env.PORT || 8080,
      },
    },
  ],
};
