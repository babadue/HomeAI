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

from transformers import SeamlessM4Tv2Model, AutoProcessor
import os

model_path = "facebook/seamless-m4t-v2-large"

user_profile = os.getenv('USERPROFILE')
print('user_profile : ', user_profile)

local_model_path = os.path.join(user_profile, r'HomeAI\models\seamless-m4t-v2-large')
print('local_model_path:  ', local_model_path)

if not os.path.exists(local_model_path):
    os.makedirs(local_model_path)

processor = AutoProcessor.from_pretrained(model_path)
processor.save_pretrained(local_model_path)
model = SeamlessM4Tv2Model.from_pretrained(model_path)
model.save_pretrained(local_model_path)

