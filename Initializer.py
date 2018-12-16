from PIL import Image

from PictureProcessor import PictureProcessor


class Initializer:

    def run(name_file, resol, color):

        print(resol)
        re = 1
        if resol == 'Не сжатое':
            re = 1
        elif resol == 'Среднее сжатие':
            re = 8
        elif resol == 'Сильное сжатие':
            re = 16
        print(re)
        thread = PictureProcessor(name_file, re, color)
        thread.start()
