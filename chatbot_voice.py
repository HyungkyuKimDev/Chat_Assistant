import os

from Chat.voiceChat import *

call_num = 0
while 1:
    name_check()

    robot = Robot()

    # Communication start
    response = mic(2)
    if response == "":
        call_num += 1
        print(call_num)
    if call_num == 3:
        speaking("Please call me hey!")
        call_num = 0
    if response == "hey":
        speaking("yes sir!")
        response = mic(3)

        if response == "reset":
            speaking("ok. Reset mode")
            name_ini()
        elif response == "turn off":
            speaking("ok. turn off mode")
            break
        elif response == "silent":
            speaking("ok. silent mode")
            call_num = - 1000000

        while response != "":
            response_ = robot.gpt_send_anw(response)
            speaking(response_)
            response = mic(3)

            if response == "":
                break
mp3_path = "./ResultMP3.mp3"
sam_path = "./sampleWav.wav"
test_path = "./test.wav"
os.remove(mp3_path)
os.remove(sam_path)
os.remove(test_path)
