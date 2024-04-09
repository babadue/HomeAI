# <div align="center">HomeAI</div>

## Description:

This software project is derived from NVIDIA's Chat with RTX. I recently installed and 
tried out this NVIDIA package. To my surprise, it is quite capable of running on a 
single GPU, such as the RTX 3060 GPU on my PC machine. Unfortunately, the demo 
software doesn't have the capability of continuing the conversation. That gave me the 
idea to create a project that allows the chatbot to carry on a continuation conversation. 

This project will go beyond to facilitate a continuous conversation of Chat with RTX. It will use the TensorRT-LLM engine with Mistral model that Chat with RTX app installed on your PC. The features will include voice interaction and more. You can interact with your own private AI in your home. The interactions can be done via text or voice and through other PCs or mobile devices. More importantly, the term 'What happens in Vegas, stays in Vegas' applies. All interactions will stay within your own PC running this project software. No data will travel out to the internet. Once the software is installed, no internet connection is required.  The role of the AI can be customized - up to certain extent.  And the chatbot can hold multiple concurrent chat conversations.  

Use cases for this project include education, home entertainment, family fun-time, etc.

## Procedure:

1. &nbsp; Install NVIDIA's [Chat with RTX](https://www.nvidia.com/en-us/ai-on-rtx/chat-with-rtx-generative-ai/) to get the TensorRT-LLM engine with Mistral model installed on your PC.

2. &nbsp; Clone this respository.

3. &nbsp; In the cloned folder on your PC, starting the installation by double-click on the `install.bat`.  The installation process will take about 10 minutes depending on your internet connection speed.  Once finished, the installation window will automatically close and you should see an icon on your Desktop with HomeAI ![ ](homeai.png "Optional title").

4. &nbsp; The `config.json` file in `config` folder is where you can customize the role.  It is under `strings` section and `my_sys_cmd` key.

* You can run uninstall.bat to uninstall HomeAI.

* To update HomeAI with the new update, run update.bat.

## System Requirements:

* Same as NVIDIA's [Chat with RTX](https://www.nvidia.com/en-us/ai-on-rtx/chat-with-rtx-generative-ai/) .

* HomeAI also uses a second LLM model - SeamlessM4T-v2.  While this model can be run without a GPU, but performance is 
greatly improved if it can access the GPU. It can share the same GPU with the Mistral model.

* If you already have a GPU version with 8GB, then that will be fine. But if you are planning to acquire the hardware, I would recommend that you get the one above 8GB. If you are budget conscious, the RTX 3060 is excellent choice since it has 12GB. I develop my project using this GPU.

## About security:

The project is intended for home use. During the installation process, it will generate the necessary components for SSL using a self-signed certificate. SSL is needed because modern browsers require it to allow access to the microphone from a web page. When you first visit the HomeAI page, you will receive a warning about an unsecured page. You can safely proceed to access it.

There are other components in the project that were also designed with home usage in mind.  Therefore, if you are planning to use this in an office environment, you need to take this into consideration and make modifications where needed.

## Contributors:

ChatGPT-3.5 the coding machine - Without it, this project would probably take much longer to complete!

## Project Attribution:
https://www.nvidia.com/en-us/ai-on-rtx/chat-with-rtx-generative-ai/

## Disclaimer:

This project is provided "as is" and without any warranty. Use it at your own risk. 
    
https://github.com/babadue/HomeAI/assets/116512015/f1c40096-b8fd-4555-a566-186d4bda2827

https://github.com/babadue/HomeAI/assets/116512015/bc9d7484-af37-4d22-914d-35fce506bc14



