# Gradio 应用默认启动文件为app.py，应用代码相关的文件包含模型推理，应用的前端配置代码
import os
#os.system("mim install mmcv-full")
import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel

# download internlm2 to the base_path directory using git tool
base_path = './BlackHumor'
os.system(f'git clone https://code.openxlab.org.cn/GreyOrigine/BlackHumor.git {base_path}')
os.system(f'cd {base_path} && git lfs pull')

tokenizer = AutoTokenizer.from_pretrained(base_path,trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(base_path,trust_remote_code=True, torch_dtype=torch.float16).cuda()

def chat(message,history):
    for response,history in model.stream_chat(tokenizer,message,history,max_length=2048,top_p=0.7,temperature=1):
        yield response

gr.ChatInterface(chat,
                 title="InternLM2-Chat-7B",
                description="""
InternLM is mainly developed by Shanghai AI Laboratory.  
                 """,
                 ).queue(1).launch()
