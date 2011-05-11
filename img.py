import sys
from PIL import Image, ImageDraw

import classify

def image_colors(filename, k=3):
    fp = open(filename, "r")
    im = Image.open(fp)
    im.thumbnail((500, 500), Image.NEAREST)
    im.load()
    classifier = classify.KColorMeans(k=k)

    for pixel in im.getdata():
        classifier.fit(pixel)

    prediction = classifier.predict()
    fp.close()
    return prediction

def draw_sample(filename, predictions):
    k = len(predictions)
    im = Image.new("RGB", (100, k * 50))
    draw = ImageDraw.Draw(im)

    top, bottom = 0, 50
    for color in predictions:
        print color
        draw.rectangle(((0, top), (100, bottom)), fill=tuple(color))
        draw.line(((0,bottom), (100, bottom)), fill="white", width=2)
        top, bottom = top + 100, bottom + 50

    im.show()

    img_orig = Image.open(filename)
    img_orig.thumbnail((500, 500), Image.NEAREST)
    img_orig.show()

def main(args):
    try:
        filename = args[1]
    except IndexError:
        print("Usage: %s <classes> <filename>" % (args[0], ))
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
    
