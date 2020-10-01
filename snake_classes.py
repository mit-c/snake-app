import pygame
import random


class Snake:

    def __init__(self, pos, direction, length, memory, speed, radius):
        self.pos = pos
        self.direction = direction
        self.length = length
        self.memory = memory
        self.speed = speed
        self.radius = radius
        self.snake_coords = []
        self.time_gap = round((1 / self.speed) * radius * 2.1)

    def change_dir(self, event):
        key_dict = {273: (0, -1), 275: (1, 0), 276: (-1, 0), 274: (0, 1)}  # swapped up and down
        wasd_key_dict = {100: (1, 0), 119: (0, -1), 97: (-1, 0), 115: (0, 1)}
        key_dict.update(wasd_key_dict)
        key_pressed = event.dict['key']
        if key_pressed in key_dict.keys():
            human_key = key_dict[key_pressed]
            if self.direction[0] != -human_key[0] and self.direction[1] != -human_key[1]:
                self.direction = human_key

    def move(self):
        self.memory.append(self.pos)
        time_gap = self.time_gap
        del self.memory[:(-time_gap) * self.length]
        # This deletes really old snake memory.#
        mem_copy = self.memory.copy()
        self.snake_coords = mem_copy[::-time_gap]
        # Fixed problem with slicing!!!
        self.pos = (self.pos[0] + self.speed * self.direction[0], self.pos[1] + self.speed * self.direction[1])


class SnakeGame:

    def __init__(self, screen, snake, foods, food_radius, game_map, high_score, width, height):
        '''

        :param screen:  pygame screen object
        :param snake: my snake object
        :param food: list of positions of food
        '''
        self.screen = screen
        self.snake = snake
        self.foods = foods
        self.game_map = game_map  # pairs of coordinates to draw line between. Should be scaled based on game size. #screen.get_height/get_width
        self.food_radius = food_radius
        self.state = "Alive"
        self.high_score = high_score
        self.width = width
        self.height = height

    def draw(self):
        food_radius = self.food_radius
        snake_radius = self.snake.radius
        background_colour = (255, 255, 255)
        line_colour = (0, 0, 0)
        if self.state == "Death by snake":
            background_colour = (255, 0, 0)

        if self.state == "Death by wall":
            background_colour = (0, 0, 0)
            line_colour = (255, 255, 255)
        self.screen.fill(background_colour)
        for line in self.game_map:
            pygame.draw.line(self.screen, line_colour, line[0], line[1], 10)
        counter = 0
        for snake_pos in self.snake.snake_coords:
            if(counter == 0): # can make patterns using %
                snake_col = (255,0,0)
            else:
                snake_col = (0, 255,0)
            pygame.draw.circle(self.screen, snake_col, (round(snake_pos[0]), round(snake_pos[1])), snake_radius)
            for food in self.foods:
                pygame.draw.circle(self.screen, (0, 0, 255), food, food_radius)
            counter += 1

    def eat_food(self):
        snake_position = self.snake.pos
        food_list = self.foods
        food_radius = self.food_radius
        snake_radius = self.snake.radius

        for food in food_list:
            xfood = food[0]
            yfood = food[1]

            xsnake = snake_position[0]
            ysnake = snake_position[1]

            if check_collision_circle_taxicab(food, snake_position, food_radius + snake_radius):
                self.snake.length += 1
                self.foods.remove(food)

    def show_stats(self):
        print("length of memory: ", len(self.snake.memory))
        # print("length of snake ", self.snake.length)
        # print("snake cords ", self.snake.snake_coords)

    def check_snake_death(self):
        # Cases for snake death: hit map (will implement later), snake head hit snake.
        epsilon = 3
        snake_coords = self.snake.snake_coords.copy()

        snake_head = snake_coords[0]
        snake_coords.remove(snake_head)
        if snake_coords:
            for snake_coord in snake_coords:
                taxicab_dist = self.snake.radius * 2
                if check_collision_circle_taxicab(snake_head, snake_coord, dist=taxicab_dist):
                    self.state = "Death by snake"
                    return True

        for line in self.game_map:
            if check_collision_map(snake_head, self.snake.radius, line):
                self.state = "Death by wall"
                return True

        return False

    def start(self, my_game):
        self = my_game
        w = self.width
        h = self.height
        running = True
        count = 0
        random.seed(a=1)
        start_time = 0
        event_memory = []
        key_lag = 180

        pygame.display.set_caption("Snake!")
        while running:
            count += 1
            # store every event in memory
            # access memory every key_lag ms.
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    event_memory.append(event)
                if event.type == pygame.QUIT:
                    running = False
            end_time = pygame.time.get_ticks()
            diff = end_time - start_time
            if (diff > key_lag) and event_memory:
                mem_event = event_memory.pop(0)
                self.snake.change_dir(mem_event)
                start_time = end_time

            if count % 5000 == 0:
                self.foods.pop(0)
            if count % 1000 == 0:
                if len(self.foods) < 5:
                    self.foods.append((random.randint(0, w), random.randint(0, h)))
            self.eat_food()
            self.snake.move()
            end_time_moving = pygame.time.get_ticks()

            self.draw()
            start_time_moving = end_time_moving
            pygame.display.flip()

            self.show_stats()

            if not self.snake.snake_coords == [] and self.check_snake_death():
                dead = True
                white = (255, 255, 255)
                blue = (0, 0, 255)
                red = (255, 0, 0)
                green = (0, 255, 0)
                gold = (255, 223, 0)
                emerald = (255 * 0, 255 * 0.6, 255 * 0.11)
                if self.snake.length > self.high_score:
                    self.high_score = self.snake.length
                    text_col = gold
                    background_col = emerald
                    string1 = "New High Score"
                else:
                    text_col = white
                    background_col = red
                    string1 = "Game Over"
                font = pygame.font.Font("freesansbold.ttf", 32)

                string2 = "Score: " + str(self.snake.length)
                string3 = "High Score: " + str(self.high_score)
                string4 = self.state

                text1, textRect1 = create_text(string1, 32, (w // 2, h // 5), text_col, background_col)
                text2, textRect2 = create_text(string2, 32, (w // 2, h // 2), text_col, background_col)
                text3, textRect3 = create_text(string3, 32, (w // 2, 3 * h // 4), text_col, background_col)
                text4, textRect4 = create_text(string4, 32, (w // 2, h // 3), text_col, background_col)
                while dead:
                    self.screen.fill(background_col)
                    self.screen.blit(text1, textRect1)
                    self.screen.blit(text2, textRect2)
                    self.screen.blit(text3, textRect3)
                    self.screen.blit(text4, textRect4)
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            dead = False
                            running = False

                        if event.type == pygame.KEYDOWN and event.dict['key'] == 13:
                            dead = False
                newSnake = Snake(pos=(w // 2, h // 2), direction=(0, 1), length=1, memory=[],
                                 speed=0.05,
                                 radius=7)
                newGame = SnakeGame(screen=self.screen, snake=newSnake, foods=[(10, 10), (20, 20), (30, 30)],
                                    food_radius=5,
                                    game_map=self.game_map, high_score=self.high_score, width=w,
                                    height=h)
                if running:
                    self.start(newGame)

                print("Game ended")

        pygame.quit()


def check_collision_circle_taxicab(pos1, pos2, dist):
    xpos1 = pos1[0]
    ypos1 = pos1[1]

    xpos2 = pos2[0]
    ypos2 = pos2[1]

    xdiff = abs(xpos1 - xpos2)
    ydiff = abs(ypos1 - ypos2)

    return True if xdiff + ydiff < dist else False


def check_collision_circle(pos1, pos2, radius1, radius2):
    xpos1 = pos1[0]
    ypos1 = pos1[1]

    xpos2 = pos2[0]
    ypos2 = pos2[1]

    xdiff = abs(xpos1 - xpos2)
    ydiff = abs(ypos1 - ypos2)

    return True if xdiff ** 2 + ydiff ** 2 < (radius1 + radius2) ** 2 else False


def check_collision_map(pos, radius1, line):  # line is defined by start and end points
    xcoord1 = pos[0]
    ycoord1 = pos[1]

    xcoordStart = line[0][0] - xcoord1
    ycoordStart = line[0][1] - ycoord1

    xcoordEnd = line[1][0] - xcoord1
    ycoordEnd = line[1][1] - ycoord1

    dy = ycoordEnd - ycoordStart
    dx = xcoordEnd - xcoordStart

    if dx == 0:  # we have straight line up so easy to check i.e. we have x=x0

        if radius1 ** 2 > xcoordStart ** 2:
            ysol1 = (radius1 ** 2 - xcoordStart ** 2) ** 0.5
            ysol2 = - ysol1
            if min(ycoordStart, ycoordEnd) <= (ysol1) <= max(ycoordStart, ycoordEnd) or min(ycoordStart,
                                                                                            ycoordEnd) <= ysol2 <= max(
                ycoordStart, ycoordEnd):
                return True
            else:
                return False
        else:
            return False

    # need to fix following logic. Also should implement for snake collision taxicab distance not hypotenuse.
    m = dy / dx
    if m == 0:  # x constant
        if radius1 ** 2 > ycoordStart ** 2:

            xsol1 = (radius1 ** 2 - ycoordStart ** 2) ** 0.5
            xsol2 = -xsol1

            if -radius1 <= xsol1 <= radius1 or -radius1 <= xsol2 <= radius1:
                return True
            else:
                return False
        else:
            return False
    # y = m x + c
    c = ycoordStart - m * xcoordStart
    # solve equation then check in interval
    disc_c = c * c - radius1 * radius1
    disc_a = 1 + m * m
    disc_b = 2 * m * c
    disc = disc_b * disc_b - 4 * disc_a * disc_c

    if disc < 0:
        return False
    else:

        x_sol1 = (-disc_b + disc ** 0.5) / (2 * disc_a)

        if not min(xcoordStart, xcoordEnd) <= x_sol1 <= max(xcoordStart, xcoordEnd):
            return False
        else:

            y_sol1 = m * x_sol1 + c
            if not min(ycoordStart, ycoordEnd) <= y_sol1 <= max(ycoordStart, ycoordEnd):
                return False
            else:
                return True

        x_sol2 = (-disc_b - disc ** 0.5) / (2 * disc_a)
        if not xcoordStart <= x_sol2 <= xcoordEnd:
            return False
        else:
            y_sol2 = m * x_sol2 + c
            if not ycoordStart <= y_sol2 <= ycoordEnd:
                return False
            else:
                True


def create_text(text, font_size, pos, colour, back_col):
    font = pygame.font.Font("freesansbold.ttf", font_size)
    string_to_disp = text
    text = font.render(string_to_disp, True, colour, back_col)
    textRect = text.get_rect()
    textRect.center = pos
    return text, textRect
