@echo off 
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install pywin32
pip install pynput
pip install scipy
python3 -m pip install sounddevice
pip install pillow
nssm install "monitoring" "C:\Users\ysudh\AppData\Local\Programs\Python\Python310\python.exe" "C:\Users\ysudh\Monitoring_Tool.py"