import sys
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

import bot
from time import sleep
from PySide6.QtCore import QThread, QObject, Signal, QUrl
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QStackedWidget, QVBoxLayout


class Worker(QObject):
    update_anim = Signal(str)
    play_bad_apple = Signal()

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            response = bot.handle_conversation()

            if response == 100: self.play_bad_apple.emit()
            else:
                # speak_result(response)
                self.update_anim.emit("speaking")
            sleep(15)
            self.update_anim.emit("idle")

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.gif = None
        self.setWindowTitle("Grumbot")

        self.container = QLabel("Grumbot")
        self.video_player = VideoPlayer()

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.addWidget(self.video_player)
        self.central_widget.addWidget(self.container)

        self.central_widget.setCurrentWidget(self.container)
        self.update_gif("idle")

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

        self.worker.update_anim.connect(self.update_gif)
        self.worker.play_bad_apple.connect(self.play_bad_apple)

    def update_gif(self, new_anim):
        self.gif = QMovie(f"assets/faces/{new_anim}.gif")
        self.container.setMovie(self.gif)
        self.gif.start()

    def play_bad_apple(self):
        self.central_widget.setCurrentWidget(self.video_player)
        self.video_player.play()

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