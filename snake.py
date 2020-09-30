import pygame
import snake_classes as snake
pygame.init()
# ctrl + alt + L reformats.
screen = pygame.display.set_mode([500, 500])
running = True

snake = snake.Snake((250, 250), (0, 1), [])
game_of_snake = snake.SnakeGame(screen, snake, [])
while running:
    for event in pygame.event.get():
        print(event.dict)



        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (250, 250), 75)

    pygame.display.flip()
pygame.quit()
