# afk-macro
Paste in your paragraph and it will auto type it in for you at your chosen wpm 
Dependecies:
pyautgui
string
threading
tkinter
time

use this for packaging

python -m pip install pyautogui
python -m pip install pyinstaller
python -m PyInstaller 
pyinstaller --onefile --noconsole --clean --icon=autotype.ico ai_main.py
