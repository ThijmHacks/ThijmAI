import speech_recognition as sr


from ThijmAI.listening.user import *
from ThijmAI.listening.keyword import *
from ThijmAI.speaking.speak import *
from ThijmAI.command.command import *

class ThijmAI():
    def __init__(self):
        keywords = "friday"
        while True:
            activated = keyword(keywords)
            if activated:
                command_input = user()

                command(command_input)