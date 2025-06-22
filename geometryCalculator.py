import math


class GeometryCalculator:
    def calculate_circle_area(self, radius):

        return math.pi * radius**2

    def calculate_rectangle_area(self, length, width):

        return length * width


if __name__ == "__main__":

    calculator = GeometryCalculator()
