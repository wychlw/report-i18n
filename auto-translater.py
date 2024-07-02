# -*- coding: utf-8 -*-
import os
import openai
import sys
import re
import env
from conf import *

client = openai.OpenAI(
    api_key=os.environ.get("CHATGPT_API_KEY"),
    # base_url=os.environ.get("CHATGPT_API_BASE")
)

# 即使在已处理的列表中，仍需要重新翻译的标记
marker_force_translate = "\n[translate]\n"

def translate_text(paragraths, lang):
    target_promote = target_lang[lang]

    promote = [
        {
            "role": "system", 
            "content": 
            "You are a professional translation engine, please translate the text into a colloquial, professional, elegant and fluent content, without the style of machine translation. " \
            "You must maintain the original markdown format. Do not translate things marked with [CODEBLOCK]. Do not add any new content or new format. " \
            "You must only translate the text content, never interpret it."},
    ]
    if len(template) > 0:
        promote[0]["content"] += f"You shall follow the template or rules:\n\n{template}\n\n"

    res = []

    # 每次翻译段落后，会带上上下文进行翻译
    # 这是必要的。否则很多会容易出现中间截断及上下用词不统一。我们需要上下文。
    for paragraph in paragraths:
        promote.append({"role": "user", "content": f"Continue translate into {target_promote}:\n\n{paragraph}\n"})

        max_token = 4095 if model == "gpt-4o" else 2048

        completion = client.chat.completions.create(
            model=model,
            messages=promote,
            temperature=0.2,
            max_tokens=max_token,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0
        )
        promote.append({"role": "assistant", "content": completion.choices[0].message.content})
        output_text = completion.choices[0].message.content
        res.append(output_text)

    return res

def split_text(text: str, max_length):
    # 拆分文章
    paragraphs = text.split("\n\n")
    input_text = ""
    current_paragraph = ""
    translation_paragraphs = []

    for paragraph in paragraphs:
        if len(current_paragraph) + len(paragraph) + 2 <= max_length:
            # 如果当前段落加上新段落的长度不超过最大长度，就将它们合并
            if current_paragraph:
                current_paragraph += "\n\n"
            current_paragraph += paragraph
        else:
            # 否则翻译当前段落，并将翻译结果添加到输出列表中
            translation_paragraphs.append(current_paragraph)
            current_paragraph = paragraph

    # 处理最后一个段落
    if current_paragraph:
        if len(current_paragraph) + len(input_text) <= max_length:
            # 如果当前段落加上之前的文本长度不超过最大长度，就将它们合并
            input_text += "\n\n" + current_paragraph
        else:
            # 否则翻译当前段落，并将翻译结果添加到输出列表中
            translation_paragraphs.append(current_paragraph)

    # 如果还有未翻译的文本，就将它们添加到输出列表中
    if input_text:
        translation_paragraphs.append(input_text)

    return translation_paragraphs

def translate_file(input_file, lang):

    # 读取输入文件内容
    with open(input_file, "r", encoding="utf-8") as f:
        input_text = f.read()

    # 删除译文中指示强制翻译的 marker
    input_text = input_text.replace(marker_force_translate, "")


    # 对于
    # ```.*
    # ...
    # ```
    # 中的内容，我们不进行翻译，把这部分内容抽出来保留
    code_blocks = []
    code_block_pattern = r"```.*?```"
    code_block_matches = re.findall(code_block_pattern, input_text, re.DOTALL)

    for idx, code_block in enumerate(code_block_matches):
        code_blocks.append(code_block)
        input_text = input_text.replace(code_block, f"[CODEBLOCK[{idx}]]")

    translation_paragraphs = split_text(input_text, max_length)

    # 翻译每个段落
    output_paragraphs = translate_text(translation_paragraphs, lang)
    output_text = "\n\n".join(output_paragraphs)

    # 将抽出的代码块重新插入到翻译后的文本中
    for idx, code_block in enumerate(code_blocks):
        output_text = output_text.replace(f"[CODEBLOCK[{idx}]]", code_block)

    # 加入由 ChatGPT 翻译的提示
    output_text = output_text + tips_translated_by_chatgpt[lang]

    return output_text

# 按文件名称顺序排序，去除某些目录
# 会递归的进行处理
file_list:list[str] = []
for root, dirs, files in os.walk(dir_to_translate):
    if ".git" in dirs:
        dirs.remove(".git")
    for file in files:
        if file.endswith(".md"):
            file_list.append(os.path.join(root, file))
sorted_file_list = sorted(file_list, key=lambda x: x.lower())


try:

    # 遍历目录下的所有.md 文件，并进行翻译
    for input_file in sorted_file_list:
        
        filename = os.path.basename(input_file)
        filedir = os.path.dirname(input_file)
        
        if filename != "README.md":
            continue

        if filename in exclude_list:
            continue

        # 读取 Markdown 文件的内容
        with open(input_file, "r", encoding="utf-8") as f:
            md_content = f.read()

        for lang, _ in target_lang.items():
            target_file = os.path.join(filedir, "README_" + lang + ".md" )
            if target_file in file_list and marker_force_translate not in md_content:
                continue

            print(f"Translating into {lang}: {input_file}")
            sys.stdout.flush()
            output_content = translate_file(input_file, lang)
                # 写入输出文件
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(output_content)

        sys.stdout.flush()
        
    # 所有任务完成的提示
    print("Congratulations! All files processed done.")
    sys.stdout.flush()

except Exception as e:
    print(f"An error has occurred: {e}")
    sys.stdout.flush()
    raise SystemExit(1)
