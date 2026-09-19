import gradio as gr
from core.graph import build_mind_graph
from langchain_core.messages import HumanMessage
import time

mind = build_mind_graph()

def chat_fn(message: str, history: list):
    """Gradio 6 compatible - messages format"""
    if not message or not message.strip():
        yield history
        return

    history = history + [{"role": "user", "content": message}]
    history = history + [{"role": "assistant", "content": "🧠 Thinking..."}]
    yield history

    initial_state = {
        "messages": [HumanMessage(content=message)],
        "goal": message.strip(),
        "plan": [],
        "current_step": 0,
        "research_notes": [],
        "final_answer": None,
        "status": "thinking"
    }

    try:
        start = time.time()
        result = mind.invoke(initial_state)
        elapsed = time.time() - start

        answer = result.get("final_answer", "No response generated.")
        final = f"{answer}\n\n---\n*Responded in {elapsed:.1f}s*"

        history = history[:-1] + [{"role": "assistant", "content": final}]
        yield history

    except Exception as e:
        history = history[:-1] + [{"role": "assistant", "content": f"❌ Error: {str(e)}"}]
        yield history

def create_ui():
    demo = gr.ChatInterface(
        fn=chat_fn,
        title="🧠 MindCore",
        description="Elite Cognitive System • Fast • Local • Private",
        examples=[
            "Explain multi-agent AI systems simply",
            "Design a clean architecture for a powerful agent framework",
            "How can I make a local AI agent system very fast?"
        ],
        chatbot=gr.Chatbot(height=520),
        textbox=gr.Textbox(placeholder="Ask anything...", scale=7),
    )
    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        theme=gr.themes.Soft(primary_hue="violet", secondary_hue="slate"),
        css=".gradio-container { max-width: 880px !important; margin: auto !important; }"
    )
