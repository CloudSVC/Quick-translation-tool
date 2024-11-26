import json
import re
import keyboard
import pyperclip
import requests


def contains_english(text):
    # 使用正则表达式匹配英文字符
    pattern = re.compile(r'[a-zA-Z]')
    return bool(pattern.search(text))


def baidu_translate(word):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
    }
    url = "https://fanyi.baidu.com/ait/text/translate"
    if (contains_english(word)):
        data = {
            "query": word,
            "from": "en",
            "to": "zh",
        }
    else:
        data = {
            "query": word,
            "from": "zh",
            "to": "en",
        }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, data=data)

    # 使用 splitlines() 将文本按行分割
    for line in response.text.splitlines():
        if "翻译中" in line:
            json_str = line[6: -1] + "}"
            try:
                data = json.loads(json_str)
                print("原文：" + data['data']['list'][0]['src'])
                print("译文：" + data['data']['list'][0]['dst'])
                print()
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")


def start_keyboard_listener():
    """
    开始键盘监听的回调函数
    """
    # do something
    baidu_translate(pyperclip.paste())


# 注册热键，设置回调函数
keyboard.add_hotkey('Win+C', start_keyboard_listener)

if __name__ == '__main__':
    print("""
                      _   _           
  _ __    _ __     __| | | |_   _   _ 
 | '_ \  | '_ \   / _` | | __| | | | |
 | | | | | | | | | (_| | | |_  | |_| |
 |_| |_| |_| |_|  \__,_|  \__|  \__, |
                                |___/                                                             

ctrl+alt+c 退出程序
win + c 快速翻译                               
    """)
    # 进入监听状态
    # 在主程序中，通过keyboard.wait('ctrl+alt+c')进入监听状态，等待用户按下Ctrl+C来终止程序。
    try:
        keyboard.wait('ctrl+alt+c')
    except KeyboardInterrupt:
        ...
