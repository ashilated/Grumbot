import pyttsx3
from PySide6.QtCore import QObject


class TTS(QObject):
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[25].id)

    def start_loop(self):
        self.engine.startLoop()

    def speak(self, message):
        self.engine.say(message)
