from Chat.voiceChat import *

while True:
    conversation = conversation_loop()
    if not conversation:
        break
