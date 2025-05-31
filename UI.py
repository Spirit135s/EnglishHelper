from openai import OpenAI
import gradio as gr
import json

# 请替换成你的OpenAI API Key
client = OpenAI(api_key="sk-c4d67b703ba447ed9bd593d71562103c", base_url="https://api.deepseek.com")



topic="game"

def chatbot(query, history):
    messages = [{"role":"system", "content": "你叫做Alex,是一位英文学习助手，用CET4级英语和用户进行关于"+topic+"主题对话，每次回复不超过3句话，不多于40个单词,同时回答要求用中文总结用户的语法错误 \n 你在给出回复要求如下：1.不要使用Markdown格式 2.用包含Reply对象，Error数组和键值对布尔End的json文件返回你的回答。 3.在Reply对象，单独放置一个字符串，输出你给出的回答。 4.在Error列表，将问题分类为“语法问题” “语句不通” “用词不当”，“习惯文化不符”,“逻辑混乱”部分。每个错误输出对象包含“问题分类”，“问题说明”，“修改建议”键值对,分别用problem, explain, suggestion表示。 5.如果你认为对话完全可以结束或者你就收到单独的一条“<END>”提示词,此时将返回的End项设为True,否则设置为False。"}]
    for q, a in history:
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    response_json=json.loads(response.choices[0].message.content)  # Ensure the response is in JSON format
    answer = response_json["Reply"] # Extract the reply from the response
    error = response_json["Error"]  # Extract the error list from the response
    for err in error:
        print(f"问题分类: {err['problem']}, 问题说明: {err['explain']}, 修改建议: {err['suggestion']}")
    end = response_json["End"]  # Extract the end flag from the response
    return answer  # Only return the answer, not the history

gr.ChatInterface(chatbot, title="和Alex练习对话", description="请随意想一个话题，使用英文开始对话吧").launch()