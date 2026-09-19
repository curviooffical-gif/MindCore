"""
MindCore - Elite Cognitive System
"""

from dotenv import load_dotenv
from rich.console import Console
import gradio as gr
from ui.app import create_ui

load_dotenv()
console = Console()

def main():
    console.print("[bold magenta]🧠 MindCore v0.2[/bold magenta]")
    console.print("[green]Fast Cognitive System ready[/green]")
    console.print("Open → http://127.0.0.1:7860")
    console.print("-" * 40)
    
    demo = create_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        theme=gr.themes.Soft(primary_hue="violet", secondary_hue="slate"),
        css=".gradio-container { max-width: 880px !important; margin: auto !important; }"
    )

if __name__ == "__main__":
    main()
