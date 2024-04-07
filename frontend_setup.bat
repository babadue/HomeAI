:: SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
:: SPDX-License-Identifier: MIT
::
:: Permission is hereby granted, free of charge, to any person obtaining a
:: copy of this software and associated documentation files (the "Software"),
:: to deal in the Software without restriction, including without limitation
:: the rights to use, copy, modify, merge, publish, distribute, sublicense,
:: and/or sell copies of the Software, and to permit persons to whom the
:: Software is furnished to do so, subject to the following conditions:
::
:: The above copyright notice and this permission notice shall be included in
:: all copies or substantial portions of the Software.
::
:: THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
:: IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
:: FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
:: THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
:: LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
:: FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
:: DEALINGS IN THE SOFTWARE.

:: ******************************************************************
:: Note that majority of the code in this file is derived from Chat with RTX's app_launch.bat.
:: The above copyright text is retained for record.

@echo off
setlocal enabledelayedexpansion
set "env_path_found="

for /f "tokens=1,* delims= " %%a in ('"%programdata%\MiniConda\Scripts\conda.exe" env list') do (
    set "env_name=%%a"
    set "env_path=%%b"
    if "!env_path!"=="" (
        set "env_path=!env_name!"
    )
    echo !env_path! | findstr /C:"env_home_ai" > nul
    if !errorlevel! equ 0 (
        set "env_path_found=!env_path!"
        goto :endfor
    )
)

:endfor
if not "%env_path_found%"=="" (
    echo Environment path found: %env_path_found%
    call "%programdata%\MiniConda\Scripts\activate.bat" "%USERPROFILE%\HomeAI\env_home_ai"
    python --version
) else (
    echo Environment with 'env_home_ai' not found.  so install
    call "%programdata%\MiniConda\Scripts\conda.exe" create --prefix "%USERPROFILE%\HomeAI\env_home_ai" python=3.10.14 -y
    call "%programdata%\MiniConda\Scripts\activate.bat" "%USERPROFILE%\HomeAI\env_home_ai"
    pip install flask==3.0.2
    pip install flask_cors==4.0.0
    pip install requests==2.31.0
    pip install transformers==4.39.3
    pip install protobuf==5.26.1
    pip install zmq
    pip install sentencepiece==0.2.0
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    python download_model.py
    python --version

)

endlocal

