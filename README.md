# Chat Assistant

<b>A Chat Assistant</b> for senior. Using <b>Python, Naver Clova and ChatGPT 3.5</b>  
It can understand what you say on Mic. And answer like a human on Speaker.   
It can be your friend. And If you want to change ChatGPT's prompt, then you can make other Chat Assistant easily.

## Features

1. <b>Wake Chat Assistant</b> : If you call "Robot" within 2 secs, then It works using.
    - Execute
        ```python
      robot = Robot()

        # Communication start
        response = mic(2)
        if response == "":
            call_num += 1
            print(call_num)
        if call_num == 3:
            speaking("Please call me Robot!")
            call_num = 0
        if response == "robot":
            speaking("yes sir!")
            response = mic(3)
        ```
2. <b>Talk Something</b> : Say anything on Mic within 3 secs, The Chat Assistant understand what you said.
    - Execute
   ```python
    while response != "":
        response_ = robot.gpt_send_anw(response)
        emotion = response_[0]
        ans = response_[1]

        speaking(ans)
    os.remove("sampleWav.wav")    
    ```
3. <b>Make Answer properly</b> : It is going to make answer something using ChatGPT. And speak out using Speaker. 

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

### Recording voice.
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

    return response
```
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



## Demo

---