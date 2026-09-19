from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from core.state import MindState

# Optimized for speed on local models
llm = ChatOllama(
    model="llama3.2",
    temperature=0.25,
    num_predict=700,
)

def mind_node(state: MindState) -> MindState:
    """Single high-quality cognitive pass - much faster"""
    goal = state.get("goal", "")
    
    system = SystemMessage(content="""You are MindCore — an elite cognitive AI system.
You think deeply, structure your reasoning, and deliver clear, professional, high-value answers.
Be concise yet complete. Use markdown for readability when helpful.""")
    
    human = HumanMessage(content=goal)
    response = llm.invoke([system, human])
    
    return {
        "final_answer": response.content,
        "status": "done",
        "messages": [AIMessage(content=response.content)],
        "plan": ["Direct cognitive response"],
        "research_notes": []
    }

def build_mind_graph():
    graph = StateGraph(MindState)
    graph.add_node("mind", mind_node)
    graph.set_entry_point("mind")
    graph.add_edge("mind", END)
    return graph.compile()
