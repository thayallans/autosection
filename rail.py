from typing import Callable
import math


class Rail:
    name = "Rail"

    def __init_(self, fun: Callable, distance):
        self.fun = fun
        self.total_distance = distance

    def get(self, position: float):
        return self.fun(position)


class LeftRail(Rail):
    name = "LeftRail"

    def __init__(self, transform):
        self.outside_len = 100
        self.inside_width = 100
        self.curve_length = (2 * math.pi * 75) / 4
        self.total_distance = self.outside_len * 2 + self.curve_length

        self.cutoffs = [100, 100 + self.curve_length]
        self.inner_start = (-25, -50)
        self.transform = transform

        self.cache = {}

    def applyTransform(self, x, y, transform):
        for i in range(transform):
            x, y = -1 * y, x
        return x, y

    def get(self, scalar):
        if scalar in self.cache:
            return self.cache[scalar]
        if scalar < self.cutoffs[0]:
            x_cord = 0 - (self.outside_len - scalar + self.inside_width / 2)
            y_cord = -25
            r = self.applyTransform(x_cord, y_cord, self.transform)
        elif scalar > self.cutoffs[1]:
            len_left = self.total_distance - scalar
            y_cord = self.outside_len - len_left + self.inside_width / 2
            x_cord = 25
            r = self.applyTransform(x_cord, y_cord, self.transform)
        else:
            prop_dist = (scalar - self.cutoffs[0]) / self.curve_length
            angle = math.radians(90) * prop_dist
            x_cord = 0 - self.inside_width / 2 + 75 * math.sin(angle)
            y_cord = self.inside_width / 2 - 75 * math.cos(angle)
            r = self.applyTransform(x_cord, y_cord, self.transform)
        self.cache[scalar] = r
        return r

    def __hash__(self):
        return hash(self.name + str(self.transform))  # LeftRail3

    def __eq__(self, other):
        return self.name == other.name and self.transform == other.transform


class RightRail(Rail):
    name = "RightRail"

    def __init__(self, transform):
        self.outside_len = 100
        self.inside_width = 100
        self.curve_length = (2 * math.pi * 25) / 4
        self.total_distance = self.outside_len * 2 + self.curve_length
        self.cutoffs = [100, 100 + self.curve_length]
        self.inner_start = (-25, -50)
        self.transform = transform

    def applyTransform(self, x, y, transform):
        for i in range(transform + 1):
            x, y = -1 * y, x
        return x, y

    def get(self, scalar):
        scalar = self.total_distance - scalar
        if scalar < self.cutoffs[0]:
            x_cord = 0 - (self.outside_len - scalar + self.inside_width / 2)
            y_cord = 25
            return self.applyTransform(x_cord, y_cord, self.transform)
        elif scalar > self.cutoffs[1]:
            y_cord = scalar - self.cutoffs[1] + self.inside_width / 2
            x_cord = -25
            return self.applyTransform(x_cord, y_cord, self.transform)
        else:
            prop_dist = (scalar - self.cutoffs[0]) / self.curve_length
            angle = math.radians(90) * prop_dist
            x_cord = 0 - self.inside_width / 2 + 25 * math.sin(angle)
            y_cord = self.inside_width / 2 - 25 * math.cos(angle)
            return self.applyTransform(x_cord, y_cord, self.transform)

    def __hash__(self):
        return hash(self.name + str(self.transform))  # RightRail0

    def __eq__(self, other):
        return self.name == other.name and self.transform == other.transform
