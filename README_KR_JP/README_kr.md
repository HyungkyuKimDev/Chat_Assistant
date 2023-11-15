# 언어 선택
<div align="center">
  <a href="https://github.com/HyungkyuKimDev/Chat_Assistant/blob/main/README.md">
    <img src="../img/america_flag.png" alt="Logo" width="80" height="80">
  </a>
    <a href="https://github.com/HyungkyuKimDev/Chat_Assistant/blob/main/README_jp.md">
    <img src="../img/japan_flag.png" alt="Logo" width="80" height="80">
  </a>
    <a href="https://github.com/HyungkyuKimDev/Chat_Assistant/blob/main/README_kr.md">
    <img src="../img/korea_flag.png" alt="Logo" width="80" height="80">
  </a>
</div>

# Chat Assistant

노인을 위한 <b>A Chat Assistant</b>입니다. <b>Python, Wake Word, Naver Clova and ChatGPT 3.5</b>를 사용해 구현하였습니다. 
마이크를 통해 말하신것을 텍스트로 인식합니다. 그런 다음 적절한 답을 만들어 스피커를 통해 출력합니다.  
이것은 당신의 친구가 될 수 있으며, ChatGPT의 프롬포트를 변경하시면, 또 다른 본인만의 chat bot을 만들 수 있습니다. 

## 특징

1. <b>Wake Chat Assistant</b> : "Hey"라고 말하면, 작동합니다.

2. <b>대답 하기</b> : 마이크를 통해 3초간 녹음을 하면, ChatGPT가 해당 음성을 텍스트로 인식합니다.
    - 실행
   ``python
    while response != "":
        response = robot.gpt_send_anw(response)
        ans = response

        speaking(ans)
    ```
3. <b>적절한 대답 생성</b> : ChatGPT를 이용해서 답을 구현합니다. 이후, 그 답을 스피커를 통해 출력합니다. 

4. <b>특별한 기능</b>
   - <b>초기화 기능</b> : "Reset"이라고 말하면, 유저 데이터를 삭제한 뒤, 유저 데이터를 다시 물어봅니다.
   - <b>종료 기능</b> : "Turn off"라고 말하면, 프로세스를 끝냅니다.

    ```python
    if response == "reset":
        speaking("ok. Reset mode")
        name_ini()
    elif response == "turn off":
        speaking("ok. turn off mode")
        return False
   ```
    
 
## 저장

- <b>이 저장소</b>를 git clone 해주세요. 
  ```sh
  git clone https://github.com/HyungkyuKimDev/Chat_Assistant.git
  ```
- 터미널로 <b>requirements.txt</b> 파일을 실행해, 필요한 패키지들을 설치해주세요.
    ```sh
  pip install -r requirements.txt 
  ```


## 사용법


- 디렉터리를 클론하신 곳으로 이동해주세요. 
    ```sh
  cd [The dircetory where you clone]
  ```
- <b>chatbot_voice.py</b>를 python3나 사용하시는 IDE로 실행해주세요.
   ```sh
  python3 chatbot_voice.py
  ```

## Code

### Wake Word
```python
stream = sd.InputStream(
        samplerate=RATE, channels=CHANNELS, dtype='int16')
    stream.start()

    owwModel = Model(
        wakeword_models=["../models/hey.tflite"], inference_framework="tflite")

    n_models = len(owwModel.models.keys())

    # Wake Word 확인을 위한 Main loop 
    while True:
        # audio 데이터 얻기
        audio_data, overflowed = stream.read(CHUNK)
        if overflowed:
            print("Audio buffer has overflowed")

        audio_data = np.frombuffer(audio_data, dtype=np.int16)

        # Feed to openWakeWord model
        prediction = owwModel.predict(audio_data)
        common = False
        # Process prediction results
        for mdl in owwModel.prediction_buffer.keys():
            scores = list(owwModel.prediction_buffer[mdl])
            if scores[-1] > 0.2:  # Wake word 확인시
                print(f"wake word dectected {mdl}!")
                mdl = ""
                scores = [0] * n_models
                audio_data = np.array([])
                common = True
        if common:
            speaking("yes sir!")
```

- Reference : [dscripka/openWakeWord](https://github.com/dscripka/openWakeWord)


### 음성 녹음
```python
def mic(time):
    import requests
    import sounddevice as sd
    from scipy.io.wavfile import write

    # 음성 녹음
    fs = 44100
    seconds = time # 녹음 시간
    
    myRecording = sd.rec(int(seconds * fs), samplerate=fs, channels=4)  # channels는 마이크 장치 번호
    print("recording start")
    # 마이크 장치 채널 찾는 방법 => python -m sounddevice
    sd.wait()
    write('sampleWav.wav', fs, myRecording)

    # 음성을 텍스트로 변환 Naver Cloud : CLOVA Speech Recognition
    ## Set
    lang = "Eng"
    url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
    
    ## 음성 파일 녹음
    data_voice = open('sampleWav.wav', 'rb')

    ## headers
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/octet-stream"
    }

    ## VTT Output
    response = requests.post(url, data=data_voice, headers=headers)

    result_man = str(response.text)
    result = list(result_man)
    count_down = 0
    say_str = []

    for i in range(0, len(result) - 2):
        if count_down == 3:
            say_str.append(result[i])

        if response.text[i] == "\"":
            if count_down == 3:
                break
            else:
                count_down += 1

    anw_str = ''.join(map(str, say_str))

    print(anw_str)

    return anw_str
```
- Reference : [Naver Cloud : CLOVA Speech Recognition](https://api.ncloud-docs.com/docs/ai-naver-clovaspeechrecognition)
<br></br>
### 스피커 사용해 오디오 출력
```python
def speaking(anw_text):

    # NAVER CLOVA : CLOVA Voice
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

        # 스피커 출력
        filename = "ResultMP3.mp3"
        dst = "test.wav"
        sound = AudioSegment.from_mp3(filename)
        sound.export(dst, format="wav")

        # data, fs = sf.read(filename, dtype='')
        pl("test.wav")
    else:
        print("404 error")

        # 오디오 데이터 삭제
        os.remove("ResultMP3.mp3")
        os.remove("test.wav")
```
- Reference : [NAVER CLOVA : CLOVA Voice](https://api.ncloud-docs.com/docs/ai-naver-clovavoice-ttspremium)

<br></br>
### OpenAI 이용해, 대답 구하기

```python
class Robot():
    memory_size = 100

    with open('../user_value.json', 'r') as f:
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
                                      {"role": "user", "content": question}]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.gpt_standard_messages,
            temperature=0.8
        )

        answer = response['choices'][0]['message']['content']

        self.gpt_standard_messages.append({"role": "user", "content": question})
        self.gpt_standard_messages.append({"role": "assistant", "content": answer})

        return answer
```

## 연락처

김형규
- hyungkyukimdev@gmail.com
- [Linkedein](https://www.linkedin.com/in/hyung-gyu-kim-202b991b8/)
- [Blog](https://honoluulu-life.tistory.com/)

프로젝트 링크: [HyungkyuKimDev/Chat_Assistant](HyungkyuKimDev/Chat_Assistant)

## Thanks to
[Topasm](https://github.com/Topasm) 
- Wake Word 부분 개발
- Robot Engineer