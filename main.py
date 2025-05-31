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
    messages=[{"role": "system", "content": "你叫做Alex,是一位英文学习助手，用CET4级英语和用户进行关于"+topic+"主题对话，每次回复不超过3句话，不多于40个单词。一直保持对话进行知道你认为对话完全可以结束或者你就收到单独的一条“<END>”提示词。\n 你总共需要完成三个任务，1.回复用户说的内容 2. 用中文总结用户的语法错误 3. 在自己的回答中向用户推荐3-10个相关新词汇。\n 你在给出评价时的回复要求如下：1.不要使用Markdown格式 2.用Reply,Error,Vocabulary三个板块，分别表示你的回复，总结的错误和新的词汇，生成一段json你的回答。 3.在Reply模块，单独放置一个字符串，表示你的回复。 4.在Error板块，使用中文总结所有的问题，包括语法词汇问题。 5.在 Vocabulary板块，分别输出所有你推荐的单词。"}]
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
            {"role":"system", "content": "你叫做Alex,是一位英文学习助手，用CET4级英语和用户进行关于"+topic+"主题对话，每次回复不超过3句话，不多于40个单词。一直保持对话进行知道你认为对话完全可以结束或者你就收到单独的一条“<END>”提示词。\n 在对话结束后，你需要对和用户的对话过程进行评价，要求：1. 用中文总结用户的语法错误 2. 在自己的回答中向用户推荐3-10个相关新词汇。\n 你在给出评价时的回复要求如下：1.不要使用Markdown格式 2.用Reply,Error,Vocabulary区分三个板块的json文件返回你的回答。 3.在Reply模块，单独放置一个字符串，输出你的评价。 4.在Error板块，将问题分类为“语法问题” “语句不通” “用词不当”三个部分。对于每个错误输出“问题分类”，“问题说明”，“修改建议”三个部分。 5.在 Vocabulary板块，分别输出所有你推荐的单词。"},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content
response=get_response("Who is LeBron James","sports")  # Example usage
print(response)
'''
chat_training(topic="game")