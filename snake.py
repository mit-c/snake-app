import pygame
import random
import snake_classes as snake

pygame.init()
# ctrl + alt + L reformats.
w = 400
h = 400
screen = pygame.display.set_mode([w, h])
game_map = [((0, 0), (w, 0)), ((w, 0), (w, h)), ((w, h), (0, h)), ((0, h), (0, 0)),
            ((round(w / 2), h), (round(w / 2), h - round(h / 3)))]

my_memory = []
my_snake = snake.Snake(pos=(w // 2, h // 2), direction=(0, 1), length=1, memory=my_memory, speed=0.05, radius=7)
game_of_snake = snake.SnakeGame(screen=screen, snake=my_snake, foods=[(10, 10), (20, 20), (30, 30)], food_radius=5,
                                game_map=game_map, high_score=0, width=w, height=h)
# food_radius = 5
# snake_radius = 10
game_of_snake.start(game_of_snake)

pygame.quit()
