from openai import OpenAI

#client = OpenAI(base_url='http://localhost:10098/v1',api_key='ollama', # 必填项，但在Ollama中会被忽略)

client = OpenAI(api_key="sk-c4d67b703ba447ed9bd593d71562103c", base_url="https://api.deepseek.com")


def get_response(input_messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=input_messages
    )
    return response

def chat_training(topic="any"):
    input_content = input("学生:")
    messages=[{"role": "system", "content": "你叫Alex，15岁美国学生。用CET4级英语和用户进行"+topic+"主题对话，每次回复不超过2句话。对话结束后：1. 用中文总结用户的语法错误 2. 在自己的回答中向用户推荐3个相关新词汇。请用Reply,Error,Vocabulary区分三个板块，用json格式返回你的回答。"}]
    while input_content!='exit':
        messages.append({"role": "user", "content": input_content})
        response = get_response(messages)
        messages.append(response.choices[0].message)
        print("AI:"+response.choices[0].message.content)
        input_content = input("学生:")
        #print("-------type",type(response))
'''
def get_response(prompt,topic="any"):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你叫Alex，15岁美国学生。用CET4级英语和用户进行"+topic+"主题对话，每次回复不超过2句话。对话结束后：1. 用中文总结用户的语法错误 2. 在自己的回答中向用户推荐3个相关新词汇。请用Reply,Error,Vocabulary区分三个板块，用json格式返回你的回答。"},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content
response=get_response("Who is LeBron James","sports")  # Example usage
print(response)
'''
chat_training(topic="game")