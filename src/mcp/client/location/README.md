# Simple Location MCP Client

This is a simple MCP client that communicates with any MCP server using standard input/output (stdio).

## How to Run

To start the client, use the following command:

```bash
uv run main.py <path-to-server.py>
```

Replace `<path-to-server.py>` with the path to your MCP server script.

## Requirements

- This client connects to Python-based MCP servers via stdio.
- Ensure all required dependencies are installed in the client's virtual environment using:

```bash
uv add <dependency-name>
```

Install any additional dependencies your server or client may require before running.