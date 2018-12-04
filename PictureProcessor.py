from PIL import ImageDraw


class PictureProcessor:
    Apaette = {'черно-белое': ['000000000', '255255255'],
               'Геймбой': ['000000000', '052104086', '136192112', '224248208'],
               'Apple 2': ['000000000', '062049162', '087066000', '140062052', '084084084', '141071179', '144095037',
                           '124112218', '128128128', '104169065',
                           '187119109', '122191199', '171171171', '208220113', '172234136', '255255255'],
               'отенки серого': ['000000000', '065065065', '084084084', '103103103', '127127127', '138138138',
                                 '171171171',
                                 '204204204', '255255255']}


    def __init__(self, image, resolution, palette):
        self.image = image
        self.resolution = resolution
        self.palette = palette

    def Pixilizer(self):
        pix = self.image.load()
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0]
        height = self.image.size[1]
        for a in range(width // self.resolution):
            for b in range(height // self.resolution):
                middleR = 0
                middleG = 0
                middleB = 0
                for i in range(a * self.resolution, (a + 1) * self.resolution):
                    for j in range(b * self.resolution, (b + 1) * self.resolution):
                        middleR += pix[i, j][0]
                        middleG += pix[i, j][1]
                        middleB += pix[i, j][2]
                middleR = middleR // (self.resolution * self.resolution)
                middleG = middleG // (self.resolution * self.resolution)
                middleB = middleB // (self.resolution * self.resolution)

                draw.rectangle(((a * self.resolution, b * self.resolution),
                                ((a + 1) * self.resolution - 1, (b + 1) * self.resolution - 1)),
                               fill=(middleR, middleG, middleB))

        del draw

    def Colorer(self):
        pix = self.image.load()
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0]
        height = self.image.size[1]
        listP = self.Apaette[str(self.palette)]
        for a in range(width // self.resolution):
            for b in range(height // self.resolution):

                middle = ''
                if pix[a * self.resolution, b * self.resolution][0] < 10:
                    middle = '00' + str(pix[a * self.resolution, b * self.resolution][0])
                if pix[a * self.resolution, b * self.resolution][0] < 100:
                    middle = '0' + str(pix[a * self.resolution, b * self.resolution][0])
                if pix[a * self.resolution, b * self.resolution][0] < 256:
                    middle = str(pix[a * self.resolution, b * self.resolution][0])

                if pix[a * self.resolution, b * self.resolution][1] < 10:
                    middle += '00' + str(pix[a * self.resolution, b * self.resolution][1])
                if 9 < pix[a * self.resolution, b * self.resolution][1] < 100:
                    middle += '0' + str(pix[a * self.resolution, b * self.resolution][1])
                if 99 < pix[a * self.resolution, b * self.resolution][1] < 256:
                    middle += str(pix[a * self.resolution, b * self.resolution][1])

                if pix[a * self.resolution, b * self.resolution][2] < 10:
                    middle += '00' + str(pix[a * self.resolution, b * self.resolution][2])
                if 9 < pix[a * self.resolution, b * self.resolution][2] < 100:
                    middle += '0' + str(pix[a * self.resolution, b * self.resolution][2])
                if 99 < pix[a * self.resolution, b * self.resolution][2] < 256:
                    middle += str(pix[a * self.resolution, b * self.resolution][2])

                ras = 10000000000
                for i in listP:
                    if abs(int(middle) - int(i)) < ras:
                        ras = abs((int(middle) - int(i)))
                        fin = i
                draw.rectangle(((a * self.resolution, b * self.resolution), ((a + 1) * self.resolution - 1,
                                                                             (b + 1) * self.resolution - 1)),
                               fill=(int(fin[0:3]), int(fin[3:6]), int(fin[6:9])))

        del draw
