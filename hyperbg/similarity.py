import os
import sys

from hyperbg import img, classify

def sort_similar(filenames, colors, similarity=classify.euclidean_color_distance):
    ordered_images = []
    for filename in filenames:
        wallpaper = img.Wallpaper(filename)
        wallpaper.load()
        main_colors = wallpaper.colors()

        dist = 0
        for main_color in main_colors:
            dist += similarity(main_color, colors)

        ordered_images.append([filename, dist])

    return sorted(ordered_images, key=lambda x: x[1])


if __name__ == "__main__":
    directory = sys.argv[1]
    r, g, b = sys.argv[2:5]
    filenames = [
            os.path.join(directory, filename)
            for filename in os.listdir(directory)
    ]
    for fname, score in sort_similar(filenames, [
            int(r), int(g), int(b)
        ]):
        print "%s - %s" % (fname, score)

