import random

class Figure:
    x = 0
    y = 0
    Figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 8, 9], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 2, 5, 6]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],

    ]

    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.type = random.randint(0, len(self.Figures) - 1)
        self.color = self.type + 3
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.Figures[self.type])

    def image(self):
        return self.Figures[self.type][self.rotation]


