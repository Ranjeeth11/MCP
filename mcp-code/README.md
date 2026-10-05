# MCP: Runnable Examples

These files go with `MCP.md` (one folder up). One small **Product Catalog** project grows step by step, from an empty server to a server with security improvements.

| Item | Version used |
|---|---|
| MCP specification | **2026-07-28** (current stable) |
| Python SDK | **`mcp` 2.3.0** (v2 line), import `from mcp.server import MCPServer` |
| Python | 3.10 or newer (tested on 3.14) |
| MCP Inspector | `@modelcontextprotocol/inspector` 2.9.0 (needs Node.js 22.19+) |

## 1. Install

```bash
cd mcp-code
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Check the install:

```bash
python -c "import importlib.metadata as m; print(m.version('mcp'))"   # 2.3.0
```

## 2. Files and run order

Run every command from inside the `mcp-code` folder.

| # | File | Concept | Run |
|---|---|---|---|
| 1 | `01_basic_server.py` | Smallest possible server | `python 01_basic_server.py` (waits silently on stdin; Ctrl+C to stop) |
| 2 | `02_server_with_tool.py` | Tool = action | open with the Inspector (see section 3) |
| 3 | `03_server_with_resource.py` | Resource = information | open with the Inspector |
| 4 | `04_server_with_prompt.py` | Prompt = reusable template | open with the Inspector |
| 5 | `05_client.py` | Client connects and lists tools, resources, prompts | `python 05_client.py` |
| 6 | `06_tool_client.py` | Call tool, read resource, get prompt | `python 06_tool_client.py` |
| 7 | `07_transport_example.py` | Streamable HTTP transport | terminal 1: `python 07_transport_example.py server`, terminal 2: `python 07_transport_example.py client` |
| 8 | `08_final_mcp_server.py` | Validation, permissions, audit logging, progress | `python 08_final_mcp_server.py` (stdio) or set `MCP_TRANSPORT=http` |

The servers do nothing visible when started directly. A stdio server waits for a client on stdin. Use a client (files 05 to 07) or the Inspector to talk to them.

### Environment variables used by `08_final_mcp_server.py`

| Variable | Default | Meaning |
|---|---|---|
| `CATALOG_ALLOW_WRITES` | unset (writes disabled) | Set to `1` to enable the `update_stock` tool |
| `MCP_TRANSPORT` | `stdio` | Set to `http` to serve Streamable HTTP |
| `PORT` | `8000` | HTTP port when `MCP_TRANSPORT=http` |

```powershell
# PowerShell
$env:CATALOG_ALLOW_WRITES="1"; $env:MCP_TRANSPORT="http"; python 08_final_mcp_server.py
```
```bash
# bash
CATALOG_ALLOW_WRITES=1 MCP_TRANSPORT=http python 08_final_mcp_server.py
```

## 3. MCP Inspector

The Inspector is the official tool for testing servers. It runs through `npx`, so no install is needed (Node.js 22.19 or newer).

**Web UI, stdio server** (the Inspector starts the server for you):

```bash
# Windows
npx @modelcontextprotocol/inspector .venv\Scripts\python.exe 04_server_with_prompt.py
# macOS / Linux
npx @modelcontextprotocol/inspector .venv/bin/python 04_server_with_prompt.py
```

The command prints a URL with a one-time session token. Open it, click **Connect**, then use the **Tools**, **Resources** and **Prompts** tabs.

**CLI mode** (good for quick checks and CI):

```bash
npx @modelcontextprotocol/inspector --cli .venv/bin/python 04_server_with_prompt.py --method tools/list
npx @modelcontextprotocol/inspector --cli .venv/bin/python 04_server_with_prompt.py \
    --method tools/call --tool-name get_product --tool-arg product_id=P200
```

**HTTP server** (start `python 07_transport_example.py server` first):

```bash
npx @modelcontextprotocol/inspector --server-url http://127.0.0.1:8000/mcp --transport http
```

The SDK also has a shortcut, `mcp dev 04_server_with_prompt.py`, which launches the Inspector through `uv`. It needs `uv` on PATH.

## 4. Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'mcp.server'` or `cannot import name 'MCPServer'` | Old v1 SDK installed (`FastMCP` era) | `pip install "mcp[cli]==2.3.0"` inside the venv |
| Client hangs or prints `Connection closed` | The server printed to **stdout** or crashed at startup | Log to stderr only. Run the server file directly to see the traceback |
| `npx` not found or Inspector fails to start | Node.js missing or older than 22.19 | Install a current Node.js LTS |
| `Address already in use` on port 8000 | Another server is still running | Stop it, or use `PORT=8001` with file 08 |
| Tool returns `Error executing tool ...` without your message | A plain exception was raised | Raise `ToolError("message")` for errors the caller should see |
| Raw `curl` to `/mcp` returns `Missing session ID` | No `MCP-Protocol-Version: 2026-07-28` header, so the server treats it as a legacy (2025) client | Send that header plus `Mcp-Method` (see the guide, Module 3) |
