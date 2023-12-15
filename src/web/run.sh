echo "const server_vars = {address: \"$API_HOST\", port: \"$API_PORT\"}; module.exports = {server_vars};" > variables.js

npm run dev
