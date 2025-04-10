from datetime import datetime

from ThijmAI.speaking.speak import *
import ThijmAI.command.ai as ai
import ThijmAI.command.homeassistant as ha

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

    if "lights" in command:

        ha.homeassistant(command)

    else:

        output = f"You said to me: {command}"

        print(output)
        speak(output)

        return