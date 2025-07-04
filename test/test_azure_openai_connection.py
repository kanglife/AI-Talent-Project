import openai
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

client = openai.AzureOpenAI(  # openai>=1.0.0 기준
    api_key=os.getenv("AOAI_API_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AOAI_ENDPOINT")
)

response = client.chat.completions.create(
    model=os.getenv("AOAI_DEPLOY_GPT4O"),
    messages=[
        {"role": "user", "content": "ping"}
    ]
)

print("✅ 연결 성공! 응답:")
print(response.choices[0].message.content)
