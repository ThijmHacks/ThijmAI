from datetime import datetime

from ThijmAI.speaking.speak import *
import ThijmAI.command.ai as ai

def command(command):
    command = command or ""
    if "time" in command:
        time = datetime.now()

        output = "It is currently: " + time.strftime("%H:%M")

        print(output)
        speak(output)

        return

    if "what is" in command:
        output = ai.chat(command)

        print(output)
        speak(output)
    else:


        output = f"You said to me: {command}"

        print(output)
        speak(output)

        return