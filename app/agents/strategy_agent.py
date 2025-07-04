# 최종 투자 전략 작성 (LLM)
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def build_strategy(state):
    llm = AzureChatOpenAI(
        api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
        api_version="2024-05-01-preview",
        deployment_name=os.getenv("AOAI_DEPLOY_GPT4O")
    )
    prompt = f"""
    사용자 투자 성향: {state['investor_profile']}

    [요약된 자산 정보]
    {state['summary']}

    위 정보를 바탕으로 맞춤형 투자 전략 3가지를 제시해줘.
    """
    result = llm.invoke(prompt)
    state["final_strategy"] = result.content
    return state