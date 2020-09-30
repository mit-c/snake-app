import pygame


class Snake:

    def __init__(self, pos, direction, length, memory, speed, radius):
        self.pos = pos
        self.direction = direction
        self.length = length
        self.memory = memory
        self.speed = speed
        self.radius = radius
        self.snake_coords = []
        self.time_gap = round((1 / self.speed) * radius)

    def change_dir(self, event):
        key_dict = {273: (0, -1), 275: (1, 0), 276: (-1, 0), 274: (0, 1)}  # swapped up and down
        key_pressed = event.dict['key']
        if key_pressed in key_dict.keys():
            human_key = key_dict[key_pressed]
            if self.direction[0] != -human_key[0] and self.direction[1] != -human_key[1]:
                self.direction = human_key

    def move(self):
        self.memory.append(self.pos)
        self.make_snake_coords()

        self.pos = (self.pos[0] + self.speed * self.direction[0], self.pos[1] + self.speed * self.direction[1])

    def make_snake_coords(self):  # creates snake cords from existing memory
        time_gap = self.time_gap

        mem_copy = self.memory[-time_gap * self.length - time_gap:: 1]

        self.snake_coords = mem_copy[:-time_gap:time_gap]


class SnakeGame:
    def __init__(self, screen, snake, foods, food_radius, game_map):
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

    def draw(self):
        food_radius = self.food_radius
        snake_radius = self.snake.radius
        self.screen.fill((255, 255, 255))

        for snake_pos in self.snake.snake_coords:

            pygame.draw.circle(self.screen, (0, 255, 0), (round(snake_pos[0]), round(snake_pos[1])), snake_radius)
            for food in self.foods:
                pygame.draw.circle(self.screen, (0, 0, 255), food, food_radius)

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

            xdiff = xfood - xsnake
            ydiff = yfood - ysnake

            if check_collision_circle(food, snake_position, food_radius, snake_radius):
                self.snake.length += 1
                self.foods.remove(food)

    def show_stats(self):
        print("length of memory: ", len(self.snake.memory))
        print("length of snake ", self.snake.length)
        print("snake cords ", self.snake.snake_coords)

    def check_snake_death(self):
        # Cases for snake death: hit map (will implement later), snake head hit snake.
        epsilon = 3
        snake_coords = self.snake.snake_coords.copy()

        snake_head = snake_coords[0]
        snake_coords.remove(snake_head)
        if snake_coords:
            for snake_coord in snake_coords:
                if check_collision_circle(snake_head, snake_coord, self.snake.radius + epsilon,
                                          self.snake.radius + epsilon):
                    print("snake on snake")
                    return True

        for line in self.game_map:
            if check_collision_map(snake_head, self.snake.radius, line):
                print("map", line)
                return True
        return False


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

    if dx == 0: # we have straight line up so easy to check i.e. we have y= y_0
        if radius1**2 > ycoordStart ** 2:

            xsol1 = (radius1 ** 2 - ycoordStart**2)**0.5
            xsol2 = -(radius1 ** 2 - ycoordStart**2)**0.5
            print("1st xsol", xsol1, "2nd xsol", xsol2, "xstart", ycoordStart, "xend", ycoordEnd)
            print(xcoordStart <= xsol1 <= xcoordEnd)
            if -radius1 <= xsol1 <= radius1 or -radius1 <= xsol2 <= radius1:
                return True
            else:
                return False
        else:
            return False
    # need to fix following logic. Also should implement for snake collision taxicab distance not hypotenuse.
    m = dy / dx
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
        if not xcoordStart <= x_sol1 <= xcoordEnd:
            return False
        else:
            y_sol1 = m * x_sol1 + c
            if not ycoordStart <= y_sol1 <= ycoordEnd:
                return False
            else:
                True

        x_sol2 = (-disc_b - disc ** 0.5) / (2 * disc_a)
        if not xcoordStart <= x_sol2 <= xcoordEnd:
            return False
        else:
            y_sol2 = m * x_sol2 + c
            if not ycoordStart <= y_sol2 <= ycoordEnd:
                return False
            else:
                True
