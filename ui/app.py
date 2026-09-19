import gradio as gr
from core.graph import build_mind_graph
from langchain_core.messages import HumanMessage
import time

mind = build_mind_graph()

def run_mind(goal: str, history: list):
    if not goal or not goal.strip():
        return history, ""
    
    history = history or []
    
    # Show thinking state immediately
    history = history + [(goal, "🧠 *MindCore is thinking...*")]
    yield history, ""
    
    initial_state = {
        "messages": [HumanMessage(content=goal)],
        "goal": goal.strip(),
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
        
        # Replace thinking message with real answer
        history = history[:-1] + [(goal, answer + f"\n\n---\n*Responded in {elapsed:.1f}s*")]
        yield history, ""
        
    except Exception as e:
        history = history[:-1] + [(goal, f"❌ Error: {str(e)}")]
        yield history, ""

def create_ui():
    with gr.Blocks(title="MindCore") as demo:
        
        gr.HTML("""
        <div style="text-align:center; margin-bottom: 12px;">
            <h1 style="font-size: 2.3rem; font-weight: 700; margin: 0; letter-spacing: -0.5px;">
                🧠 MindCore
            </h1>
            <p style="color: #64748b; font-size: 1.05rem; margin-top: 6px;">
                Elite Cognitive System • Fast • Local • Private
            </p>
        </div>
        """)
        
        chatbot = gr.Chatbot(
            height=520,
            show_label=False,
            type="tuples"
        )
        
        with gr.Row():
            txt = gr.Textbox(
                placeholder="Ask anything... (e.g. Design a complete multi-agent architecture)",
                show_label=False,
                scale=6,
                lines=2,
                max_lines=5
            )
            submit_btn = gr.Button("Send", variant="primary", scale=1, min_width=110)
        
        with gr.Row():
            clear_btn = gr.Button("Clear", variant="secondary", size="sm")
            gr.HTML("<div style='flex:1'></div>")
            gr.HTML("<span style='color:#94a3b8;font-size:0.8rem;'>Powered by llama3.2 • Local</span>")
        
        # Events
        submit_btn.click(
            fn=run_mind,
            inputs=[txt, chatbot],
            outputs=[chatbot, txt]
        )
        txt.submit(
            fn=run_mind,
            inputs=[txt, chatbot],
            outputs=[chatbot, txt]
        )
        clear_btn.click(lambda: ([], ""), outputs=[chatbot, txt])
        
        gr.HTML("""
        <div style="text-align:center; color:#94a3b8; font-size:0.85rem; margin-top:18px;">
            MindCore v0.2 • Production Foundation • Built for speed & clarity
        </div>
        """)
    
    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        theme=gr.themes.Soft(primary_hue="violet", secondary_hue="slate", neutral_hue="slate"),
        css=".gradio-container { max-width: 860px !important; margin: auto !important; }"
    )
