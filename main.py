from openai import OpenAI
import json

# 请替换成你的OpenAI API Key
client = OpenAI(api_key="sk-c4d67b703ba447ed9bd593d71562103c", base_url="https://api.deepseek.com")



topic="any"
history=[]

def chatbot(query):
    messages = [{"role":"system", "content": """
    你叫做Alex,是一位英文学习助手，用CET4级英语和用户进行对话，每次回复不超过4句话，不多于60个单词。回答分为两部分，一部分进行对话，一部分指出用户的错误。
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
    """}]
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

if __name__ == "__main__":
    while True:
        query = input("You: ")
        answer,ENDTAG=chatbot(query=query)
        print(answer)
        if ENDTAG:
            break
  