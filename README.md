# MindCore 🧠

**Advanced Multi-Agent Cognitive System**  
A powerful, future-proof "mind-based" AI agent framework built entirely on free open-source tools from GitHub.  
Designed to remain relevant and powerful till 2031 and beyond.

## Vision
MindCore acts as a central intelligent mind that can:
- Plan complex tasks
- Orchestrate specialized agents
- Maintain long-term memory
- Use tools (code execution, browser, APIs, files)
- Self-improve over time
- Work with local or cloud LLMs

## Core Stack (All Free & Open Source)
- **Orchestration**: LangGraph + CrewAI
- **Agents Runtime**: LangGraph Deep Agents / custom agents
- **Memory**: LangGraph checkpoints + vector store (Chroma / Qdrant)
- **Tools & Protocol**: MCP (Model Context Protocol), browser-use
- **Local Models**: Ollama
- **UI**: Gradio (quick start) → Next.js (production)
- **Sandbox**: Docker / E2B style

## Project Structure
```
MindCore/
├── agents/           # Specialized agents (Planner, Researcher, Coder, Critic, Memory)
├── core/             # Main orchestration, graph, state
├── memory/           # Long-term & short-term memory
├── tools/            # Custom tools + MCP integration
├── ui/               # Gradio / Streamlit interface
├── configs/          # Model configs, agent roles
├── data/             # Local knowledge / embeddings
├── tests/
├── requirements.txt
├── .env.example
└── main.py           # Entry point
```

## Quick Start (VS Code)
1. Clone the repo
2. Create virtual environment
3. `pip install -r requirements.txt`
4. Install Ollama and pull a model (`ollama pull llama3.2` or qwen2.5)
5. Copy `.env.example` to `.env` and set keys if needed
6. Run `python main.py`

## Status
🚧 Under active construction - Day 1

Built with ❤️ for the open-source future.
