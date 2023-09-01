import random

import pygame

from src.Ball import Ball
from src.Player import Player

window_width = 800
window_height = 600
speed = 120
score = 0
pygame.init()
pygame.display.set_caption("pong")
window = pygame.display.set_mode((window_width, window_height))
refresh_controller = pygame.time.Clock()
p_width = 20
p_height = 100
player1 = Player(p_width, window_height / 2 - p_height / 2, 1)
player2 = Player(window_width - p_width * 2, window_height / 2 - p_height / 2, 2)
Ball = Ball(window_width / 2, window_height / 2)


def paint_hud():
    font = pygame.font.SysFont('Arial', 20)
    render = font.render(F"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    window.blit(render, rect)

    pygame.display.flip()


def repaint():
    window.fill(pygame.Color(0, 0, 0))
    pygame.draw.rect(window, pygame.Color(255, 255, 255),
                     pygame.Rect(player1.x, player1.y, player1.width, player1.height))
    pygame.draw.rect(window, pygame.Color(255, 255, 255),
                     pygame.Rect(player2.x, player2.y, player2.width, player2.height))
    pygame.draw.circle(window, pygame.Color(255, 255, 255), (Ball.x, Ball.y), Ball.radius)
    pygame.draw.aaline(window, pygame.Color(255, 255, 255), (window_width / 2, 0), (window_width / 2, window_height))
    pygame.display.flip()


def handle_keys():
    global score
    print("Score: 0")
    events = pygame.event.get()
    print("Score: 0.5")
    for e in events:
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                player1.press_up = True
            if e.key == pygame.K_DOWN:
                player1.press_down = True
            if e.key == pygame.K_w:
                player2.press_up = True
            if e.key == pygame.K_s:
                player2.press_down = True
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_UP:
                player1.press_up = False
            if e.key == pygame.K_DOWN:
                player1.press_down = False
            if e.key == pygame.K_w:
                player2.press_up = False
            if e.key == pygame.K_s:
                player2.press_down = False
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()
    player1.move()
    if Ball.intersects([player1, player2]):
        Ball.bounce_x()
        score += 1
    if Ball.y <= 0 or Ball.y >= window_height:
        Ball.bounce_y()
    player2.move()


def create_text(text, font_size, color, x, y):
    font = pygame.font.SysFont('Arial', font_size)
    render = font.render(text, True, color)
    rect = render.get_rect()
    rect.midtop = (x, y)
    window.blit(render, rect)
    pygame.display.flip()


def game_over():
    if Ball.x - Ball.radius <= 0 or Ball.x + Ball.radius >= window_width:
        return False
    else:
        return True


def game_over_message():
    create_text("Game Over", 50, pygame.Color(255, 255, 255), window_width / 2, window_height / 2)
    create_text("Press Space to Play Again", 20, pygame.Color(255, 255, 255), window_width / 2, window_height / 2 + 50)
    pygame.display.flip()


def reset():
    Ball.x = window_width / 2
    Ball.y = window_height / 2
    Ball.velocity_x = random.choice([-1, 1])
    Ball.velocity_y = random.choice([-1, 1])
    player1.x = p_width
    player1.y = window_height / 2 - p_height / 2
    player2.x = window_width - p_width * 2
    player2.y = window_height / 2 - p_height / 2
    player1.press_up = False
    player1.press_down = False
    player2.press_up = False
    player2.press_down = False
    score = 0


def game_loop():
    running = True
    reset()
    global score
    while running:
        handle_keys()
        print("Score: 1")
        Ball.move()
        print("Score: 2")
        repaint()
        print("Score: 3")
        paint_hud()
        print("Score: 4")
        running = game_over()
        print(running)
        print("Score: 5")
        refresh_controller.tick(speed)
        print("Score: 6")
        print(running)
        # print("Ball x and y: ", Ball.x, Ball.y)
        # print("Player 1 x and y: ", player1.x, player1.y)
        # print("Player 2 x and y: ", player2.x, player2.y)

    while not running:
        game_over_message()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    game_loop()


if __name__ == "__main__":
    game_loop()
