# coding : utf-8

import math

# Задача-1: Написать класс для фигуры-треугольника, заданного координатами трех точек.
# Определить методы, позволяющие вычислить: площадь, высоту и периметр фигуры.

print('Задача-1: Треугольник: периметр, высоты, площадь')
print('---------------------------------------------------------------------------------')


class Side:
    @staticmethod
    def side(x, y):
        return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


class Triangle(Side):
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c
        self.ab = self.side(a, b)
        self.bc = self.side(b, c)
        self.ca = self.side(c, a)

    @property
    def perimetr(self):
        return self.ab + self.bc + self.ca

    def height(self, side):
        """Вычисление высоты через сторону side (ее задаем при вызове функции)"""
        half_p = triang.perimetr / 2
        return 2 * math.sqrt(half_p * (half_p - self.ab) * (half_p - self.bc) * (half_p - self.ca)) / side

    @property
    def area(self):
        """Вычисление площади треугольника"""
        return (self.ab * triang.height(self.ab)) / 2


triang = Triangle((0, 0), (0, 5), (5, 5))
print(triang.ab, triang.bc, triang.ca)
print(triang.perimetr)
print(triang.height(triang.ab))
print(triang.area)

print('---------------------------------------------------------------------------------')

# Задача-2: Написать Класс "Равнобочная трапеция", заданной координатами 4-х точек.
# Предусмотреть в классе методы:
# проверка, является ли фигура равнобочной трапецией;
# вычисления: длины сторон, периметр, площадь.

print('Задача-2: Равнобедренная трапеция: проверка на равнобедренность, периметр, высоты, площадь')
print('---------------------------------------------------------------------------------')


class Trapeze(Side):
    def __init__(self, a, b, c, d):
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        self.ab = self.side(a, b)
        self.bc = self.side(b, c)
        self.cd = self.side(c, d)
        self.da = self.side(d, a)

    @property
    def perimetr(self):
        return self.ab + self.bc + self.cd + self.da

    @property
    def area(self):
        second_side = math.sqrt(trap.ab ** 2 - ((trap.da - trap.bc) ** 2) / 4)
        return ((trap.bc + trap.da) / 2) * second_side

    @staticmethod
    def degree(side_1, side_2):
        return math.tan(side_1 / side_2)

    def true_trapeze(self):
        """Проверка на то, что четырехугльник - равнобедренная трапеция"""
        if self.ab == self.cd and self.degree(self.ab, self.da) == self.degree(self.cd, self.da):
            return True
        else:
            return False


trap = Trapeze((0, 0), (3, 6), (6, 6), (9, 0))
print(trap.bc, trap.ab, trap.da)
if trap.true_trapeze() is True:
    print('Трапеция - равнобедренная')
else:
    print('Трапеция - не равнобедренная')
print('Периметр трапеции =', trap.perimetr)
print('Площадь трапеции =', trap.area)
