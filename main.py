"""
MindCore - Entry Point
Advanced Multi-Agent Cognitive System
"""

import os
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

def main():
    console.print("[bold cyan]MindCore v0.1[/bold cyan] - Multi-Agent Cognitive System")
    console.print("Status: Day 1 - Foundation ready")
    console.print("\nNext steps:")
    console.print("1. Install dependencies: pip install -r requirements.txt")
    console.print("2. Install Ollama and pull a model")
    console.print("3. We will build agents, graph, and UI step by step")
    console.print("\nRepo: https://github.com/curviooffical-gif/MindCore")

if __name__ == "__main__":
    main()
