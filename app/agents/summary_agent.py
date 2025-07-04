# 투자 자산 요약 (LLM)
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def summarize_data(state):
    data = state["investment_data"]
    profile = state["investor_profile"]

    llm = AzureChatOpenAI(
        api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
        api_version="2024-05-01-preview",
        deployment_name=os.getenv("AOAI_DEPLOY_GPT4O")
    )

    prompt = f"""
    너는 투자 분석가야. 사용자의 투자성향은 \"{profile}\"이야.
    아래의 자산 정보를 간단히 요약해줘:
    {data}
    """
    result = llm.invoke(prompt)
    state["summary"] = result.content
    return state