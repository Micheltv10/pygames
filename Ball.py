class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_x = 1
        self.velocity_y = 1
        self.radius = 10

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y


    def bounce_y(self):
        self.velocity_y *= -1

    def bounce_x(self):
        self.velocity_x *= -1

    def intersects(self, players):
        for player in players:
            if player.id == 1:
                if self.x - self.radius <= player.x + player.width and player.y <= self.y <= player.y + player.height:
                    return True
            if player.id == 2:
                if self.x + self.radius >= player.x and player.y <= self.y <= player.y + player.height:
                    return True
        return False
