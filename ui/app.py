import gradio as gr
from core.graph import build_mind_graph
from langchain_core.messages import HumanMessage
from rich.console import Console

console = Console()
mind = build_mind_graph()

def run_mind(goal: str, history: list):
    if not goal.strip():
        return history, "Please enter a goal."
    
    # Initial state
    initial_state = {
        "messages": [HumanMessage(content=goal)],
        "goal": goal,
        "plan": [],
        "current_step": 0,
        "research_notes": [],
        "final_answer": None,
        "status": "planning"
    }
    
    try:
        result = mind.invoke(initial_state)
        answer = result.get("final_answer", "No answer generated.")
        plan = result.get("plan", [])
        
        # Format nice response
        plan_text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(plan)]) if plan else "No plan"
        full_response = f"**Goal:** {goal}\n\n**Plan Created:**\n{plan_text}\n\n---\n\n**Final Answer:**\n{answer}"
        
        history.append((goal, full_response))
        return history, ""
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        history.append((goal, error_msg))
        return history, ""

def create_ui():
    with gr.Blocks(
        title="MindCore - Advanced Cognitive System",
        theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="slate"),
        css="""
        .gradio-container { max-width: 900px !important; }
        .chatbot { min-height: 500px; }
        """
    ) as demo:
        gr.Markdown("""
        # 🧠 MindCore
        **Advanced Multi-Agent Cognitive System**  
        Enter any goal and watch the mind plan → research → answer.
        """)
        
        chatbot = gr.Chatbot(
            label="MindCore Conversation",
            height=500,
            show_label=True,
            avatar_images=(None, "🧠")
        )
        
        with gr.Row():
            txt = gr.Textbox(
                placeholder="Example: Explain how to build a powerful AI agent system step by step",
                label="Your Goal",
                scale=4,
                lines=2
            )
            btn = gr.Button("Run MindCore", variant="primary", scale=1)
        
        clear = gr.Button("Clear Chat")
        
        btn.click(fn=run_mind, inputs=[txt, chatbot], outputs=[chatbot, txt])
        txt.submit(fn=run_mind, inputs=[txt, chatbot], outputs=[chatbot, txt])
        clear.click(lambda: ([], ""), outputs=[chatbot, txt])
        
        gr.Markdown("""
        ---
        **Status:** Day 1 Foundation | Powered by LangGraph + Ollama (llama3.2)  
        Agents: Planner → Researcher → Final Synthesizer
        """)
    
    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
