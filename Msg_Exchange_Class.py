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

import zmq
import json

class Msg_Backend:
    def __init__(self, callback=None):
        self.callback = callback
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.connect("tcp://localhost:6666")
    
    def start_communication(self):
        while True:
            response = self.socket.recv_string()
            if response:
                # print(f"Received response from App2: {response}")
                if self.callback:
                    self.callback(response)

    def send_seamlessengine(self, sessionId, text):
        data = {'sessionId': sessionId, 'text': text}
        json_data = json.dumps(data)
        # print("Sending json_data: ", json_data)
        self.socket.send_string(json_data)

class Msg_Frontend:
    def __init__(self, callback=None):
        self.callback = callback
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        # self.socket.bind("tcp://*:6666")
        self.socket.bind("tcp://127.0.0.1:6666")
    
    def start_communication(self):
        while True:
            response = self.socket.recv_string()
            if response:
                # print(f"Received response from App2: {response}")
                if self.callback:
                    self.callback(response)

    def send_tensorrtengine(self, sessionId, text):
        data = {'sessionId': sessionId, 'text': text}
        json_data = json.dumps(data)
        # print("Sending json_data: ", json_data)
        self.socket.send_string(json_data)