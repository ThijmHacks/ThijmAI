import speech_recognition as sr


from ThijmAI.listening.user import *
from ThijmAI.listening.keyword import *


class ThijmAI():
    def __init__(self):
        keywords = "jarvis"
        while True:
            activated = keyword(keywords)
            if activated:
                user()