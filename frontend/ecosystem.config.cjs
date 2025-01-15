const fs = require("fs");
const path = require("path");

// Extract version from the current symlink
const currentPath = "/var/www/asklyla.com/current";
const version = path.basename(fs.readlinkSync(currentPath));

module.exports = {
  apps: [
    {
      name: "asklyla.com", // Keep a standard process name
      script: "./.output/server/index.mjs",
      cwd: "/var/www/asklyla.com/current",
      env: {
        NODE_ENV: "production",
        SOCKET_PATH: "/var/www/asklyla.com/current/asklyla.com.sock",
        VERSION: version, // Pass version as an environment variable
      },
    },
  ],
};
