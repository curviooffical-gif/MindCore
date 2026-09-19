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
    history.append((goal, "🧠 *MindCore is thinking...*"))
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
        
        # Replace the thinking message with real answer
        history[-1] = (goal, answer + f"\n\n---\n*Responded in {elapsed:.1f}s*")
        yield history, ""
        
    except Exception as e:
        history[-1] = (goal, f"❌ Error: {str(e)}")
        yield history, ""

def create_ui():
    custom_css = """
    .gradio-container {
        max-width: 860px !important;
        margin: auto !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }
    .main-title {
        text-align: center;
        margin-bottom: 8px !important;
    }
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 24px !important;
    }
    footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 20px;
    }
    """
    
    with gr.Blocks(
        title="MindCore",
        theme=gr.themes.Soft(
            primary_hue="violet",
            secondary_hue="slate",
            neutral_hue="slate",
            font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"]
        ),
        css=custom_css
    ) as demo:
        
        gr.HTML("""
        <div class="main-title">
            <h1 style="font-size: 2.4rem; font-weight: 700; margin: 0; letter-spacing: -0.5px;">
                🧠 MindCore
            </h1>
        </div>
        <p class="subtitle">Elite Cognitive System • Fast • Local • Private</p>
        """)
        
        chatbot = gr.Chatbot(
            height=520,
            show_label=False,
            container=True,
            bubble_full_width=False,
            avatar_images=(
                None,
                "https://api.dicebear.com/7.x/bottts/svg?seed=MindCore&backgroundColor=7c3aed"
            )
        )
        
        with gr.Row(equal_height=True):
            txt = gr.Textbox(
                placeholder="Ask anything... (e.g. Design a complete multi-agent architecture)",
                show_label=False,
                container=False,
                scale=6,
                lines=2,
                max_lines=4
            )
            submit_btn = gr.Button("Send", variant="primary", scale=1, min_width=100)
        
        with gr.Row():
            clear_btn = gr.Button("Clear", variant="secondary", size="sm")
            gr.HTML("<div style='flex:1'></div>")
            gr.HTML("<span style='color:#94a3b8;font-size:0.8rem;align-self:center;'>Powered by llama3.2 • Local</span>")
        
        # Events
        submit_btn.click(
            fn=run_mind,
            inputs=[txt, chatbot],
            outputs=[chatbot, txt],
            show_progress="full"
        )
        txt.submit(
            fn=run_mind,
            inputs=[txt, chatbot],
            outputs=[chatbot, txt],
            show_progress="full"
        )
        clear_btn.click(lambda: ([], ""), outputs=[chatbot, txt])
        
        gr.HTML("""
        <div class="footer">
            MindCore v0.2 • Production Foundation • Built for speed & clarity
        </div>
        """)
    
    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
