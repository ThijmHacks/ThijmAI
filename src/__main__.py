import speech_recognition as sr

def user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something: ")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said to me: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Can you repeat that?")
        return None
    except sr.RequestError:
        print("I cannot connect to your service.")
        return None

def keyword(keyword="assistant"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Enabled")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        if keyword.lower() in command:
            return True
        return False
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None


while True:
    activated = keyword("laptop")
    if activated:
        user()
