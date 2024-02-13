import shutil
import sys
import numpy as np

from PyQt5.QtWidgets import QApplication,  QFileDialog, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt, QRect

from widget.helpers import UIHelpers

from PIL import Image, ImageFilter, ImageCms, ImageOps
import matplotlib.pyplot as plt


class Forma(QWidget):
    """Главная форма приложения"""

    def __init__(self):
        super(Forma, self).__init__()
        self.file = None
        self.imagePath = ''
        self.image_path_news = ''
        self.initUI()

    def initUI(self):
        self.resize(1100, 600)
        self.move(100, 10)
        self.setWindowTitle(
            'Пространственная и частотная обработка изображений')
        self.setStyleSheet("background-color: rgb(207, 207, 207)")

        self.label_img_1 = UIHelpers.createLabel(
            self, 350, 380, 10, 10, 'border-style: solid; border-width: 1px; border-color: black;')

        self.label_img_2 = UIHelpers.createLabel(
            self, 350, 380, 365, 10, 'border-style: solid; border-width: 1px; border-color: black;')

        self.button_original = UIHelpers.createButton(
            self,
            'Оригинал',
            self.original,
            QRect(10, 430, 200, 41),
            "background-color:rgb(170, 85, 127);\n""font: 12pt \"Pristina\";"
        )

        self.button_open = UIHelpers.createButton(
            self,
            'Открыть фото',
            self.dialog,
            QRect(10, 475, 200, 41),
            "background-color:rgb(170, 85, 127);\n""font: 12pt \"Pristina\";"
        )

        self.button_save = UIHelpers.createButton(
            self,
            'Сохранить фото',
            self.saveImage,
            QRect(10, 520, 200, 41),
            "background-color:rgb(170, 85, 127);\n""font: 12pt \"Pristina\";"
        )

        # ----------------------------------------------------------------------------------------------------------------------------------

        self.label_resize = UIHelpers.createLabel(
            self, 120, 50, 750, 10, '', 'Изменение размера \n изображения'
        )
        self.line_edit_resize_width = UIHelpers.createLineEdit(
            self, 745, 60, 'Ширина')
        self.line_edit_resize_height = UIHelpers.createLineEdit(
            self, 745, 90, 'Высота')

        self.button_resize = UIHelpers.createButton(
            self,
            'Изменить размер',
            self.resizeImage,
            QRect(750, 130, 120, 30),
            "background-color:rgb(170, 85, 127);\n""font: 8pt \"Pristina\";"
        )

        # ------------------------------------------------------------------------------------------------------------------------------------

        self.label_crop = UIHelpers.createLabel(
            self, 130, 50, 745, 170, '', 'Обрезка изображения'
        )
        self.line_edit_crop_x = UIHelpers.createLineEdit(
            self, 745, 210, 'X')
        self.line_edit_crop_y = UIHelpers.createLineEdit(
            self, 745, 240, 'Y')
        self.line_edit_crop_x_width = UIHelpers.createLineEdit(
            self, 745, 270, 'Ширина')
        self.line_edit_crop_y_height = UIHelpers.createLineEdit(
            self, 745, 300, 'Высота')

        self.button_resize = UIHelpers.createButton(
            self,
            'Обрезать',
            self.cropImage,
            QRect(755, 330, 120, 30),
            "background-color:rgb(170, 85, 127);\n""font: 8pt \"Pristina\";"
        )
        # --------------------------------------------------------------------------------------------------------------------------------------------
        self.label_lab = UIHelpers.createLabel(
            self, 130, 50, 250, 400, '', 'Цветовая схема LAB'
        )
        self.button_lab = UIHelpers.createButton(
            self,
            'Схема LAB',
            self.convert_to_lab,
            QRect(220, 450, 200, 41),
            "background-color:rgb(170, 85, 127);\n""font: 12pt \"Pristina\";"
        )

        # ------------------------------------------------------------------------------------------------------------------------------------------------

        self.label_gray = UIHelpers.createLabel(
            self, 130, 50, 480, 400, '', 'Преобразование'
        )
        self.button_gray = UIHelpers.createButton(
            self,
            'Серый',
            self.convert_gray,
            QRect(440, 450, 200, 41),
            "background-color:rgb(170, 85, 127);\n""font: 12pt \"Pristina\";"
        )
        # -------------------------------------------------------------------------------------------------------------------------------------------------

        self.label_histogram = UIHelpers.createLabel(
            self, 220, 50, 650, 400, '', 'Гистограмма яркости изображения'
        )
        self.button_histogram = UIHelpers.createButton(
            self,
            'Постороить',
            self.histogram_gray,
            QRect(660, 450, 200, 41),
            "background-color:rgb(170, 85, 127);\n""font: 12pt \"Pristina\";"
        )

        # --------------------------------------------------------------------------------------------------------------------------------------------

        self.label_histogram = UIHelpers.createLabel(
            self, 500, 30, 290, 500, '', 'Выравнивание гистограммы яркости с методом повышения контраста'
        )
        self.button_histogram = UIHelpers.createButton(
            self,
            'Нормализации гистограммы',
            self.normalize_histogram,
            QRect(380, 530, 300, 41),
            "background-color:rgb(170, 85, 127);\n""font: 12pt \"Pristina\";"
        )

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.label_histogram = UIHelpers.createLabel(
            self, 100, 30, 950, 10, '', 'Фильтры'
        )
        self.button_median_filter = UIHelpers.createButton(
            self,
            'Медианный',
            self.median_filter,
            QRect(930, 50, 150, 41),
            "background-color:rgb(170, 85, 127);\n""font: 8pt \"Pristina\";"
        )
        self.button_gaussia_filter = UIHelpers.createButton(
            self,
            'Гаусса',
            self.gaussian_filter,
            QRect(930, 100, 150, 41),
            "background-color:rgb(170, 85, 127);\n""font: 8pt \"Pristina\";"
        )
        self.button_core_filter = UIHelpers.createButton(
            self,
            'Свой',
            self.filter_core,
            QRect(930, 150, 150, 41),
            "background-color:rgb(170, 85, 127);\n""font: 8pt \"Pristina\";"
        )

        # --------------------------------------------------------------------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------------------------------------------------------------------

    def normalize_histogram(self):
        """Контрастная нормализация гистограммы"""
        img = Image.open(self.imagePath)
        # Применение нормализации гистограммы
        img_contrast = ImageOps.equalize(img)
        img_contrast.save('cache/cache.jpg')

        pixmap = QPixmap('cache/cache.jpg')

        self.label_img_2.setPixmap(pixmap.scaled(
            self.label_img_2.size(), Qt.KeepAspectRatio))

        plt.figure(figsize=(10, 5))

        # Генерация и отображение гистограммы оригинального изображения
        plt.subplot(1, 2, 1)
        # Для каждого изображения считаются значения гистограммы по плоско развернутому массиву пикселей (flatten())
        plt.hist(np.array(img.convert('L')).flatten(), bins=256, range=(
            0, 256), alpha=0.75, color='blue', label='Original')
        plt.legend()

        # Генерация и отображение гистограммы изображения после нормализации
        plt.subplot(1, 2, 2)
        plt.hist(np.array(img_contrast.convert('L')).flatten(), bins=256,
                 range=(0, 256), alpha=0.75, color='red', label='Equalized')
        plt.legend()

        plt.show()

    def filter_core(self):
        """Фильтр по ядру"""
        input_image = Image.open(self.imagePath)
        # Создаем ядро фильтра
        kernel = [
            0, 0, 0,
            0, 1, 0,
            0, 0, 0
        ]
        # Применяем свертку с заданным ядром
        output_image = input_image.filter(
            ImageFilter.Kernel((3, 3), kernel, scale=None, offset=0))
        output_image.save(self.imagePath)
        pixmap = QPixmap(self.imagePath)
        self.label_img_2.setPixmap(pixmap)

    def median_filter(self):
        """Медианный фильтр"""
        input_image = Image.open(self.imagePath)
        # Применяем медианный фильтр с радиусом 3
        output_image = input_image.filter(ImageFilter.MedianFilter(size=3))
        output_image.save('cache/cache.jpg')
        pixmap = QPixmap(self.imagePath)
        self.label_img_2.setPixmap(pixmap)

    def gaussian_filter(self):
        """Фильтр гаусса"""

        input_image = Image.open(self.imagePath)
        # Применяем гауссовый фильтр с радиусом 3
        gaussian_image = input_image.filter(ImageFilter.GaussianBlur(radius=3))
        gaussian_image.save(self.imagePath)
        pixmap = QPixmap(self.imagePath)
        self.label_img_2.setPixmap(pixmap)

    def histogram_gray(self):
        """Построение гистограммы яркости серого"""

        image = Image.open(self.imagePath)
        gray_image = image.convert('L')
        gray_image.save('cache/cache.jpg')
        pixmap = QPixmap(self.imagePath)
        self.label_img_2.setPixmap(pixmap)

        # Возвращает гистограмму, которая представляет собой список, частота каждого значения яркости от 0 до 255.
        histogram = gray_image.histogram()
        # Разделяем данные гистограммы на красный цвет
        histogram_red = histogram[0:256]

        # Строим гистограмму яркости
        plt.figure(figsize=(8, 5))
        # Строится столбчатая гистограмма (ось X) значения яркости от 0 до 255, (ось Y) — частоту каждого уровня яркости в изображении
        plt.bar(range(256), histogram_red, color='red')
        plt.ylabel('Частота')
        plt.xlabel('Яркость')
        plt.title('Гистограмма яркости изображения')
        plt.show()

    def convert_gray(self):
        """Фильтр серого"""
        image = Image.open(self.imagePath)
        gray_image = image.convert('L')
        gray_image.save('cache/cache.jpg')
        pixmap = QPixmap(self.imagePath)
        self.label_img_2.setPixmap(pixmap)

    def convert_to_lab(self):
        """Переход в цветовую схему LAB"""
        # Открываем изображение с помощью Pillow
        image = Image.open(self.imagePath)

        # Конвертируем изображение в цветовую схему Lab
        if image.mode == "L":
            self.showMessage()
            return
        else:
            lab_image = image.convert(
                "LAB", colors=ImageCms.createProfile("LAB"))
            lab_image.save('cache/lab_image.tif')

        # Отображаем исходное и конвертированное изображение
        pixmap_lab = QPixmap('cache/lab_image.tif')
        self.label_img_2.setPixmap(pixmap_lab)
        self.saveImage()

    def showMessage(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Уберите серый фильтр!")
        msgBox.setWindowTitle("Информирование")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK')

    def original(self):
        """Загрузка оригинальной фото в label"""
        if self.file:
            images_o = QPixmap(self.file)
            images_o.save('cache/cache.jpg')
            self.label_img_2.setPixmap(images_o)

    def dialog(self):
        """Загружаем изображения"""
        self.file, self.check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                            "",
                                                            "All files (*.*);;BMP (*.bmp);;GIF (*.gif);;ICNS (*.icns);;ICO (*.ico);;JPEG (*.jpeg);;JPG (*.jpg);;PBM (*.pbm);;PGM (*.pgm);;PNG (*.png);;PPM (*.ppm);;SVG (*.svg);;SVGZ (*.svgz);;TGA (*.tga);;TIF (*.tif);;TIFF (*.tiff);;WBMP (*.wbmp);;WEBP (*.webp);;XBM (*.xbm);;XPM (*.xpm)")

        if self.check:

            self.imagePath = 'cache/cache.jpg'
            self.images_open = QPixmap(self.file)
            self.images_open.save(self.imagePath)
            # Показываем картинку на этикетке
            self.label_img_1.setPixmap(self.images_open)
            self.label_img_1.setProperty("path", self.file)
            self.label_img_2.setPixmap(self.images_open)
            self.label_img_2.setProperty("image_path", self.file)

    def saveImage(self):
        """Сохраняем изображения"""
        if self.imagePath:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "new_photo.jpg",
                                                      "Image Files (*.png *.jpg *.jpeg *.bmp *.tif)",
                                                      options=options)
            if fileName:
                print("файл для Сохранения: ", fileName)

                shutil.copy(self.imagePath, fileName)

    def resizeImage(self):
        """Изменения размера изображения"""
        try:
            width = int(self.line_edit_resize_width.text())
            height = int(self.line_edit_resize_height.text())
            image = QPixmap(self.imagePath)
            resized_image = image.scaled(width, height)
            resized_image.save('cache/cache.jpg')
            self.label_img_2.setPixmap(resized_image)

        except ValueError:
            print('Введеные данные были не числом')
            return

    def cropImage(self):
        """Обрезка изображения"""
        try:
            x = int(self.line_edit_crop_x.text())
            y = int(self.line_edit_crop_y.text())
            width = int(self.line_edit_crop_x_width.text())
            height = int(self.line_edit_crop_y_height.text())

            # Открыть изображение с Pillow
            image = Image.open(self.imagePath)
            cropped_image = image.crop((x, y, x+width, y+height))

            # Сохранить обрезанное изображение
            cropped_image.save('cache/cache.jpg')

            pixmap = QPixmap(self.imagePath)
            self.label_img_2.setPixmap(pixmap)

        except ValueError:
            print('Введенные данные не являются числами')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    forma = Forma()
    forma.show()
    sys.exit(app.exec_())
