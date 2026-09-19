from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from core.state import MindState
from typing import Literal

# Local LLM via Ollama
llm = ChatOllama(model="llama3.2", temperature=0.3)

def planner_node(state: MindState) -> MindState:
    """Master Planner Agent - breaks the goal into clear steps"""
    goal = state.get("goal", "")
    system = SystemMessage(content="""You are the Master Planner of MindCore.
Your job is to break any goal into 3-6 clear, sequential steps.
Respond ONLY with a numbered list of steps. No extra text.""")
    human = HumanMessage(content=f"Goal: {goal}")
    response = llm.invoke([system, human])
    
    steps = [line.strip() for line in response.content.split("\n") if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith("-"))]
    if not steps:
        steps = [response.content.strip()]
    
    return {
        "plan": steps,
        "current_step": 0,
        "status": "researching",
        "messages": [AIMessage(content=f"Plan created with {len(steps)} steps:")]
    }

def researcher_node(state: MindState) -> MindState:
    """Researcher Agent - gathers knowledge for the current step"""
    plan = state.get("plan", [])
    step_idx = state.get("current_step", 0)
    
    if step_idx >= len(plan):
        return {"status": "answering"}
    
    current_step = plan[step_idx]
    system = SystemMessage(content="""You are the Deep Researcher of MindCore.
Provide useful, accurate information and reasoning for the given step.
Be concise but insightful.""")
    human = HumanMessage(content=f"Current step to research: {current_step}\n\nOverall Goal: {state.get('goal')}")
    response = llm.invoke([system, human])
    
    notes = state.get("research_notes", []) + [f"Step {step_idx+1}: {response.content}"]
    
    return {
        "research_notes": notes,
        "current_step": step_idx + 1,
        "messages": [AIMessage(content=f"Researched step {step_idx+1}")]
    }

def answer_node(state: MindState) -> MindState:
    """Final Answer Agent - synthesizes everything into a clean response"""
    goal = state.get("goal", "")
    plan = state.get("plan", [])
    notes = state.get("research_notes", [])
    
    system = SystemMessage(content="""You are the Final Synthesizer of MindCore.
Create a clear, professional, complete answer based on the plan and research notes.
Write in a helpful, structured way.""")
    
    content = f"Goal: {goal}\n\nPlan:\n" + "\n".join(plan) + "\n\nResearch Notes:\n" + "\n\n".join(notes)
    human = HumanMessage(content=content)
    response = llm.invoke([system, human])
    
    return {
        "final_answer": response.content,
        "status": "done",
        "messages": [AIMessage(content=response.content)]
    }

def route_after_research(state: MindState) -> Literal["researcher", "answer"]:
    plan = state.get("plan", [])
    step = state.get("current_step", 0)
    if step < len(plan):
        return "researcher"
    return "answer"

def build_mind_graph():
    """Build the complete MindCore cognitive graph"""
    graph = StateGraph(MindState)
    
    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("answer", answer_node)
    
    graph.set_entry_point("planner")
    graph.add_edge("planner", "researcher")
    graph.add_conditional_edges("researcher", route_after_research, {
        "researcher": "researcher",
        "answer": "answer"
    })
    graph.add_edge("answer", END)
    
    return graph.compile()
