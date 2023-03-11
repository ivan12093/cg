import math
from math import pi
from dataclasses import dataclass


@dataclass
class Point2D:
    x: float
    y: float

    def __str__(self):
        return f"({self.x}, {self.y})"

    @staticmethod
    def dist(a: "Point2D", b: "Point2D"):
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


class Vector:
    def __init__(self, start: Point2D, end: Point2D):
        self.start = start
        self.end = end
        self.x = end.x - start.x
        self.y = end.y - start.y

    # | a.x a.y |
    # | b.x b.y |
    @staticmethod
    def skew_product(vec_a: "Vector", vec_b: "Vector"):
        return vec_a.x * vec_b.y - vec_b.x * vec_a.y

    def point_pos(self, point: Point2D):
        """
        :param point: точка, относительную позицию которой надо вычислить
        :return: отрицательное значение, если точка ниже вектора, положительное значение если выше, 0
        если лежит на прямой
        """
        fake_vec = Vector(self.start, point)
        skew_product = self.skew_product(self, fake_vec)
        return skew_product

    def length(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5


def select_line_from_points(points: list[Point2D]):
    """
    Выбирает такие две точки из множества, что линия проходящая через них
    делит множество точек на два множество, разность мощностей которых минимальна
    :param points: множество точек
    :return: индексы двух точек
    """
    if len(points) < 2:
        raise Exception('минимум должно быть две точки')
    min_diff = float('inf')
    res_a = 0
    res_b = 1
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            upper = lower = 0
            vec = Vector(points[i], points[j])
            for k in range(len(points)):
                if k == i or k == j:
                    continue
                point_pos = vec.point_pos(points[k])
                if point_pos < 0:
                    lower += 1
                elif point_pos > 0:
                    upper += 1
            diff = abs(upper - lower)
            if diff < min_diff:
                min_diff = diff
                res_a = i
                res_b = j
    return res_a, res_b


def divide_points_by_vec(points: list[Point2D], vec: Vector):
    """
    :param points: точки которые надо поделить
    :param vec: вектор которым делим
    :return: три множества: точки под, на, над прямой, образованной вектором
    """
    lower, on, upper = [], [], []
    for p in points:
        p_pos = vec.point_pos(p)
        if p_pos < 0:
            lower.append(p)
        elif p_pos > 0:
            upper.append(p)
        else:
            on.append(p)
    return lower, on, upper


class Circle:
    def __init__(self, center: Point2D, radius: float):
        self.center = center
        self.radius = radius

    def is_point_in(self, point: Point2D):
        x_diff = point.x - self.center.x
        y_diff = point.y - self.center.y
        distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
        return distance <= self.radius

    def square(self):
        return int(pi * self.radius ** 2)

    @staticmethod
    def intersection_square(a: "Circle", b: "Circle"):
        D = Point2D.dist(a.center, b.center)

        F1 = 2 * math.acos((a.radius ** 2 - b.radius ** 2 + D ** 2) / (2 * a.radius * D))
        F2 = 2 * math.acos((b.radius ** 2 - a.radius ** 2 + D ** 2) / (2 * b.radius * D))

        S1 = a.radius ** 2 * (F1 - math.sin(F1)) / 2
        S2 = b.radius ** 2 * (F2 - math.sin(F2)) / 2

        return S1 + S2

    @staticmethod
    def total_area(a: "Circle", b: "Circle"):
        S1 = a.square()
        S2 = b.square()
        try:
            intrt = Circle.intersection_square(a, b)
        except Exception as e:
            print(e)
            intrt = 0
        return int(S1 + S2 - intrt)

    @staticmethod
    def circle_with_diameter_on(q1: Point2D, q2: Point2D):
        vec = Vector(q1, q2)
        center = Point2D(x=q1.x + vec.x / 2, y=q1.y + vec.y / 2)
        radius = ((vec.x / 2) ** 2 + (vec.y / 2) ** 2) ** 0.5
        print(center, radius, vec.x, vec.y)
        print(q1, q2)
        return Circle(center, radius)

    @staticmethod
    def circle_with_3_points(q1: Point2D, q2: Point2D, q3: Point2D):
        x1 = q1.x
        x2 = q2.x
        x3 = q3.x
        y1 = q1.y
        y2 = q2.y
        y3 = q3.y
        x0 = -(1 / 2) * (y1 * (x2 ** 2 - x3 ** 2 + y2 ** 2 - y3 ** 2) + y2 *
                         (-x1 ** 2 + x3 ** 2 - y1 ** 2 + y3 ** 2) + y3 *
                         (x1 ** 2 - x2 ** 2 + y1 ** 2 - y2 ** 2)) / (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

        y0 = (1 / 2) * (x1 * (x2 ** 2 - x3 ** 2 + y2 ** 2 - y3 ** 2) + x2 *
                        (-x1 ** 2 + x3 ** 2 - y1 ** 2 + y3 ** 2) + x3 * (x1 ** 2 - x2 ** 2 + y1 ** 2 - y2 ** 2)) / (
                         x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

        radius = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        return Circle(Point2D(x0, y0), radius)

    @staticmethod
    def min_circle_with_2_points(points: list[Point2D], q1: Point2D, q2: Point2D):
        min_circle = Circle.circle_with_diameter_on(q1, q2)
        for p in points:
            if not min_circle.is_point_in(p):
                min_circle = Circle.circle_with_3_points(p, q1, q2)
        return min_circle

    @staticmethod
    def min_circle_with_point(points: list[Point2D], q: Point2D):
        min_circle = Circle.circle_with_diameter_on(points[0], q)
        for i in range(1, len(points)):
            if not min_circle.is_point_in(points[i]):
                min_circle = Circle.min_circle_with_2_points(points[:i], points[i], q)
        return min_circle

    @staticmethod
    def min_circle(points: list[Point2D]):
        if len(points) < 1:
            raise Exception('точек не должно быть меньше 1')
        if len(points) < 2:
            return Circle(points[0], 0)
        min_circle = Circle.circle_with_diameter_on(points[0], points[1])
        for i in range(2, len(points)):
            if not min_circle.is_point_in(points[i]):
                min_circle = Circle.min_circle_with_point(points[:i], points[i])
        return min_circle
