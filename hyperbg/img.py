import sys
from PIL import Image, ImageDraw, ImageEnhance

from hyperbg import classify

class Wallpaper(object):
    IMAGE_SCALE_SIZE = (600, 600)

    def __init__(self, filename, k=3):
        self.filename = filename
        self.k = k

    def __prepare(self):
        "Return a new Image object enhanced for the classifying goal"
        self.image.thumbnail(self.IMAGE_SCALE_SIZE, Image.NEAREST)
        self.image = ImageEnhance.Contrast(self.image).enhance(0.9)
        self.image = ImageEnhance.Sharpness(self.image).enhance(1.1)

    def load(self):
        self.image = Image.open(self.filename)
        self.image.load()

    def colors(self):
        "Extract the first k dominant colors from an image"
        self.__prepare()
        classifier = classify.Classifier(k=self.k)

        for pixel in self.image.getdata():
            classifier.fit(pixel)

        prediction = classifier.predict()

        return prediction

def draw_sample(filename, predictions):
    "Draw the original image with a box of the predicted dominant colors"
    k = len(predictions)

    fp = open(filename, "r")
    im = Image.open(fp)
    im.thumbnail(Wallpaper.IMAGE_SCALE_SIZE, Image.ANTIALIAS)
    draw = ImageDraw.Draw(im)

    top, bottom = 0, 50
    for color in predictions:
        draw.rectangle(((0, top), (150, bottom)), fill=tuple(color))
        draw.line(((0, bottom), (150, bottom)), fill="white", width=2)
        text_x = 10
        text_y = (top + bottom) / 2
        draw.text((text_x, text_y), str(color), fill="red")
        top, bottom = top + 50, bottom + 50

    fp.close()
    im.show()

def main(args):
    try:
        filename = args[1]
    except IndexError:
        print("Usage: %s <filename> [<classes>]" % (args[0], ))
        return False
 
    try:
        k = int(args[2])
    except (IndexError, ValueError):
        k = None

    wallpaper = Wallpaper(filename, k or 3)
    wallpaper.load()
    predictions = wallpaper.colors()
    draw_sample(filename, predictions)

    return True

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
