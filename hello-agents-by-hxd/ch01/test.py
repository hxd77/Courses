from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL_ID = os.getenv("MODEL_ID")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

response = client.chat.completions.create(
    model=MODEL_ID,
    messages=[
        {"role": "user", "content": "你好，请只回复：测试成功"}
    ]
)

print(response.choices[0].message.content)