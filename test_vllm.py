from openai import OpenAI
from vllm import LLM, SamplingParams

# 设置 OpenAI 的 API key 和 API base，以使用 vLLM 的 API 服务器
openai_api_key = "token-abc123"
# openai_api_base = "http://localhost:8081/v1"
openai_api_base = "http://localhost:8082/v1"

# "messages": [
# {"role": "system", "content": "You are a helpful assistant."},
# {"role": "user", "content": "Who won the world series in 2020?"}

def get_message_chatgpt(inputs):
    return [{"role": "system", "content": "You are a helpful assistant."},{"role": "user","content": inputs}]

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# 询问大模型 "一加一等于多少"
# question = "一加一等于多少"
question="""
假设你是一名优秀的翻译人员，现在给你一个json格式的文件，需要你做如下操作：
0.翻译要求直译，保留完整的语义、逻辑结构，措辞恰当。回答只要json，不要其他多余的话。
1.json中的字段保持原本的样子，比如 "arguments"保留作为key不翻译。
2.将"text"字段中的英文句子翻译成中文
3."event_trigger"字段内容翻译成中文，要与"text"字段中对应的中文保持一致，
4."event_type"字段内容翻译成中文
5."argument"字段内容翻译成中文，要与"text"字段中对应的中文保持一致，
6."role"字段内容翻译成中文
内容如下：{"text": "An email scam passing as a Netflix notification has been targeting subscribers of the streaming service .", "event": [{"event_trigger": "email scam", "event_type": "phishing", "trigger_pos": [], "arguments": [{"argument": "a Netflix notification", "role": "trusted entity", "argument_pos": []}, {"argument": "the streaming service", "role": "trusted entity", "argument_pos": []}, {"argument": "subscribers", "role": "victim", "argument_pos": []}]}], "task": "EE"}

"""
# question="请帮我生成一个500字的玄幻小说，以李白在东京为原型"


# 创建完成请求
completion = client.chat.completions.create(
    # model="/ai/teacher/ytw/plm/Qwen2-7B-Instruct",
    model="qwen15-14b-chat",
    # model="/data/technode/pretrained_models/qwen1.5_14b_sft_full_v961_sharegpt_490k_z3",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question},
    ],
    # prompt=get_message_chatgpt(question),
    # max_model_len=2048,
    max_tokens=512,  # 设置返回结果的最大 token 数
    temperature=0.5  # 设置生成的温度，控制生成内容的多样性
)

# 打印完成结果
print("Completion result:\n", completion)
print("Completion result:\n", completion.choices[0].message.content)
# Completion(id='cmpl-ac9b291ee58d40eaba6579d61ef9d2e1', choices=[CompletionChoice(finish_reason='length', index=0, logprobs=None, text='？ 一加一等于二。这是基本的数学加法，表示两个数量合并后得到的结果是两个数之和。\n\n如果需要更详细的解释，加法是一种基本的数学运算，用来表示两个或多个数值的总和。在数学中，加法通常表示为两个数之间使用加号（+）连接，例如在这个例子中，"一加一" 表示的是数字1（一）和数字1（一）相加。', stop_reason=None)], created=1720422441, model='/data/technode/pretrained_models/Qwen2-7B-Instruct', object='text_completion', system_fingerprint=None, usage=CompletionUsage(completion_tokens=100, prompt_tokens=5, total_tokens=105))
