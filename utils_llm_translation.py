
"""
针对英文数据集进行保留原始数据结构、任务标签等形势下翻译成为中文数据集

要求：
TODO:1.语句翻译成中文，且label保持不变，比如实体抽取任务下，实体翻译成中文必须在句子对应的实体范围内
2.保留原始数据结构，比如原始数据集中有多个句子，每个句子有多个实体，翻译后的句子也要有对应的实体范围


prompt范例

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


from openai import OpenAI
import os,json
from tqdm import tqdm
import time
from datetime import datetime
import random
import re
from Prompts import *



def get_message_chatgpt(inputs):
    return [{"role": "system", "content": "You are a helpful assistant."},{"role": "user","content": inputs}]


def get_vllm(query, model_type='qwen1.5-14b-chat'):
        
    # 设置 OpenAI 的 API key 和 API base，以使用 vLLM 的 API 服务器
    openai_api_key = "token-abc123"
    
    # 
    model_trans={
        'qwen2-7b-instruct':["/ai/teacher/ytw/plm/Qwen2-7B-Instruct","http://localhost:8081/v1"],
        'qwen1.5-14b-chat':["qwen15-14b-chat","http://localhost:8082/v1"],
    }
    
    model_name,openai_api_base=model_trans[model_type]
    
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )
        
    if not isinstance(query,str):
        query=str(query)
    
    completion = client.chat.completions.create(
        model=model_name,
        # model="/data/technode/pretrained_models/qwen1.5_14b_sft_full_v961_sharegpt_490k_z3",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ],
        temperature= 0.3,
        top_p= 0.85,
        max_tokens= 1024,
    )    
    # print("in get vllm:",completion.choices[0].message.content)
    return completion.choices[0].message.content

def subop_read_instructdata_zh(datapath):
    try:
        with open(datapath, 'r', encoding='utf-8') as file:
            data = [json.loads(line) for line in file]
    except:
        print("try another parse")
        data = []
        with open(datapath, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                data.append(eval(line))
    return data

def write_file(results,path):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            for dictionary in results:
                json.dump(dictionary, file, ensure_ascii=False)
                file.write('\n')
        # print("write in ", path)
    except:
        print("write error ",path)

# 主要接口
def processingInstruction(data):
    result=[]
    for item in tqdm(data):
        cur_json = get_vllm(Academic_EE_Prompts.replace("@@@@@@@@@@",str(item)),'qwen2-7b-instruct')
        result.append(cur_json)
    return result
    
# 0_定义路径等变量
source_dir="/ai/teacher/ytw/down_mirror/iepile/IE-en/EE"
target_dir="/ai/teacher/ytw/processed_data/iepile/IE-en/EE"

## 没有target_dir文件创建文件夹
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
    

# 1_读取原始数据集
## 读取source_dir所有的文件夹名
folders=os.listdir(source_dir)

# 读取每个文件夹下所有文件名
for folder in folders:
    dir_time=time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    start_time=datetime.now()
    dir_samples=0
    
    ## 判定folder是否是文件夹
    if not os.path.isdir(os.path.join(source_dir,folder)):
        continue
    ## 读取每个文件夹下所有文件名
    files=os.listdir(os.path.join(source_dir,folder))
    for file in files:
        if file in ['dev.json','train.json','test.json']:                
            # 读取每个文件
            print(os.path.join(source_dir,folder,file))
            data=subop_read_instructdata_zh(os.path.join(source_dir,folder,file))   
        else:
            continue
        if len(data)==0:
            continue
        
        cur_json=processingInstruction(data)
        
        dir_samples+=len(cur_json)
        
        # # 翻译text字段
        # text_zh=get_vllm(data['text'])
        # # 翻译event_trigger字段
        # event_trigger_zh=get_vllm(data['event'][0]['event_trigger'])
        # # 翻译event_type字段
        # event_type_zh=get_vllm(data['event'][0]['event_type'])
        # # 翻译argument字段
        # argument_zh=[]
        # for argument in data['event'][0]['arguments']:
        #     argument_zh.append(get_vllm(argument['argument']))
        # # 翻译role字段
        # role_zh=[]
        # for role in data['event'][0]['arguments']:
        #     role_zh.append(get_vllm(role['role']))
        # 构造新的json数据
        # new_data={
        #     'text':text_zh,
        #     'event':[{
        #         'event_trigger':event_trigger_zh,
        #         'event_type':event_type_zh,
        #         'arguments':[{
        #             'argument':argument_zh[i],
        #             'role':role_zh[i]
        #         } for i in range(len(argument_zh))]
        #     }]
        # }
        # 写入文件
        print(os.path.join(target_dir,folder,file))
        cur_save = os.path.join(target_dir,folder)
        if not os.path.exists(cur_save):
            os.makedirs(cur_save)
        write_file(cur_json, os.path.join(cur_save,file))
    
    print("folder:",folder,"samples:",dir_samples,"start_time",dir_time,"time_cost:",datetime.now()-start_time)    
