# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# ******************************************************************
# Note that majority of the code in this file is derived from Chat with RTX's app.py.
# The above copyright text is retained for record.

import os
import sys
local_app_data = os.getenv('LOCALAPPDATA')
path_to_module = os.path.join(local_app_data, r'NVIDIA\ChatWithRTX\RAG\trt-llm-rag-windows-main')

# Add the directory to the Python path
sys.path.append(path_to_module)

import json
from pathlib import Path
from trt_llama_api import TrtLlmAPI
from collections import defaultdict
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt

model_config_file = 'config\\config.json'

my_lists=[]  # list of instances of  chat sessions
myChatHistory=[]
my_chat_history=None

def read_config(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except json.JSONDecodeError:
        print(f"There was an error decoding the JSON from the file {file_name}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def get_model_config(config, model_name=None):
    models = config["models"]["supported"]
    selected_model = next((model for model in models if model["name"] == model_name), models[0])
    user_profile = os.getenv('LOCALAPPDATA')
    path_to_module = os.path.join(user_profile, r'NVIDIA\ChatWithRTX\RAG\trt-llm-rag-windows-main')
    my_model_path = os.path.join(path_to_module, selected_model["metadata"]["model_path"])
    my_tokenizer_path = os.path.join(path_to_module, selected_model["metadata"]["tokenizer_path"])

    return {
        # "model_path": os.path.join(os.getcwd(), selected_model["metadata"]["model_path"]),
        "model_path": my_model_path,      
        "engine": selected_model["metadata"]["engine"],
        "tokenizer_path": my_tokenizer_path,
        "max_new_tokens": selected_model["metadata"]["max_new_tokens"],
        "max_input_token": selected_model["metadata"]["max_input_token"],
        "temperature": selected_model["metadata"]["temperature"]
    }


# read model specific config
selected_model_name = None
# selected_data_directory = None
config = read_config(model_config_file)

if selected_model_name == None:
    selected_model_name = config["models"].get("selected")

model_config = get_model_config(config, selected_model_name)
trt_engine_path = model_config["model_path"]
trt_engine_name = model_config["engine"]
tokenizer_dir_path = model_config["tokenizer_path"]

# create trt_llm engine object
llm = TrtLlmAPI(
    model_path=model_config["model_path"],
    engine_name=model_config["engine"],
    tokenizer_dir=model_config["tokenizer_path"],
    temperature=model_config["temperature"],
    max_new_tokens=model_config["max_new_tokens"],
    context_window=model_config["max_input_token"],
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=False
)


# chat function to trigger inference
def call_llm_streamed(sessionId, query):
    partial_response = ""
    response = llm.stream_complete(query)
    for token in response:
        partial_response += token.delta

    return (sessionId, partial_response)

# convert history list to chat format per mistral instruct model
def apply_chat_template(chat):
    formatted_chat = ""
    for item in chat:
        question = item[0]
        answer = item[1] if item[1] is not None else ""
        formatted_chat += f"<s> [INST] {question} [/INST]{answer}</s> "
    return formatted_chat.strip()


#     # call garbage collector after inference
#     torch.cuda.empty_cache()
#     gc.collect()

#     global llm, service_context, embed_model, faiss_storage, engine
#     import gc
#     if llm is not None:
#         llm.unload_model()
#         del llm
#     # Force a garbage collection cycle
#     gc.collect()

# call garbage collector after inference
# torch.cuda.empty_cache()
# gc.collect()


def my_stream_chatbot(query, client):
    sessionId=client[0]
    client_history=client[1]
    history_str=apply_chat_template(client_history)
    client_history.append([query, None])  # Add the first query with no response

    # my custom code 
    sys_cmd=config["strings"].get("my_sys_cmd")
    new_query=f"""<s> [INST] {query} [/INST]  </s>"""
    query=sys_cmd + history_str + new_query

    response_data = call_llm_streamed(sessionId, query)
    response = response_data[1]
    client_history[-1][1] = response
    my_msg_exchange.send_seamlessengine(sessionId,response)


import threading
from Msg_Exchange_Class import Msg_Backend

def find_client(clients, sessionId):
    for client in clients:
        if client[0] == sessionId:
            return client
    return None

def delete_a_client(clients, sessionId):
    for client in clients:
        if client[0] == sessionId:
            clients.remove(client)
            return

def create_a_client(clients, sessionId):
    clients.append([sessionId, []])
    client=clients[-1]
    return client


def didReceive(json_data):
    data = json.loads(json_data)
    sessionId = data['sessionId']
    text = data['text']
    if text=='delete session':
        # deleting the requested session
        delete_a_client(my_lists, sessionId)
    else:
        client=find_client(my_lists, sessionId)
        if client==None:
            client=create_a_client(my_lists, sessionId)       
        my_stream_chatbot(text, client)

my_msg_exchange = Msg_Backend(callback=didReceive)
communication_thread = threading.Thread(target=my_msg_exchange.start_communication)
communication_thread.start()

import shutil
print("\n" * 2)
print("Mistral engine is ready. You can minimize this window.\n".center(shutil.get_terminal_size().columns))
print("But do not close it while HomeAI is running.\n".center(shutil.get_terminal_size().columns))


    





