# python async function run in sync and exists loop fastapi/fastmcp/openwebui-pipeline

```py
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
    Run an async coroutine in a dedicated background loop,
    and wait for the result synchronously.
    """
    _start_background_loop()
    future = asyncio.run_coroutine_threadsafe(coro, _loop)
    return future.result()  # blocks current (sync) thread until done

async def convert_mcp_tools(client):
    tools = []
    async with client:
        for t in await client.list_tools():
            # Extract tool args
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
    ...
    def __init__(self):
        self.name = "RCA Analyzer"
        ...
        self.client = Client("http://<mcp server>/mcp")
        self.tools = run_coro_sync(convert_mcp_tools(self.client))
        print(self.tools)
        ...
```