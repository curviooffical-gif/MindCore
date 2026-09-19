from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from core.state import MindState

# Maximum speed for local llama3.2
llm = ChatOllama(
    model="llama3.2",
    temperature=0.2,
    num_predict=400,
    num_ctx=2048,
)

def mind_node(state: MindState) -> MindState:
    goal = state.get("goal", "")

    system = SystemMessage(content="""You are MindCore, an elite cognitive AI.
Give clear, structured, high-value answers.
Be direct and useful. Use markdown when helpful.""")

    response = llm.invoke([system, HumanMessage(content=goal)])

    return {
        "final_answer": response.content,
        "status": "done",
        "messages": [AIMessage(content=response.content)],
        "plan": [],
        "research_notes": []
    }

def build_mind_graph():
    graph = StateGraph(MindState)
    graph.add_node("mind", mind_node)
    graph.set_entry_point("mind")
    graph.add_edge("mind", END)
    return graph.compile()
