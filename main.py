from openai import OpenAI
import json

# 请替换成你的OpenAI API Key
client = OpenAI(api_key="sk-c4d67b703ba447ed9bd593d71562103c", base_url="https://api.deepseek.com")



topic="any"
history=[]

prompt_chat = {
    "role":"system", "content": """
    你叫做Alex，今年19岁，是一位英文学习助手，用CET4级英语和用户进行对话，每次回复不超过4句话，不多于60个单词。回答分为两部分，一部分进行对话，一部分指出用户的错误。
    你在给出回复要求如下：
    1.用包含Reply键值对，Error数组和布尔键值对End的json文件返回你的回答。 
    2.Reply键直接对应一条字符串，输出你给出的回答，不在其中提及用户的英文使用错误。
    3.在Errors列表，将问题分类为“语法问题” “语句不通” “用词不当”，“习惯文化不符”,“逻辑混乱”部分。每个错误输出对象包含“问题分类”，“问题说明”，“修改建议”键值对,分别用problem, explain, suggestion表示。 
    4.如果你认为对话完全可以结束或者你收到单独的一条“<END>”提示词,此时将返回的End项设为True,否则设置为False。
    
    EXAMPLE JSON OUTPUT:
    {
        "Reply": "I don't understand. Can you explain more about games you like?",
        "Errors": [
            {
            "problem": "语法问题",
            "explain": "句子不完整",
            "suggestion": "建议补充完整句子，如'I feel bad about this game'"
            }
        ],
        "End": false
    }
    """
}

prompt_conclusion = {
    "role":"system", 
    "content" : """
    你是一位英文老师，现在你有一段基于CET4级英语和包含用户和你进行对话的内容。基于以上的对话内容，对对话过程进行评价，总字数在100字左右，同时给出若干个你认为适合讨论话题的单词。
    你的回答要求如下：
    1.用包含Assess键值对和Vocabulary数组的json文件返回你的回答。 
    2.Assess键对应一条字符串，以第二人称称呼用户，用中文输出你给出的评价。 
    3.在Vocabulary数组，基于整个对话的长度，输出4-20个所有你推荐的值得用户学习掌握的单词，其中不包含单词缩写。每个单词对象要求包含“eng”，“chn”两个键值对，分别对应原英文单词和对应的中文释义

    EXAMPLE JSON OUTPUT:
    {
        "Assess": "你在对话中使用了礼貌的语言，这利于学习交流。作为英语学习者，掌握礼貌用语和表达方式是非常重要的。建议你在未来的交流中保持礼貌，这样不仅能更好地学习英语，也能与他人建立良好的沟通关系。",
        "Vocabulary": [
            {
            "eng": "Goodbye",
            "chn": "再见"
            },
            {
            "eng": "Farewell",
            "chn": "告别"
            },
            {
            "eng": "Polite",
            "chn": "有礼貌的"
            }
        ]
    }
"""
}

def chatbot(query):
    messages = [prompt_chat]
    for q, a in history:
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )
    response_json=json.loads(response.choices[0].message.content)  # Ensure the response is in JSON format
    answer = response_json["Reply"] # Extract the reply from the response
    error = response_json["Errors"]  # Extract the error list from the response
    for err in error:
        print(f"问题分类: {err['problem']}, 问题说明: {err['explain']}, 修改建议: {err['suggestion']}")
    ENDTAG = response_json["End"]  # Extract the end flag from the response

    history.append((query,answer))
    return answer,ENDTAG  

def concludebot():
    messages = [prompt_conclusion]
    for q, a in history:
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )

    response_json=json.loads(response.choices[0].message.content)  # Ensure the response is in JSON format
    assess = response_json["Assess"]  # Extract the assessment from the response
    vocabulary = response_json["Vocabulary"]  # Extract the vocabulary list from the response
    for word in vocabulary:
        print(f"单词: {word['eng']}, 释义: {word['chn']}")
    return assess


if __name__ == "__main__":
    while True:
        query = input("You: ")
        answer,ENDTAG=chatbot(query=query)
        print(answer)
        if ENDTAG:
            break
print(concludebot())