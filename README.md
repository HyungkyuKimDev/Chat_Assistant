# Language Select
<div align="center">
    <a href="https://github.com/HyungkyuKimDev/Chat_Assistant/blob/main/README.md">
        <img src="img/america_flag.png" alt="Logo" width="80" height="80">
    </a>
        <a href="https://github.com/HyungkyuKimDev/Chat_Assistant/blob/main/README_KR_JP/README_jp.md">
        <img src="img/japan_flag.png" alt="Logo" width="80" height="80">
    </a>
        <a href="https://github.com/HyungkyuKimDev/Chat_Assistant/blob/main/README_KR_JP/README_kr.md">
        <img src="img/korea_flag.png" alt="Logo" width="80" height="80">
    </a>
</div>


# Chat Assistant

<b>A Chat Assistant</b> for senior. Using <b>Python, Naver Clova, Wake Word and ChatGPT 3.5</b>  
It can understand what you say on Mic. And answer like a human on Speaker.   
It can be your friend. And If you want to change ChatGPT's prompt, then you can make other Chat Assistant easily.

## Features

1. <b>Wake Chat Assistant</b> : If you say "Hey", then It works using.


2. <b>Talk Something</b> : After saying "Hey", Say anything on Mic within 3 secs, The Chat Assistant understand what you said.
    - Execute
   ```python
    while response != "":
        response = robot.gpt_send_anw(response)
        ans = response

        speaking(ans)
    ```
3. <b>Make Answer properly</b> : It is going to make answer something using ChatGPT. And speak out using Speaker. 

4. <b>Special Function</b>
   - <b>Reset</b> : If you say "Reset", Then It remove the user's data. And ask you about new user's data.
   - <b>Turn off</b> : If you say "Turn off", Then It quit the process.

    ```python
    if response == "reset":
        speaking("ok. Reset mode")
        name_ini()
    elif response == "turn off":
        speaking("ok. turn off mode")
        return False
   ```
    
 
## Setup

- Clone <b>this Repository</b> on your PC. 
  ```sh
  git clone https://github.com/HyungkyuKimDev/Chat_Assistant.git
  ```
- Install <b>requirements.txt</b> file on your Terminal.
    ```sh
  pip install -r requirements.txt 
  ```


## Usage


- change Directory to The directory where you clone This Repository.
    ```sh
  cd [The dircetory where you clone]
  ```
- execute <b>chatbot_voice.py</b>
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

    # Main loop for wake word detection
    while True:
        # Get audio
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
            if scores[-1] > 0.2:  # Wake word detected
                print(f"wake word dectected {mdl}!")
                mdl = ""
                scores = [0] * n_models
                audio_data = np.array([])
                common = True
        if common:
            speaking("yes sir!")
```

- Reference : [dscripka/openWakeWord](https://github.com/dscripka/openWakeWord)

### Recording voice
```python
def mic(time):
    import requests
    import sounddevice as sd
    from scipy.io.wavfile import write

    # Recording Voice
    fs = 44100
    seconds = time # time for recording
    
    myRecording = sd.rec(int(seconds * fs), samplerate=fs, channels=4)  # channels는 마이크 장치 번호
    print("recording start")
    # Find mic channel => python -m sounddevice
    sd.wait()
    write('sampleWav.wav', fs, myRecording)

    # Voice To Text Using Naver Cloud : CLOVA Speech Recognition
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
### Use Speaker
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
```
- Reference : [NAVER CLOVA : CLOVA Voice](https://api.ncloud-docs.com/docs/ai-naver-clovavoice-ttspremium)

<br></br>
### Make an Answer Using OpenAI
```python
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
```

## Contact

Hyungkyu Kim 
- hyungkyukimdev@gmail.com
- [Linkedein](https://www.linkedin.com/in/hyung-gyu-kim-202b991b8/)
- [Blog](https://honoluulu-life.tistory.com/)

Project Link: [HyungkyuKimDev/Chat_Assistant](HyungkyuKimDev/Chat_Assistant)

## Thanks to
[Topasm](https://github.com/Topasm) 
- Wake Word Part developed 
- Robot Engineer