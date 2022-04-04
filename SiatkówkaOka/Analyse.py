import Effectiveness
import Image
from statistics import mean


class Analyse:
    def __init__(self):
        self.images = []
        self.holdsOut = []
        self.effective = []
        self.sen = []
        self.spe = []
        self.acc = []

    def __images(self, paths):
        for path in paths:
            img = Image.loadImage(path)
            prep = Image.getPreparedImage(img)
            result = Image.getResultImage(prep)

            self.images.append(Image.getResultBinary(result, prep))

    def __holdOuts(self, paths):
        for path in paths:
            self.holdsOut.append(Image.getHoldOut(path))

    def __effectiveness(self):
        for i in range(len(self.images)):
            self.effective.append(Effectiveness.checkEffectiveness(self.images[i], self.holdsOut[i],
                                                                   isPrint=False, isTable=False))

    def __average(self):
        for element in self.effective:
            self.sen.append(element[4])
            self.spe.append(element[5])
            self.acc.append(element[6])

    def analyse5images(self, paths, hoPaths):
        self.__images(paths)
        self.__holdOuts(hoPaths)
        self.__effectiveness()
        self.__average()

        avgSen = mean(self.sen)
        avgSpe = mean(self.spe)
        avgAcc = mean(self.acc)

        print('Effectiveness for 5 images')
        print('Average sensitivity: {}%'.format(round(avgSen * 100, 2)))
        print('Average specificity: {}%'.format(round(avgSpe * 100, 2)))
        print('Average accuracy: {}%'.format(round(avgAcc * 100, 2)))
        print('Specificity&Sensitivity Average: {}%\n'.format(round((avgSen + avgSpe) / 2 * 100, 2)))
