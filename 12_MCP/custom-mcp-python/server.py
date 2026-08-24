"""Custom MCP server — Python + FastAPI equivalent of custom-mcp-node.

Exposes the same tools and resource as the TypeScript version:
  - add(a, b): adds two numbers
  - get-energy-prices: fetches tomorrow's energy prices
  - get-todos: fetches a public todo list
  - greeting://{name} resource: returns a greeting for a given name

Run with: uvicorn server:app --port 3000
"""

from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from mcp.server import MCPServer

mcp_server = MCPServer(name="Demo", version="1.0.0")


@mcp_server.tool(name="add")
def add(a: float, b: float) -> str:
    return str(a + b)


@mcp_server.tool(name="get-energy-prices")
async def get_energy_prices() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.awattar.de/v1/marketdata")
        data = response.json()
    return f"Energy prices for tomorrow: {data}"


@mcp_server.tool(name="get-todos")
async def get_todos() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos")
        data = response.json()
    return f"Todos: {data}"


@mcp_server.resource("greeting://{name}")
def greeting(name: str) -> str:
    return f"Hello, {name}!"


mcp_app = mcp_server.streamable_http_app()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # mcp_app's own lifespan starts the MCP session manager's task group.
    # FastAPI doesn't run a mounted sub-app's lifespan automatically, so we
    # enter it explicitly here to keep that startup/shutdown tied to ours.
    async with mcp_app.router.lifespan_context(mcp_app):
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/", mcp_app)

if __name__ == "__main__":
    import asyncio
    import sys

    import uvicorn

    config = uvicorn.Config(app, host="0.0.0.0", port=3000)
    server = uvicorn.Server(config)

    # On Windows, uvicorn's default event loop is a ProactorEventLoop, which
    # logs a noisy (but harmless) ConnectionResetError whenever a client
    # disconnects abruptly — which our short-lived-connection-per-request
    # client does on every call. Running under a SelectorEventLoop instead
    # avoids that; asyncio.run(loop_factory=...) is the non-deprecated way
    # to choose the loop type (the older set_event_loop_policy is removed
    # in newer Python versions).
    loop_factory = asyncio.SelectorEventLoop if sys.platform == "win32" else None

    print("MCP server running at http://localhost:3000")
    asyncio.run(server.serve(), loop_factory=loop_factory)
