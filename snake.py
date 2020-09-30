import pygame
import random
import snake_classes as snake

pygame.init()
# ctrl + alt + L reformats.
w = 500
h = 500
screen = pygame.display.set_mode([w, h])
game_map = [((0, 0), (w, 0)), ((w, 0), (w, h)), ((w, h), (0, h)), ((0, h), (0, 0))]

running = True
my_memory = [(250, 250), (220, 220), (150, 200)]
my_snake = snake.Snake(pos=(250, 250), direction=(0, 1), length=1, memory=my_memory, speed=0.1, radius=7)
game_of_snake = snake.SnakeGame(screen=screen, snake=my_snake, foods=[(10, 10), (20, 20), (30, 30)], food_radius=5,
                                game_map=game_map)
# food_radius = 5
# snake_radius = 10
count = 0
random.seed(a=1)

while running:
    count += 1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            game_of_snake.snake.change_dir(event)

        if event.type == pygame.QUIT:
            running = False
    if count % 1000 == 0 and len(game_of_snake.foods) < 5:
        game_of_snake.foods.append((random.randint(0, 500), random.randint(0, 500)))
    game_of_snake.eat_food()
    game_of_snake.snake.move()



    #game_of_snake.show_stats()
    game_of_snake.draw()
    if not game_of_snake.snake.snake_coords == [] and game_of_snake.check_snake_death():
        print("Game ended")
    pygame.display.flip()

pygame.quit()
