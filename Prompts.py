"""

构建promot


"""



Academic_EE_Prompts = """假设你是一名优秀的翻译人员，现在给你一个json格式的文件，需要你做如下操作：
0.翻译要求直译，保留完整的语义、逻辑结构，措辞恰当。回答只要json，不要其他多余的话。
1.json中的字段保持原本的样子，比如 "arguments"保留作为key不翻译。
2.将"text"字段中的英文句子翻译成中文
3."event_trigger"字段内容翻译成中文，要与"text"字段中对应的中文保持一致，
4."event_type"字段内容翻译成中文
5."argument"字段内容翻译成中文，要与"text"字段中对应的中文保持一致，
6."role"字段内容翻译成中文
内容如下：@@@@@@@@@@
"""
Academic_NER_Prompts=""""""
Academic_RE_Prompts=""""""
Academic_EC_Prompts=""""""