import speech_recognition as sr
from ThijmAI.speaking.speak import *


def user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something: ")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said to me: {command}")
        speak(command)

        return command.lower()
    except sr.UnknownValueError:
        print("Can you repeat that?")
        return None
    except sr.RequestError:
        print("I cannot connect to your service.")
        return None