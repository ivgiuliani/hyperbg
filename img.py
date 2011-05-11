from PIL import Image, ImageDraw

import classify

def image_colors(filename, k=3):
    fp = open(filename, "r")
    im = Image.open(fp)
    im.load()
    classifier = classify.KColorMeans(k=k)

    for pixel in im.getdata():
        classifier.fit(pixel)

    prediction = classifier.predict()
    fp.close()
    return prediction

if __name__ == "__main__":
    import sys
    k = int(sys.argv[1])
    filename = sys.argv[2]

    print "Using k: %d" % k

    predictions = image_colors(filename, k)

    im = Image.new("RGB", (100, k * 50))
    draw = ImageDraw.Draw(im)

    top, bottom = 0, 100
    for color in predictions:
        print color
        draw.rectangle(((0, top), (100, bottom)), fill=tuple(color))
        draw.line(((0,bottom), (100, bottom)), fill="white", width=2)
        top, bottom = top + 100, bottom + 50

    im.show()

    img_orig = Image.open(filename)
    img_orig.thumbnail((500, 500), Image.NEAREST)
    img_orig.show()
    
