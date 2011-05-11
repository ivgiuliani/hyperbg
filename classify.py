import random
import math
import operator

RGB_RED, RGB_GREEN, RGB_BLUE = 0, 1, 2

def euclidean_color_distance(obj1, obj2):
    "Returns the euclidean distance between two colors"
    return 30 * (obj1[RGB_RED] - obj2[RGB_RED]) ** 2     + \
           59 * (obj1[RGB_GREEN] - obj2[RGB_GREEN]) ** 2 + \
           11 * (obj1[RGB_BLUE] - obj2[RGB_BLUE]) ** 2

def color_distance(obj1, obj2):
    """Returns the distance between two colors
    
    see http://www.compuphase.com/cmetric.htm
    """

    # convert the values in the 0-255 range
    obj1 = [int(math.ceil(obj1[RGB_RED] * 255)),
            int(math.ceil(obj1[RGB_GREEN] * 255)),
            int(math.ceil(obj1[RGB_BLUE] * 255))]
    obj2 = [int(math.ceil(obj2[RGB_RED] * 255)),
            int(math.ceil(obj2[RGB_GREEN] * 255)),
            int(math.ceil(obj2[RGB_BLUE] * 255))]

    rmean = obj1[RGB_RED] + obj2[RGB_RED] / 2
    r = obj1[RGB_RED] - obj2[RGB_RED]
    g = obj1[RGB_GREEN] - obj2[RGB_GREEN]
    b = obj1[RGB_BLUE] - obj2[RGB_BLUE]

    red_c = ((512 + rmean) * r * r) >> 8
    green_c = 4 * g * g
    blue_c = ((767 - rmean) * b * b) >> 8

    return math.sqrt(red_c + green_c + blue_c)


class KColorMeans(object):
    """
    Returns k clusters for the given color dataset
    """
    ALPHA_RATE = 0.9

    def __init__(self, k=3, distance=euclidean_color_distance):
        self.k = 3
        self.distance = distance
        random.seed()
        self.means = []

        for i in range(self.k):
            self.means.append([
                random.randint(0, 255) / 255.0,
                random.randint(0, 255) / 255.0,
                random.randint(0, 255) / 255.0,
            ])

    def fit(self, instance):
        "Add the instance to the dataset"
        instance = (instance[RGB_RED] / 255.0,
                    instance[RGB_GREEN] / 255.0,
                    instance[RGB_BLUE] / 255.0)

        # do not add every instance to the dataset as images have
        # (usually) many pixels. Add a random uniformly distributed
        # subset that covers 60% of the original image
        # TODO: maybe 60% is a too low threshold
        if random.random() > 0.6:
            return

        distances = [
            self.distance(self.means[i], instance)
            for i in range(self.k)
        ]
        # find the argmin
        min_idx = distances.index(min(distances))

        # update the mean for faster convergence (see Bishop)
        color_diff = map(operator.sub, instance, self.means[min_idx])
        alpha_vector = [self.ALPHA_RATE * x for x in color_diff]
        self.means[min_idx] = map(operator.add, self.means[min_idx], alpha_vector)

    def predict(self):
        "Returns k tuples, each corrisponding to a cluster"
        predictions = []
        for mean in self.means:
            predictions.append([
                int(math.ceil(mean[RGB_RED] * 255)),
                int(math.ceil(mean[RGB_GREEN] * 255)),
                int(math.ceil(mean[RGB_BLUE] * 255))
            ])
        return predictions


