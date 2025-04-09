import speech_recognition as sr

def keyword(keyword="friday"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Enabled")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        if keyword.lower() in command.lower():
            return True
        return False
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None