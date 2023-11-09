import openai
import json
import os
import urllib.request
from pydub import AudioSegment
from playsound import playsound as pl
import requests
import sounddevice as sd
from scipy.io.wavfile import write

## ChatGPT
openai.api_key = API_KEY

# NAVER CLOVA
client_id = API_KEY
client_secret = API_KEY


class Robot():
    memory_size = 100

    with open('./user_value.json', 'r') as f:
        data = json.load(f)
        nameValue = data["user_name"]
        manWomanValue = data["user_value"]

    def set_memory_size(self, memory_size):
        self.memory_size = memory_size

    def gpt_send_anw(self, question: str):
        self.gpt_standard_messages = [{"role": "assistant",
                                   "content": f"You're a assistant robot for senior in USA. Your name is robot. "
                                              f"Your being purpose is support.  So Please answer politely in english and under 5 seconds. "
                                              f"please be a good friend to your patient. "
                                              f"Your patient's name is {self.nameValue} and {self.manWomanValue} is an old person."},
                                      {"role": "user", "content" : question}]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.gpt_standard_messages,
            temperature=0.8
        )

        answer = response['choices'][0]['message']['content']

        self.gpt_standard_messages.append({"role": "user", "content": question})
        self.gpt_standard_messages.append({"role": "assistant", "content": answer})

        return answer


def speaking(anw_text):

    # NAVER CLOVA
    encText = urllib.parse.quote(anw_text)
    data = f"speaker=djoey&volume=0&speed=0&pitch=0&format=mp3&text=" + encText
    urls = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    requests = urllib.request.Request(urls)
    requests.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    requests.add_header("X-NCP-APIGW-API-KEY", client_secret)
    response = urllib.request.urlopen(requests, data=data.encode('utf-8'))
    rescodes = response.getcode()
    if (rescodes == 200):
        response_body = response.read()
        with open('./ResultMP3.mp3', 'wb') as f:
            f.write(response_body)

        # speaker output
        filename = "ResultMP3.mp3"
        dst = "test.wav"
        sound = AudioSegment.from_mp3(filename)
        sound.export(dst, format="wav")

        # data, fs = sf.read(filename, dtype='')
        pl("test.wav")
    else:
        print("404 error")

        # Remove Audio data
        os.remove("ResultMP3.mp3")
        os.remove("test.wav")


def mic(time):


    # Recording Voice
    fs = 44100
    seconds = time

    myRecording = sd.rec(int(seconds * fs), samplerate=fs, channels=4)  # channels는 마이크 장치 번호
    print("recording start")
    # Find mic channel => python -m sounddevice
    sd.wait()
    write('sampleWav.wav', fs, myRecording)

    # Voice To Text
    ## Set
    lang = "Eng"
    url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang

    ## Recorded Voice File
    data_voice = open('sampleWav.wav', 'rb')

    ## headers
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/octet-stream"
    }

    ## VTT Output
    response = requests.post(url, data=data_voice, headers=headers)

    return response


def name_check():
    global common
    common = 0
    with open('./user_value.json', 'r') as f:
        data = json.load(f)
        if data["user_name"] == "":
            speaking("Hello sir. I have no data.so I ask you something.")
            speaking("What's your name?")
            name_ = mic(2)
            speaking(f"Hi! {name_}")
            speaking("What's your gender. please speak he or she.")
            manWoman = mic(2)
            if manWoman == "he":
                manWoman_ = "he"
            elif manWoman == "she":
                manWoman_ = "she"
            else:
                while manWoman != "he" or "she":
                    speaking("I'm sorry. could you repeat please?")
                    manWoman = mic(2)
                    if manWoman == "he":
                        manWoman_ = "he"
                        break
                    elif manWoman == "she":
                        manWoman_ = "she"
                        break
            common = 1
            speaking("Thank you. setting is over")
        else:
            name_ = data["user_name"]
            manWoman_ = data["user_value"]

        write_data = {
            "user_name": f"{name_}",
            "user_value": f"{manWoman_}"
        }

        if common == 1:
            with open('./user_value.json', 'w') as d:
                json.dump(write_data, d)

    return [name_, manWoman_]

def name_ini():
    write_data = {
            "user_name": "",
            "user_value": ""
        }
    with open('./user_value.json', 'w') as d:
                json.dump(write_data, d)

def use_sound(loc):
    pl(loc)