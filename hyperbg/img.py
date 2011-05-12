import sys
from PIL import Image, ImageDraw

from hyperbg import classify

IMAGE_SCALE_SIZE = (500, 500)

def image_colors(filename, k=3):
    "Extract the first k dominant colors from an image"
    fp = open(filename, "r")
    im = Image.open(fp)
    im.thumbnail(IMAGE_SCALE_SIZE, Image.NEAREST)
    im.load()
    classifier = classify.KColorMeans(k=k)

    for pixel in im.getdata():
        classifier.fit(pixel)

    prediction = classifier.predict()
    fp.close()
    return prediction

def draw_sample(filename, predictions):
    "Draw the original image with a box of the predicted dominant colors"
    k = len(predictions)

    fp = open(filename, "r")
    im = Image.open(fp)
    im.thumbnail(IMAGE_SCALE_SIZE, Image.ANTIALIAS)
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

    predictions = image_colors(filename, k or 3)
    draw_sample(filename, predictions)

    return True

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
