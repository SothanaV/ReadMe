# Running Async Functions Synchronously in FastAPI / FastMCP / OpenWebUI Pipelines

When an async coroutine must be called from a synchronous context (e.g. inside an OpenWebUI Pipeline `__init__`) and an event loop is already running, `asyncio.run()` will raise a `RuntimeError`. The pattern below creates a dedicated background event loop on a separate thread so the coroutine can be awaited safely.

## Table of Contents

- [Background Loop Helper](#background-loop-helper)
- [Usage Example: MCP Tool Conversion in a Pipeline](#usage-example-mcp-tool-conversion-in-a-pipeline)

---

## Background Loop Helper

```python
import threading
import asyncio

_loop = None
_loop_thread = None


def _start_background_loop():
    global _loop, _loop_thread
    if _loop is not None:
        return

    _loop = asyncio.new_event_loop()

    def run_loop():
        asyncio.set_event_loop(_loop)
        _loop.run_forever()

    _loop_thread = threading.Thread(target=run_loop, daemon=True)
    _loop_thread.start()


def run_coro_sync(coro):
    """
    Run an async coroutine in a dedicated background loop
    and block the current (sync) thread until it completes.
    """
    _start_background_loop()
    future = asyncio.run_coroutine_threadsafe(coro, _loop)
    return future.result()
```

---

## Usage Example: MCP Tool Conversion in a Pipeline

```python
async def convert_mcp_tools(client):
    tools = []
    async with client:
        for t in await client.list_tools():
            # Extract tool argument schema
            inputs = {k: v for k, v in t.inputSchema["properties"].items()}

            class _Tool:
                def __init__(self, name):
                    self.name = name

                async def _call_tool(self, kwargs):
                    print(f"call tool => {self.name} \t {kwargs}")
                    async with client:
                        res = await client.call_tool(name=self.name, arguments=kwargs)
                        return res.content[0].text

                def run_tool(self, **kwargs):
                    return asyncio.run(self._call_tool(kwargs))

            _t = _Tool(t.name)
            tools.append(
                tools.Tool(
                    name=t.name,
                    desc=t.description,
                    args=inputs,
                    func=_t.run_tool,
                )
            )
    return tools


class Pipeline:
    # ...
    def __init__(self):
        self.name = "RCA Analyzer"
        # ...
        self.client = Client("http://<mcp_server>/mcp")
        self.tools = run_coro_sync(convert_mcp_tools(self.client))
        print(self.tools)
        # ...
```
