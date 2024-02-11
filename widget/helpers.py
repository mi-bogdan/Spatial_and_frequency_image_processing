from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class UIHelpers:
    """Класс виджетов для формы"""

    @staticmethod
    def createLabel(parent, width: int, height: int, x: int, y: int, style: str = None, text: str = None):
        """Лейбел"""
        label = QtWidgets.QLabel(parent)
        label.resize(width, height)
        label.move(x, y)
        label.setStyleSheet(style)
        # Сделать изображение адаптивным к размеру этикетки
        label.setScaledContents(True)
        # self.label_img_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(Qt.AlignCenter)
        label.setText(text)

        return label

    @staticmethod
    def createButton(parent, text: str, callback, geomenty, style: str):
        """Кнопка"""
        button = QPushButton(parent)
        button.setText(text)
        button.clicked.connect(callback)
        button.setGeometry(geomenty)
        button.setStyleSheet(style)
        return button

    @staticmethod
    def createLineEdit(parent, x: int, y: int, text: str):
        """Текстовое поле"""
        line_edit = QLineEdit(parent)  # Создание текстового поля
        line_edit.move(x, y)
        # Опционально: установить текст по умолчанию
        line_edit.setPlaceholderText(text)
        # Подключим слот textChanged к изменениям текста, чтобы обрабатывать его ввод
        # line_edit.textChanged.connect(callback)
        return line_edit
