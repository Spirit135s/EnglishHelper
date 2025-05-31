from openai import OpenAI

client = OpenAI(
base_url='http://localhost:11434/v1',
api_key='ollama', # 必填项，但在Ollama中会被忽略
)

def get_response(prompt,topic="basketball"):
    response = client.chat.completions.create(
        model="qwen2.5:7b",
        messages=[
            {"role": "system", "content": "你叫Alex，15岁美国学生。用初中级英语和用户进行"+topic+"主题对话，每次回复不超过2句话。对话结束后：1. 用中文总结用户的语法错误 2. 在自己的回答中向用户推荐3个相关新词汇"},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

response=get_response("Who is LeBron James")  # Example usage
print(response)