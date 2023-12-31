# 言語の選択
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

老人のための<b>A Chat Assistant</b>です。 <b>Python, Naver Clova, Wake Word また ChatGPT 3.5</b>を利用し作りました。
マイクで話したのをテキストで認識します。その後、答えを作りスピーカでその答えを出力します。
これはあなたの友達になれますし、ChatGPTのPromptを変更すると。また、自分のChat　Botを作れます。

## 特徴

1. <b>Wake Chat Assistant</b> : あなたが”Hey＂と言うと、策動します。

2. <b>答え</b> : マイクで３秒間録音すると、ChatGPTが録音をテキストで認識します。 
    - 実行
   ```python
    while response != "":
        response = robot.gpt_send_anw(response)
        ans = response

        speaking(ans)
    ```
3. <b>答えの作り</b> : ChatGPTを利用し、答えを作ります。また、その答えをスピーカーで出力します。

4. <b>特別な機能</b>
   - <b>データの削除機能</b> : "Reset"と言うとユーザのデータを消した後、ユーザのデータを聞きます。
   - <b>終了機能</b> : "Turn off"と言うと、プロセスを終了します。

    ```python
    if response == "reset":
        speaking("ok. Reset mode")
        name_ini()
    elif response == "turn off":
        speaking("ok. turn off mode")
        return False
   ```
    
 
## 保存

- <b>このrepository</b>をgit cloneしてください。
  ```sh
  git clone https://github.com/HyungkyuKimDev/Chat_Assistant.git
  ```
- Terminalで<b>requirements.txt</b>のファイルを実行し、必要なPackageを設置してください。
    ```sh
  pip install -r requirements.txt 
  ```


## 使い方


- 位置をCloneしたところに移動してください。
    ```sh
  cd [The dircetory where you clone]
  ```
- <b>chatbot_voice.py</b>をpython3とか利用するIDEで実行してください。
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

    # Main　繰り返し、WakeWordの確認のため
    while True:
        # オーディオデータを探し
        audio_data, overflowed = stream.read(CHUNK)
        if overflowed:
            print("Audio buffer has overflowed")

        audio_data = np.frombuffer(audio_data, dtype=np.int16)


        prediction = owwModel.predict(audio_data)
        common = False

        for mdl in owwModel.prediction_buffer.keys():
            scores = list(owwModel.prediction_buffer[mdl])
            if scores[-1] > 0.2:  # もし探すと
                print(f"wake word dectected {mdl}!")
                mdl = ""
                scores = [0] * n_models
                audio_data = np.array([])
                common = True
        if common:
            speaking("yes sir!")
```

- 参考 : [dscripka/openWakeWord](https://github.com/dscripka/openWakeWord)

### 音声録音
```python
def mic(time):
    import requests
    import sounddevice as sd
    from scipy.io.wavfile import write

    # 音声録音
    fs = 44100
    seconds = time # 録音時間
    
    myRecording = sd.rec(int(seconds * fs), samplerate=fs, channels=4)  # channels는 마이크 장치 번호
    print("recording start")
    # マイクのチャネルを探し方 => python -m sounddevice
    sd.wait()
    write('sampleWav.wav', fs, myRecording)

    # 音声をテキストで変更 Naver Cloud : CLOVA Speech Recognition
    ## Set
    lang = "Eng"
    url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
    
    ## 音声を録音
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
- 参考 : [Naver Cloud : CLOVA Speech Recognition](https://api.ncloud-docs.com/docs/ai-naver-clovaspeechrecognition)
<br></br>
### スピーカーを利用し、オーディオデータの出力
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
        with open('./ResultMP3.mp3', 'wb') asオ f:
            f.write(response_body)

        # スピーカーの出力
        filename = "ResultMP3.mp3"
        dst = "test.wav"
        sound = AudioSegment.from_mp3(filename)
        sound.export(dst, format="wav")

        # data, fs = sf.read(filename, dtype='')
        pl("test.wav")
    else:
        print("404 error")

        # オーディオデータの削除
        os.remove("ResultMP3.mp3")
        os.remove("test.wav")
```
- 参考 : [NAVER CLOVA : CLOVA Voice](https://api.ncloud-docs.com/docs/ai-naver-clovavoice-ttspremium)

<br></br>
### OpenAIを利用し,答えを作り

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

## 連絡先

キム・ヒョンギュ
- hyungkyukimdev@gmail.com
- [Linkedein](https://www.linkedin.com/in/hyung-gyu-kim-202b991b8/)
- [Blog](https://honoluulu-life.tistory.com/)

プロジェクトのリンク: [HyungkyuKimDev/Chat_Assistant](HyungkyuKimDev/Chat_Assistant)

## Thanks to
[Topasm](https://github.com/Topasm) 
- Wake Word Part developed 
- Robot Engineer