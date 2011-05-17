"""
An implementation of the k-means algorithm for predominant color extraction
"""

import random
import math
import operator
from PIL import Image, ImageEnhance

RGB_RED, RGB_GREEN, RGB_BLUE = 0, 1, 2

def euclidean_color_distance(obj1, obj2):
    "Returns the euclidean distance between two colors"
    return (obj1[RGB_RED] - obj2[RGB_RED]) ** 2     + \
           (obj1[RGB_GREEN] - obj2[RGB_GREEN]) ** 2 + \
           (obj1[RGB_BLUE] - obj2[RGB_BLUE]) ** 2

def color_distance(obj1, obj2):
    """Returns the distance between two colors

    This is more accurate than the euclidean distance but it also
    considerably slower, even though gives a faster convergence.
    See http://www.compuphase.com/cmetric.htm
    """

    # convert the values in the 0-255 range
    obj1 = [int(math.ceil(obj1[RGB_RED])),
            int(math.ceil(obj1[RGB_GREEN])),
            int(math.ceil(obj1[RGB_BLUE]))]
    obj2 = [int(math.ceil(obj2[RGB_RED])),
            int(math.ceil(obj2[RGB_GREEN])),
            int(math.ceil(obj2[RGB_BLUE]))]

    rmean = obj1[RGB_RED] + obj2[RGB_RED] / 2
    r = obj1[RGB_RED] - obj2[RGB_RED]
    g = obj1[RGB_GREEN] - obj2[RGB_GREEN]
    b = obj1[RGB_BLUE] - obj2[RGB_BLUE]

    red_c = ((512 + rmean) * r * r) >> 8
    green_c = 4 * g * g
    blue_c = ((767 - rmean) * b * b) >> 8

    return math.sqrt(red_c + green_c + blue_c)


class Classifier(object):
    """Returns k clusters for the given color dataset

    Use the k-means algorithm to extract the k dominant colors.
    """

    LEARNING_RATE = 0.8

    def __init__(self, k=3, distance=euclidean_color_distance):
        self.k = k
        self.distance = distance
        random.seed()
        self.means = []

        # initialize the means to random values
        for i in range(self.k):
            self.means.append([
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ])

    def fit(self, instance):
        "Add the instance to the dataset"
        instance = (instance[RGB_RED],
                    instance[RGB_GREEN],
                    instance[RGB_BLUE])

        distances = [
            self.distance(self.means[i], instance)
            for i in range(self.k)
        ]

        # find the argmin
        min_idx = distances.index(min(distances))

        # update the mean online for faster convergence, see
        # @book{bishop2007,
        #   author = {Christopher M. Bishop},
        #   publisher = {Springer},
        #   title = {Pattern Recognition and Machine Learning},
        #   year = 2007,
        #   isbn = {0387310738},
        # }
        color_diff = map(operator.sub, instance, self.means[min_idx])
        learning_vector = [self.LEARNING_RATE * x for x in color_diff]
        self.means[min_idx] = map(operator.add, self.means[min_idx], learning_vector)

    def predict(self):
        "Returns k color tuples, each corrisponding to a cluster"
        predictions = []
        for mean in self.means:
            predictions.append([
                int(math.ceil(mean[RGB_RED])),
                int(math.ceil(mean[RGB_GREEN])),
                int(math.ceil(mean[RGB_BLUE]))
            ])
        return predictions


