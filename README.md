# Local Assistant

Fully local, privacy-focused personal assistant. No data leaves your machine.

Accessible via Telegram, powered by Ollama. Supports document search (RAG), shell commands, Obsidian note management, and autonomous agent behavior with tool calling.

## Features

- **ReAct Agent Loop** - qwen3:4b with function calling, text-based tool call parsing fallback
- **Obsidian Integration** - Hybrid read/write: filesystem for writes, GraphThulhu MCP for graph analysis
- **RAG** - LlamaIndex + LanceDB vector search over local documents
- **Smart Formatting** - `daily_log`, `sport_log`, `dream_log` tools handle markdown formatting in Python (no LLM formatting needed)
- **Memory** - SQLite conversation history + automatic fact extraction
- **Web Search** - SearxNG (self-hosted, no tracking)
- **Shell Commands** - Whitelisted safe command execution
- **Apple Reminders** - Create reminders via osascript

## Architecture

```
Telegram -> Bot Handler -> ReAct Agent Loop -> Ollama (qwen3:4b)
                                |
                    +-----------+-----------+
                    |           |           |
               Note Tools   RAG Search   MCP Client
               (filesystem) (LanceDB)   (GraphThulhu)
```

## Requirements

- Python 3.9+
- [Ollama](https://ollama.ai) with `qwen3:4b` and `nomic-embed-text`
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Optional: SearxNG (Docker), GraphThulhu MCP, Syncthing

## Setup

```bash
git clone https://github.com/bcemsayilar/local-assistant.git
cd local-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Pull models
ollama pull qwen3:4b
ollama pull nomic-embed-text

# Configure
cp .env.example .env
# Edit .env with your Telegram bot token and settings

# Set your git identity for commits
git config user.name "Your Name"
git config user.email "your-email@example.com"

# Run
python -m assistant.main
```

## Project Structure

```
assistant/
├── main.py              # FastAPI + Telegram startup
├── config.py            # Settings
├── agent/
│   ├── loop.py          # ReAct agent loop + text tool call parser
│   ├── prompts.py       # System prompt
│   └── tools.py         # Tool definitions + implementations
├── mcp/
│   └── client.py        # GraphThulhu MCP client
├── memory/              # SQLite conversation history + facts
├── rag/                 # Document indexing & retrieval
├── integrations/
│   └── telegram.py      # Telegram bot handler
└── db/                  # DB schema
```

## How It Works

The agent uses a ReAct (Reason + Act) loop. On each user message:

1. System prompt + conversation history sent to Ollama
2. Model decides to call a tool or respond directly
3. If tool call detected (native or text-parsed), tool executes and result feeds back
4. Loop continues until model gives a final text response
5. Duplicate tool call detection prevents infinite loops

### Text Tool Call Parser

qwen3:4b sometimes writes tool calls as plain text instead of using Ollama's native mechanism. The parser catches three patterns:
- `note_write(name="x", content="y")` - function style
- `{"name": "note_write", "arguments": {...}}` - JSON style
- `<tool_call>{...}</tool_call>` - XML style

## License

MIT
