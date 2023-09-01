import pygame
from src.tetris import Tetris


def high_score(score):
    with open('high_score.txt', 'r') as file:
        old_high_score = int(file.read())
    if score > old_high_score:
        with open('high_score.txt', 'w') as file:
            file.write(str(score))
        return score
    else:
        return old_high_score


def create_text(text, font_size, color, x, y):
    font = pygame.font.SysFont('Arial', font_size)
    render = font.render(text, True, color)
    rect = render.get_rect()
    rect.midtop = (x, y)
    screen.blit(render, rect)
    pygame.display.flip()


def game_over_message():
    create_text('Game Over', 30, pygame.Color(255, 255, 255), window_width / 2, window_height / 2)
    create_text(F'Score: {game.score}', 30, pygame.Color(255, 255, 255), window_width / 2, window_height / 2 - 40)
    create_text(F'High Score: {high_score(game.score)}', 30, pygame.Color(255, 255, 255), window_width / 2, window_height / 2 - 80)


def paint_hud():
    create_text(F'Score: {game.score}', 30, pygame.Color(255, 255, 255), window_width / 2, 20)


pygame.init()
window_width = 360
window_height = 660
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")

done = False
clock = pygame.time.Clock()
counter = 0
zoom = 30
fps = 3

game = Tetris(20, 10)

pressing_left = False
pressing_right = False
pressing_down = False
pressing_up = False

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

colors = [
    (0, 0, 0),
    (120, 120, 120),
    (255, 255, 255),
    (255, 0, 0),
    (0, 150, 0),
    (0, 0, 255),
    (255, 120, 0),
    (255, 255, 0),
    (180, 0, 255),
    (0, 220, 220)
]
while not done:
    if game.state == "start":
        game.drop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_LEFT:
                game.left()
            if event.key == pygame.K_RIGHT:
                game.right()
            if event.key == pygame.K_DOWN:
                game.drop()
            if event.key == pygame.K_UP:
                game.rotate()

    screen.fill(colors[0])
    for i in range(game.height):
        for j in range(game.width):
            if game.field[i][j] == 0:
                color = colors[1]
                just_border = 1
            else:
                color = colors[game.field[i][j]]
                just_border = 0
            pygame.draw.rect(screen, color, [zoom * (j + 1), zoom * (i + 1), zoom, zoom], just_border)
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = 4 * i + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [zoom * (j + game.figure.x + 1), zoom * (i + game.figure.y + 1), zoom, zoom])
    paint_hud()
    pygame.display.flip()
    clock.tick(fps)
    if game.state == "gameover":
        pygame.time.wait(1000)
        done = True
while done:
    game_over_message()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
pygame.quit()
