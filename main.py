"""
MindCore - Advanced Multi-Agent Cognitive System
Entry Point
"""

import os
from dotenv import load_dotenv
from rich.console import Console
from ui.app import create_ui

load_dotenv()
console = Console()

def main():
    console.print("[bold cyan]🧠 MindCore v0.1[/bold cyan]")
    console.print("[green]Multi-Agent Cognitive System is starting...[/green]")
    console.print("Agents: Planner → Researcher → Final Synthesizer")
    console.print("LLM: Ollama (llama3.2)")
    console.print("UI: Gradio on http://127.0.0.1:7860")
    console.print("-" * 50)
    
    demo = create_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()
