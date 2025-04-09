import speech_recognition as sr


from ThijmAI.listening.user import *
from ThijmAI.listening.keyword import *
from ThijmAI.speaking.speak import *
from ThijmAI.command.command import *

class ThijmAI():
    def __init__(self):
        program = True
        keywords = "friday"
        while program:
            activated = keyword(keywords)
            if activated:
                command_input = user()

                command(command_input)