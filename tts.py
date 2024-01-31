# coding=utf-8
import os
import json
import datetime
import re
import wave

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv(verbose=True)

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
PER = 4178
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 6

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
FORMAT = FORMATS[AUE]

CUID = "123456PYTHON"

TTS_URL = "http://tsn.baidu.com/text2audio"


class TTSError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = "http://aip.baidubce.com/oauth/2.0/token"
SCOPE = "audio_tts_post"  # 有此scope表示有tts能力，没有请在网页里勾选


def fetch_token():
    # print("fetch token begin")
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY,
    }
    post_data = urlencode(params)
    post_data = post_data.encode("utf-8")
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print("token http response http code : " + str(err.code))
        result_str = err.read()

    result_str = result_str.decode()

    # print(result_str)
    result = json.loads(result_str)
    # print("result: ", result)
    if "access_token" in result.keys() and "scope" in result.keys():
        if not SCOPE in result["scope"].split(" "):
            raise TTSError("scope is not correct")
        print(
            "SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s"
            % (result["access_token"], result["expires_in"])
        )
        return result["access_token"]
    else:
        raise TTSError(
            "MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response"
        )


"""  TOKEN end """


def new_file():
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%Y-%m-%d_%H-%M-%S") + "." + FORMAT


def text_to_audio(text):
    token = fetch_token()
    tex = quote_plus(text)  # 此处TEXT需要两次urlencode
    # print(tex)
    params = {
        "tok": token,
        "tex": tex,
        "per": PER,
        "spd": SPD,
        "pit": PIT,
        "vol": VOL,
        "aue": AUE,
        "cuid": CUID,
        "lan": "zh",
        "ctp": 1,
    }  # lan ctp 固定参数

    data = urlencode(params)
    # print(data)
    # print("test on Web Browser" + TTS_URL + "?" + data)

    req = Request(TTS_URL, data.encode("utf-8"))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()

        headers = dict((name.lower(), value) for name, value in f.headers.items())

        has_error = (
            "content-type" not in headers.keys()
            or headers["content-type"].find("audio/") < 0
        )
    except URLError as err:
        print("asr http response http code : " + str(err.code))
        result_str = err.read()
        has_error = True

    out_file = new_file()
    save_file = "error.txt" if has_error else out_file
    with open(save_file, "wb") as of:
        of.write(result_str)

    if has_error:
        result_str = str(result_str, "utf-8")
        print("tts api error:" + result_str)

    print("result saved as :" + save_file)

    return out_file


def read_text(input):
    with open(input, "r") as file:
        text = file.read()
    return text


def split_text(text):
    # 使用正则表达式来匹配句子
    sentences = re.split("。", text)

    # 初始化一个空列表来存储分割后的文本
    segmented_text = []

    # 初始化一个空字符串来存储当前分组的文本
    current_group = ""

    # 遍历每个句子
    for sentence in sentences:
        # 如果当前分组的长度加上当前句子的长度小于等于300，则将当前句子加入当前分组
        if len(current_group) + len(sentence) <= 300:
            current_group += sentence + "。"  # 添加句号以保持句子完整
        else:
            # 如果当前分组的长度加上当前句子的长度大于300，则将当前分组加入分割后的文本列表，并重新开始一个新的分组
            segmented_text.append(current_group)
            current_group = sentence + "。"  # 添加句号以保持句子完整

    # 将最后一个分组加入分割后的文本列表
    segmented_text.append(current_group)

    return segmented_text

def merge_audio(aud_files, merged_aud_file):
    data = []
    for file in aud_files:
        w = wave.open(file, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

    output = wave.open(merged_aud_file, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()


if __name__ == "__main__":
    segments = split_text(read_text("input.txt"))

    # 输出 audio 文件集合
    aud_files = []
    for seg_text in segments:
        # print(seg_text)
        aud_file = text_to_audio(seg_text)
        aud_files.append(aud_file)

    merged_aud_file = new_file()
    merge_audio(aud_files, merged_aud_file)

    print("audio file: " + merged_aud_file)
