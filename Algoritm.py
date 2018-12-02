import time

from PIL import Image  # Подключим необходимые библиотеки.

import PictureProcessor

image = Image.open("temp.jpg")  # Открываем изображение.
color = int(input())
worker = PictureProcessor.PictureProcessor(image, 32, color)
worker.Pixilizer()
image.save("ans.jpeg", "JPEG")
worker.Colorer()
image.save("fin.jpeg", "JPEG")
