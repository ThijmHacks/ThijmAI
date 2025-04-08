from ThijmAI.speaking.speak import *

def command(command):
    if "time" in command:
        output = "I cant tell you the time right now"

        print(output)

        speak(output)