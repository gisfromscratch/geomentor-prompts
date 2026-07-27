import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import sys
import time
from typing import Optional


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        start = time.perf_counter()
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        t1 = time.perf_counter()
        print(f"Connected stdio in {t1 - start:.3f} seconds")

        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        t2 = time.perf_counter()
        print(f"Created ClientSession in {t2 - t1:.3f} seconds")

        await self.session.initialize()
        t3 = time.perf_counter()
        print(f"Session initialized in {t3 - t2:.3f} seconds")

        # List available tools
        response = await self.session.list_tools()
        t4 = time.perf_counter()
        print(f"Listed tools in {t4 - t3:.3f} seconds")

        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
