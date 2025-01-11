import random
import time
import pygame
from enum import Enum
import sqlite3

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


speed = 12
scale = 20
window_width = scale * 40
window_height = scale * 20
pygame.init()
pygame.display.set_caption("Snake")
window = pygame.display.set_mode((window_width, window_height))
refresh_controller = pygame.time.Clock()

global score
global name
name = "None"
score = 0

snake_position = [window_width/2, window_height/2]
snake_body = [[window_width/2, window_height/2],
              [window_width/2 - scale, window_height/2],
              [window_width/2 - scale*2, window_height/2],
              [window_width/2 - scale*3, window_height/2]]

def save_score(score):
    date = time.strftime("%d/%m/%Y")
    con = sqlite3.connect('scores.db')
    cur = con.cursor()
    cur.execute("INSERT INTO score (name, score, date) VALUES (?, ?, ?)", (name, score, date))
    con.commit()
    con.close()

def high_score():
    con = sqlite3.connect('scores.db')
    cur = con.cursor()
    cur.execute("SELECT MAX(score) FROM score")
    high_score = cur.fetchone()
    con.close()
    print(high_score)
    return high_score[0]


def handle_keys(direction):
    events = pygame.event.get()
    new_direction = direction
    for e in events:
        match e.type:
            case pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction != Direction.DOWN:
                    new_direction = Direction.UP
                if e.key == pygame.K_DOWN and direction != Direction.UP:
                    new_direction = Direction.DOWN
                if e.key == pygame.K_LEFT and direction != Direction.RIGHT:
                    new_direction = Direction.LEFT
                if e.key == pygame.K_RIGHT and direction != Direction.LEFT:
                    new_direction = Direction.RIGHT
            case pygame.QUIT:
                pygame.quit()
                quit()
    return new_direction      
         
    
def move_snake(direction):
    if direction == Direction.UP:
        snake_position[1] -= scale
    if direction == Direction.DOWN:
        snake_position[1] += scale
    if direction == Direction.LEFT:
        snake_position[0] -= scale
    if direction == Direction.RIGHT:
        snake_position[0] += scale
    snake_body.insert(0, list(snake_position))


def eat(food_position):
    global score
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += 1
        food_position = [random.randrange(3, window_width/scale) * scale, random.randrange(3, window_height/scale) * scale]
        return food_position
    else:
        snake_body.pop()
        return food_position


def repaint(food_position):
    window.fill(pygame.Color(0, 0, 0))
    for pos in snake_body:
        pygame.draw.rect(window, pygame.Color(0, 255, 0), pygame.Rect(pos[0], pos[1], scale, scale))
    pygame.draw.rect(window, pygame.Color(255, 0, 0), pygame.Rect(food_position[0], food_position[1], scale, scale))
    pygame.display.flip()


def game_over():
    if (snake_position[0] < 0 or
        snake_position[0] > window_width - scale or
        snake_position[1] < 0 or
        snake_position[1] > window_height - scale):
        game_over_message()
        save_score(score)
        return False
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over_message()
            save_score(score)
            return False
    return True


def game_over_message():
    font = pygame.font.SysFont('Arial', 30)
    render = font.render(F'Game Over', True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    rect.midtop = (window_width / 2, window_height / 2)
    window.blit(render, rect)
    font = pygame.font.SysFont('Arial', 30)
    render = font.render(F'Score: {score}', True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    rect.midtop = (window_width / 2, window_height / 2 - scale*2 )
    window.blit(render, rect)
    font = pygame.font.SysFont('Arial', 30)
    render = font.render(F'High Score: {high_score()}', True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    rect.midtop = (window_width / 2, window_height / 2 - scale*4)
    window.blit(render, rect)
    pygame.display.flip()



def paint_hud():
    font = pygame.font.SysFont('Arial', scale)
    render = font.render(F"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    window.blit(render, rect)
    pygame.display.flip()


def game_loop():
    direction = Direction.RIGHT
    food_position = [random.randrange(3, window_width/scale) * scale, random.randrange(3, window_height/scale) * scale]
    running = True
    global score
    while running:
        direction = handle_keys(direction)
        move_snake(direction)
        food_position = eat(food_position)
        repaint(food_position)
        running = game_over()
        paint_hud()
        refresh_controller.tick(speed)
    while not running:
        game_over_message()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    snake_body.clear()
                    snake_position[0] = window_width/2
                    snake_position[1] = window_height/2
                    snake_body.insert(0, list(snake_position))
                    score = 0
                    game_loop()

if __name__ == "__main__":
    game_loop()
