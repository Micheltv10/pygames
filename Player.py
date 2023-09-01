class Player():

    def __init__(self, x_pos, y_pos, id):
        self.x = x_pos
        self.y = y_pos
        self.id = id
        self.height = 100
        self.width = 20
        self.press_up = False
        self.press_down = False

    def move(self):
        old_y = self.y
        old_x = self.x
        if self.press_up and not self.press_down:
            self.y -= 2
            if self.y < 0:
                self.y = old_y
            print("UP")
        if self.press_down and not self.press_up:
            self.y += 2
            if self.y > 600 - self.height:
                self.y = old_y
            print("DOWN")