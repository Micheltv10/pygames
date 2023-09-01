from src.figure import Figure
class Tetris:
    width = 0
    height = 0
    field = []
    score = 0
    state = "start"
    figure = None

    def __init__(self, _height, _width):
        self.height = _height
        self.width = _width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.field.append(new_line)
        self.new_figure()

    def new_figure(self):
        self.figure = Figure(2, 0)

    def side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def left(self):
        self.side(-1)

    def right(self):
        self.side(1)

    def drop(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i2 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i2][j] = self.field[i2 - 1][j]
        self.score += lines ** 2

    def freeze(self):
        for i in range(4):
            for j in range(4):
                p = 4 * i + j
                if p in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"
            print("Game over!")

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                p = 4 * i + j
                if p in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection