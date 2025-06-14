from openai import OpenAI
import gradio as gr
import json

# 请替换成你的OpenAI API Key
client = OpenAI(api_key="", base_url="https://api.deepseek.com")

# 系统提示词
chat_prompt = """
    你叫做Alex,是一位英文学习助手，用CET4级英语和用户进行对话，每次回复不超过4句话，不多于60个单词。回答分为两部分，一部分进行对话，一部分指出用户的错误。
    你在给出回复要求如下：
    1.用包含Reply键值对，Error数组和布尔键值对End的json文件返回你的回答。 
    2.Reply键直接对应一条字符串，输出你给出的回答，不在其中提及用户的英文使用错误。
    3.在Errors列表，将问题分类为"语法问题" "语句不通" "用词不当"，"习惯文化不符","逻辑混乱"部分。每个错误输出对象包含"问题分类"，"问题说明"，"修改建议"键值对,分别用problem, explain, suggestion表示。 
    4.如果你认为对话完全可以结束或者你收到单独的一条"<END>"提示词,此时将返回的End项设为True,否则设置为False。
"""

conclusion_prompt = """
    你是一位英文老师，现在你有一段基于CET4级英语和包含用户和你进行对话的内容。基于以上的对话内容，对对话过程进行评价，总字数在100字左右，同时给出若干个你认为适合讨论话题的单词。
    你的回答要求如下：
    1.用包含Assess键值对和Vocabulary数组的json文件返回你的回答。 
    2.Assess键对应一条字符串，以第二人称称呼用户，用中文输出你给出的评价。 
    3.在Vocabulary数组，基于整个对话的长度，输出4-20个所有你推荐的值得用户学习掌握的单词，其中不包含单词缩写。每个单词对象要求包含"eng"，"chn"两个键值对，分别对应原英文单词和对应的中文释义
"""

translate_prompt = """
    你是一位翻译助手，负责将用户输入的英文句子翻译成中文。
    你的回答要求如下：
    1.用包含Reply键值对和Vocabulary的链表的json文件返回你的回答。
    2.Reply键直接对应一条字符串，输出你给出的翻译结果。
    3.尽可能的使用CET4级别的语句去翻译用户的句子。
    4.Vocabulary数组，基于用户输入的句子，输出4-20个所有你推荐的值得用户学习掌握的单词，其中不包含单词缩写。每个单词对象要求包含"eng"，"chn"两个键值对，分别对应原英文单词和对应的中文释义。
"""

exam_prompt = """    
    你是一位英语考试助手，负责根据用户提供的单词列表生成一份英语考试题目。
    你的回答要求如下：
    1.用包含题目总数Total和Exam链表的json文件返回你的回答。
    2.Exam链表中每一个数组对应一道题目，输出你生成的考试题目。
    3.每个题目数组，包含三个键值对，分别为题目类型，题干和题目参考答案，对应键名字为"type","question","answer"。
    3.考试类型包含单词挖空拼写（即去除单词中间的若干字母）、中文释义翻译，完形填空，首字母填空。题目数量在10-15道之间。
    4.题目应适合CET4级别的英语学习者，难度适中。
    5.返回的json按照题目类型排序输出题目。
"""

def combine_messages(prompt, query, history):
    messages = []
    messages.append({"role":"system", "content": prompt})
    for q, a in history:
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": query})
    return messages

def chatbot(query, history):
    messages = combine_messages(chat_prompt, query, history)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )
    response_json = json.loads(response.choices[0].message.content)
    answer = response_json["Reply"]
    error = response_json["Errors"]
    error_text = ""
    for err in error:
        error_text += f"问题分类: {err['problem']}\n问题说明: {err['explain']}\n修改建议: {err['suggestion']}\n\n"
    end = response_json["End"]

    if end:
        messages = combine_messages(conclusion_prompt, query, history)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={
                'type': 'json_object'
            }
        )
        response_json = json.loads(response.choices[0].message.content)
        assess = response_json["Assess"]
        vocabulary = response_json["Vocabulary"]
        vocab_text = "推荐单词：\n"
        for word in vocabulary:
            vocab_text += f"{word['eng']}: {word['chn']}\n"
        answer += "\n\n------对话结束------\n\n"
        answer += assess + "\n\n" + vocab_text

    return answer, error_text

def translate(text):
    messages = [
        {"role": "system", "content": translate_prompt},
        {"role": "user", "content": text}
    ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )
    response_json = json.loads(response.choices[0].message.content)
    translation = response_json["Reply"]
    vocabulary = response_json["Vocabulary"]
    vocab_text = "推荐单词：\n"
    for word in vocabulary:
        vocab_text += f"{word['eng']}: {word['chn']}\n"
    return translation, vocab_text

def generate_exam(vocab_text):
    try:
        vocabulary = json.loads(vocab_text)
    except:
        return "请输入有效的JSON格式单词列表"
    
    messages = [
        {"role": "system", "content": exam_prompt},
        {"role": "user", "content": json.dumps(vocabulary)}
    ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )
    response_json = json.loads(response.choices[0].message.content)
    exam = response_json["Exam"]
    result = f"共{response_json['Total']}道题目：\n\n"
    for i, q in enumerate(exam, 1):
        result += f"{i}. {q['type']}\n{q['question']}\n答案：{q['answer']}\n\n"
    return result

# 创建Gradio界面
with gr.Blocks(title="英语学习助手") as demo:
    gr.Markdown("# 英语学习助手")
    
    with gr.Tab("对话练习"):
        chatbot_interface = gr.ChatInterface(
            chatbot,
            title="和Alex练习对话",
            description="请随意想一个话题，使用英文开始对话吧",
            examples=["Hello, how are you?", "What's your favorite movie?", "Tell me about your hobbies."],
            retry_btn=None,
            undo_btn=None,
            clear_btn="清除对话",
        )
    
    with gr.Tab("翻译辅助"):
        with gr.Row():
            with gr.Column():
                translate_input = gr.Textbox(label="请输入英文", placeholder="输入要翻译的英文...")
                translate_btn = gr.Button("翻译")
            with gr.Column():
                translate_output = gr.Textbox(label="中文翻译", lines=3)
                vocab_output = gr.Textbox(label="推荐单词", lines=5)
        translate_btn.click(
            translate,
            inputs=[translate_input],
            outputs=[translate_output, vocab_output]
        )
    
    with gr.Tab("试题生成"):
        with gr.Row():
            with gr.Column():
                vocab_input = gr.Textbox(
                    label="单词列表（JSON格式）",
                    placeholder='[{"eng": "hello", "chn": "你好"}, {"eng": "world", "chn": "世界"}]',
                    lines=5
                )
                exam_btn = gr.Button("生成试题")
            with gr.Column():
                exam_output = gr.Textbox(label="生成的试题", lines=20)
        exam_btn.click(
            generate_exam,
            inputs=[vocab_input],
            outputs=[exam_output]
        )

demo.launch() 