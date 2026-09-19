from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class MindState(TypedDict):
    """Central state of MindCore - the shared mind memory"""
    messages: Annotated[List[BaseMessage], add_messages]
    goal: str
    plan: List[str]
    current_step: int
    research_notes: List[str]
    final_answer: Optional[str]
    status: str  # planning | researching | answering | done
