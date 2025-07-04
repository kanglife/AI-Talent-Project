from langgraph.graph import StateGraph, END
from agents.summary_agent import summarize_data
from agents.strategy_agent import build_strategy
from agents.wiki_agent import wiki_search
from typing import TypedDict

class InvestmentState(TypedDict):
    investment_data: str
    investor_profile: str
    wiki_summary: str
    summary: str
    final_strategy: str

def create_agent_flow():
    builder = StateGraph(InvestmentState)

    builder.add_node("wiki", wiki_search)
    builder.add_node("summarize", summarize_data)
    builder.add_node("strategy", build_strategy)

    builder.set_entry_point("wiki")               
    builder.add_edge("wiki", "summarize")
    builder.add_edge("summarize", "strategy")
    builder.add_edge("strategy", END)

    return builder.compile()
