# agents/wiki_agent.py
import os
from dotenv import load_dotenv
from typing import Dict
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain_openai import AzureChatOpenAI

load_dotenv()

# ReAct Tool Agent 생성 함수
def create_react_tool_agent():
    llm = AzureChatOpenAI(
        api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
        api_version="2024-05-01-preview",
        deployment_name=os.getenv("AOAI_DEPLOY_GPT4O"),
    )

    wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    tools = [
        Tool(
            name="Wikipedia Search",
            func=wiki_tool.run,
            description="Wikipedia에서 정보를 검색합니다. 반드시 Thought, Action, Action Input 형식으로 출력하세요."
        )
    ]

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

# LangGraph에 연결할 노드 함수
def wiki_search(state: Dict) -> Dict:
    query = state["investment_data"]
    agent = create_react_tool_agent()
    result = agent.run(f"{query} 관련 정보를 Wikipedia에서 찾아줘")
    state["wiki_summary"] = result
    return state
