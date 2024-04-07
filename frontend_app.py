# MIT License

#Copyright (c) [2024] [github\babadue]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



from flask import render_template
from model_initializer import initialize_model
from flask import Flask, request, jsonify
from flask_cors import CORS  
import threading
from Msg_Exchange_Class import Msg_Frontend
import uuid
import json
import socket
import os
import logging

clients = []
client = []

def find_client(clients, ip_address):
    for client in clients:
        if client[0] == ip_address:
            return client            
    return None

def delete_a_client(clients, ip_address):
    for client in clients:
        if client[0] == ip_address:
            my_msg_exchange.send_tensorrtengine(client[1], 'delete session')
            clients.remove(client)
            return

def create_a_client(clients, ip_address, session_id):
    clients.append([ip_address, session_id])
    client=clients[-1]
    return client
    
    

# Shared variable to store the translated text
translated_text = None
event = threading.Event()

def didReceive(json_data):
    global translated_text
    global event
    data = json.loads(json_data)
    text = data['text']
    translated_text = text
    event.set()

my_msg_exchange = Msg_Frontend(callback=didReceive)
communication_thread = threading.Thread(target=my_msg_exchange.start_communication)
communication_thread.start()

def my_t2s(input_text):
    srcLang = 'eng'
    tgtLang = 'eng'
    # process input
    text_inputs = processor(text=f"{input_text}", src_lang=srcLang, return_tensors="pt").to(device)

    # generate translation audio
    audio_array_from_text = model.generate(**text_inputs, tgt_lang=tgtLang)[0].cpu().numpy().squeeze()
    # Set the sample rate
    sample_rate = model.config.sampling_rate
    # sd.play(audio_array_from_text, sample_rate)
    return (audio_array_from_text, sample_rate)


model, processor, device = initialize_model()
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.config['FLASK_ENV'] = 'production'
CORS(app)  

def get_server_ip():
    # Get the IP address of the server
    return socket.gethostbyname(socket.gethostname())

@app.route('/', methods=['GET', 'POST'])
def index():
    client_ip = request.remote_addr
    if request.method == 'GET':
        # reset chat
        delete_a_client(clients, client_ip)
        new_sessionid=str(uuid.uuid4())
        create_a_client(clients, client_ip, new_sessionid)
    # Use render_template to render your index.html file
    ip_address = get_server_ip()
    return render_template('index.html', ip_address=ip_address)

# Route for serving index_lab.html
# @app.route('/index_lab.html')
# def index4():
#     return app.send_static_file('index_lab.html')

@app.route('/t2ai', methods=['POST'])
def t2ai():
    global translated_text
    global event
    input_text = request.json.get('inputText', '')
    client_ip = request.remote_addr
    client = find_client(clients, client_ip)    
    sessionId = client[1]
    my_msg_exchange.send_tensorrtengine(sessionId,input_text)

    # Wait for the translated text to be received by didReceive
    event.wait()
    event.clear()

    processed_text = translated_text
    translated_text = None
    return jsonify({'processedText': processed_text})

@app.route('/t2t', methods=['POST'])
def t2t():
    input_text = request.json.get('inputText', '')
    srcLang = request.json.get('srcLang', '')
    tgtLang = request.json.get('tgtLang', '')
    # process input
    text_inputs = processor(text=f"{input_text}", src_lang=srcLang, return_tensors="pt").to(device)

    # generate translation
    output_tokens = model.generate(**text_inputs, tgt_lang=tgtLang, generate_speech=False)
    translated_text_from_text = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)

    return jsonify({'processedText': translated_text_from_text})
    
@app.route('/t2s', methods=['POST'])
def t2s():
    input_text = request.json.get('inputText', '')
    srcLang = request.json.get('srcLang', '')
    tgtLang = request.json.get('tgtLang', '')
    # process input
    text_inputs = processor(text=f"{input_text}", src_lang=srcLang, return_tensors="pt").to(device)

    # generate translation audio
    audio_array_from_text = model.generate(**text_inputs, speaker_id=8, tgt_lang=tgtLang)[0].cpu().numpy().squeeze()
    # Set the sample rate
    sample_rate = model.config.sampling_rate

    return jsonify({'audioData': audio_array_from_text.tolist(), 'sample_rate': sample_rate})
    
@app.route('/s2t', methods=['POST'])
def s2t():
    global translated_text
    global event
    audio_sample = request.json.get('audioSample', '')
    sample_rate = request.json.get('sampleRate', '')
    tgtLang = request.json.get('tgtLang', '')

    audio_inputs = processor(audios=audio_sample, sampling_rate=sample_rate, return_tensors="pt").to(device)

    output_tokens = model.generate(**audio_inputs, tgt_lang=tgtLang, generate_speech=False)
    translated_text_from_audio = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)

    client_ip = request.remote_addr
    client = find_client(clients, client_ip)    
    sessionId = client[1]
    my_msg_exchange.send_tensorrtengine(sessionId,translated_text_from_audio)

    # Wait for the translated text to be received by didReceive
    event.wait()
    event.clear()
    
    processed_text = translated_text
    translated_text = None
    # print("s2t after audio_inputs b4 return", processed_text)
    audio_array_from_text, sample_rate = my_t2s(processed_text)

    return jsonify({'audioData': audio_array_from_text.tolist(), 'sample_rate': sample_rate})

import os
import socket
import shutil

app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':

    cert_path = os.path.abspath('cert.pem')
    key_path = os.path.abspath('key.pem')

    print("\n" * 2)
    print("Speech engine is ready. You can minimize this window.\n".center(shutil.get_terminal_size().columns))
    print("But do not close it while HomeAI is running.\n".center(shutil.get_terminal_size().columns))
    ip_address = socket.gethostbyname(socket.gethostname())
    print(f"To connect to HomeAI, use this:  https://{ip_address}".center(shutil.get_terminal_size().columns))
    print("\n" * 2)

    app.run(host='0.0.0.0', port=443, ssl_context=(cert_path, key_path), debug=False)



