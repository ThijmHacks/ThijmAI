from datetime import datetime

from ThijmAI.speaking.speak import *

def command(command):
    command = command or ""
    if "time" in command:
        time = datetime.now()

        output = "It is currently: " + time.strftime("%H:%M")

        print(output)
        speak(output)

        return

    else:


        output = f"You said to me: {command}"

        print(output)
        speak(output)

        return