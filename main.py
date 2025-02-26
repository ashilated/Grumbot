import sys
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from tts import TTS
import bot
from time import sleep
from PySide6.QtCore import QThread, QObject, Signal, QUrl, Qt
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QStackedWidget, QVBoxLayout

current_anim = "idle"

class Worker(QObject):
    update_anim = Signal(str)
    play_bad_apple = Signal()


    def __init__(self):
        super().__init__()

    def run(self):
        tts_thread = QThread()
        tts = TTS()
        tts.moveToThread(tts_thread)
        tts_thread.started.connect(tts.start_loop())
        tts_thread.start()


        while True:
            response = bot.handle_conversation()

            if response == 100:
                self.play_bad_apple.emit()
            else:
                self.update_anim.emit("speaking")
                tts.speak(response)
                while tts.engine.isBusy():
                    sleep(0.1)

            self.update_anim.emit("idle")

    def go_to_sleep(self):
        timer = 0

        while True:
            if current_anim == "idle": timer += 1
            elif timer != 0: timer = 0
            if timer > 30:
                self.update_anim.emit("sleeping")
                timer = 0
            sleep(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grumbot")
        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        #self.showFullScreen()

        self.container = QLabel("Grumbot")
        self.video_player = VideoPlayer()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.addWidget(self.video_player)
        self.central_widget.addWidget(self.container)
        self.central_widget.setCurrentWidget(self.container)
        self.gif = QMovie()
        self.update_gif("idle")

        self.bot_worker = Worker()
        self.bot_thread = QThread()
        self.bot_worker.moveToThread(self.bot_thread)
        self.bot_thread.started.connect(self.bot_worker.run)
        self.bot_thread.start()

        self.sleep_worker = Worker()
        self.sleep_thread = QThread()
        self.sleep_worker.moveToThread(self.sleep_thread)
        self.sleep_thread.started.connect(self.sleep_worker.go_to_sleep)
        self.sleep_thread.start()

        self.bot_worker.update_anim.connect(self.update_gif)
        self.sleep_worker.update_anim.connect(self.update_gif)
        self.bot_worker.play_bad_apple.connect(self.play_bad_apple)
        self.video_player.media_player.mediaStatusChanged.connect(self.switch_back_widget)

    def update_gif(self, new_anim):
        global current_anim
        current_anim = new_anim
        self.gif = QMovie(f"assets/faces/{new_anim}.gif")
        self.container.setMovie(self.gif)
        self.gif.start()

    def play_bad_apple(self):
        self.central_widget.setCurrentWidget(self.video_player)
        self.video_player.play()

    def switch_back_widget(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.central_widget.setCurrentWidget(self.container)

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setSource(QUrl.fromLocalFile("assets/badapple.mp4"))

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.video_widget)
        self.setLayout(self.layout)

    def play(self):
        self.media_player.play()
        #sleep(221)

    def set_video(self, url):
        self.media_player.setSource(QUrl.fromLocalFile(url))


app = QApplication()
window = MainWindow()
window.show()
app.exec()