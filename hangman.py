from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QFont, QIcon, QPainter, QPen
from PyQt5.QtCore import Qt
import sys, random

class WordLoader:
    def __init__(self, filename):
        self.filename = filename

    def load_words(self):
        try:
            with open(self.filename, 'r', encoding="utf-8") as file:
                words = file.readlines()
                return [word.strip() for word in words]
        except FileNotFoundError:
            print(f"{self.filename} dosyası bulunamadı!")
            return []

class HangmanGame:
    def __init__(self, word_list):
        self.word_list = word_list
        self.selected_word = ""
        self.masked_word = []
        self.guessed_letters = set()
        self.wrong_guesses = 0

    def initialize_game(self):
        if not self.word_list:
            return "Kelime listesi yüklenemedi!"
        self.selected_word = random.choice(self.word_list)
        self.masked_word = ["_" if char != " " else " " for char in self.selected_word]
        self.guessed_letters.clear()
        self.wrong_guesses = 0

    def update_word(self, letter):
        if letter not in self.selected_word:
            self.wrong_guesses += 1
        for i, char in enumerate(self.selected_word):
            if char == letter:
                self.masked_word[i] = letter

class HangmanUI(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.initUI()

    def initUI(self):
        self.setFixedSize(600, 500)
        self.setWindowTitle('Adam Asmaca Oyunu')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.center_geo()

        self.word_label = QLabel("", self)
        self.word_label.setFont(QFont("Arial", 20))
        self.word_label.setAlignment(Qt.AlignTop)

        self.letter_input = QLineEdit(self)
        self.letter_input.setMaxLength(1)
        self.letter_input.setFont(QFont("Arial", 18))
        self.letter_input.setPlaceholderText("Bir harf gir")
        self.letter_input.setEnabled(False)
        self.letter_input.returnPressed.connect(self.check_letter)

        self.new_game_button = QPushButton("Yeni Oyun", self)
        self.new_game_button.setFont(QFont("Arial", 14))
        self.new_game_button.clicked.connect(self.start_game_ui)
        self.new_game_button.setVisible(False)

        self.exit_button = QPushButton("Çıkış", self)
        self.exit_button.setFont(QFont("Arial", 14))
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setVisible(False)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.word_label)
        main_layout.addWidget(self.letter_input)
        main_layout.addWidget(self.new_game_button)
        main_layout.addWidget(self.exit_button)
        self.setLayout(main_layout)

    def center_geo(self):
        screen = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen.center())
        self.move(window_geometry.topLeft())

    def start_game_ui(self):
        self.game.initialize_game()
        self.word_label.setText(" ".join(self.game.masked_word))
        self.letter_input.setEnabled(True)
        self.letter_input.setFocus()
        self.new_game_button.setVisible(False)
        self.exit_button.setVisible(False)
        self.update()

    def check_letter(self):
        letter = self.letter_input.text().lower()
        self.letter_input.clear()

        if letter in self.game.guessed_letters:
            return

        self.game.guessed_letters.add(letter)
        self.game.update_word(letter)
        self.word_label.setText(" ".join(self.game.masked_word))

        if "_" not in self.game.masked_word:
            self.letter_input.setEnabled(False)
            self.word_label.setText(f"Tebrikler! Kelimeyi buldunuz!\nKelime: {self.game.selected_word}")
            self.show_end_buttons()
        elif self.game.wrong_guesses >= 6:
            self.letter_input.setEnabled(False)
            self.word_label.setText(f"Oyun Bitti! Kelime: {self.game.selected_word}")
            self.word_label.setFont(QFont("Arial", 10))
            self.show_end_buttons()

        self.update()

    def show_end_buttons(self):
        self.new_game_button.setVisible(True)
        self.exit_button.setVisible(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        self.draw_hangman(painter)
        painter.end()

    def draw_hangman(self, painter):
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        painter.drawLine(100, 100, 100, 400)
        painter.drawLine(50, 400, 200, 400)
        painter.drawLine(100, 100, 300, 100)
        painter.drawLine(300, 100, 300, 150)

        if self.game.wrong_guesses > 0:
            painter.drawEllipse(275, 150, 50, 50)
        if self.game.wrong_guesses > 1:
            painter.drawLine(300, 200, 300, 300)
        if self.game.wrong_guesses > 2:
            painter.drawLine(300, 220, 250, 270)
        if self.game.wrong_guesses > 3:
            painter.drawLine(300, 220, 350, 270)
        if self.game.wrong_guesses > 4:
            painter.drawLine(300, 300, 250, 350)
        if self.game.wrong_guesses > 5:
            painter.drawLine(300, 300, 350, 350)


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(300, 200)
        self.setWindowTitle('Adam Asmaca Oyunu')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.center_geo()

        self.start_button = QPushButton("Oyuna Başla", self)
        self.start_button.clicked.connect(self.start_game)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def center_geo(self):
        screen = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen.center())
        self.move(window_geometry.topLeft())

    def start_game(self):
        word_loader = WordLoader("tr-wordlist.txt")
        word_list = word_loader.load_words()
        game = HangmanGame(word_list)
        self.game_window = HangmanUI(game)
        self.game_window.start_game_ui()
        self.game_window.show()
        self.close()

def main():
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
