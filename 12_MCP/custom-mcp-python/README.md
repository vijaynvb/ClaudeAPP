# MCP Project (Python)

This is a Python + FastAPI equivalent of the `custom-mcp-node` server, using the official [`mcp`](https://pypi.org/project/mcp/) Python SDK to expose the same tools and resource over the Model Context Protocol.

## Features

- **FastAPI-based HTTP server** exposing an MCP endpoint at `/mcp`
- **MCP tools**: `add`, `get-energy-prices`, `get-todos`
- **MCP resource**: `greeting://{name}`

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

```sh
cd custom-mcp-python
pip install -r requirements.txt
```

### Start the server

```sh
python server.py
```

The server will run at [http://localhost:3000](http://localhost:3000), with the MCP endpoint at `http://localhost:3000/mcp`.

## Using the Model Context Protocol SDK

This project uses [`mcp.server.MCPServer`](https://pypi.org/project/mcp/) to implement an MCP server. Tools are plain typed Python functions decorated with `@server.tool()` — the SDK infers the JSON Schema from the function's type hints, so there's no schema to write by hand.

### Key Concepts

- **`MCPServer`**: main class to register tools and resources.
- **`MCPServer.streamable_http_app()`**: returns a Starlette ASGI app implementing the MCP Streamable HTTP transport (session management included), which we mount into FastAPI.
- **Tools**: functions exposed to MCP clients (`add`, `get-energy-prices`, `get-todos`).
- **Resources**: data endpoints addressed by URI template (`greeting://{name}`).

## Code Overview

The whole server is in [`server.py`](server.py):

**1.** Create an `MCPServer` instance.

**2.** Register tools with `@mcp_server.tool()`:

```python
@mcp_server.tool(name="add")
def add(a: float, b: float) -> str:
    return str(a + b)
```

**3.** Register a resource template with `@mcp_server.resource()`:

```python
@mcp_server.resource("greeting://{name}")
def greeting(name: str) -> str:
    return f"Hello, {name}!"
```

**4.** Mount the MCP app into FastAPI and run it with `uvicorn`.

## Extending the Server

Add more tools or resources by decorating additional functions with `@mcp_server.tool()` or `@mcp_server.resource()`. See the [`mcp` package documentation](https://pypi.org/project/mcp/) for more details.

## Using the MCP Server in VS Code

Same as the Node version — register it in `.vscode/mcp.json`:

```jsonc
{
    "servers": {
        "my-mcp-http-server": {
            "url": "http://localhost:3000/mcp"
        }
    }
}
```
