import random
import time

import pygame

pygame.init()
WIDTH, HEIGHT = 800, 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
BLOCK_SIZE = 40
pygame.display.set_caption('Snake v0')


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Food:
    def __init__(self, x, y, type):
        self.location = Point(x, y)
        self.type = type #if 1-normal if 2-big
        self.time = time.time()

    @property
    def x(self):
        return self.location.x

    @property
    def y(self):
        return self.location.y

    def update(self):
        if(self.type == 1):
            pygame.draw.rect(
                SCREEN,
                YELLOW,
                pygame.Rect(
                    self.location.x * BLOCK_SIZE,
                    self.location.y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
            )
        else:
            pygame.draw.rect(
                SCREEN,
                RED,
                pygame.Rect(
                    self.location.x * BLOCK_SIZE,
                    self.location.y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
            )


class Snake:
    def __init__(self):
        self.points = [
            Point(WIDTH // BLOCK_SIZE // 2, HEIGHT // BLOCK_SIZE // 2),
            Point(WIDTH // BLOCK_SIZE // 2 + 1, HEIGHT // BLOCK_SIZE // 2),
        ]
        self.occupied_squares = set()
        self.food_eaten = 0
        self.level = 0

    def update(self):
        head = self.points[0]

        pygame.draw.rect(
            SCREEN,
            RED,
            pygame.Rect(
                head.x * BLOCK_SIZE,
                head.y * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE,
            )
        )
        for body in self.points[1:]:
            pygame.draw.rect(
                SCREEN,
                BLUE,
                pygame.Rect(
                    body.x * BLOCK_SIZE,
                    body.y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
            )
        
        self.occupied_squares = set() # Clear set of occupied squares
        for point in self.points:
            self.occupied_squares.add((point.x, point.y))

    def move(self, dx, dy):
        for idx in range(len(self.points) - 1, 0, -1):
            self.points[idx].x = self.points[idx - 1].x
            self.points[idx].y = self.points[idx - 1].y

        self.points[0].x += dx
        self.points[0].y += dy

        head = self.points[0]
        if head.x > WIDTH // BLOCK_SIZE:
            return False
        elif head.x < 0:
            return False
        elif head.y > HEIGHT // BLOCK_SIZE:
            return False
        elif head.y < 0:
            return False

    def check_collision(self, food):
        if self.points[0].x != food.x:
            return False
        if self.points[0].y != food.y:
            return False
        return True


def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (x, 0), (x, HEIGHT), width=1)
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (0, y), (WIDTH, y), width=1)

def get_counter_text(snake):
    counter = snake.food_eaten
    level = snake.level
    font = pygame.font.SysFont('Arial', 30)

    count_text = font.render(str(counter), True, WHITE)
    count_text_rect = count_text.get_rect(center=(20, 20))
    level_text = font.render(str(level), True, WHITE)
    level_text_rect = level_text.get_rect(center=(780, 20))
    SCREEN.blit(count_text, count_text_rect)
    SCREEN.blit(level_text, level_text_rect)

def get_end_text():
    font = pygame.font.SysFont('Arial', 100)
    end_text = font.render('END', True, RED)
    end_text_rect = end_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(end_text, end_text_rect)

def generate_food_position(snake): 
    x_food = random.randint(0, WIDTH // BLOCK_SIZE - 1) 
    y_food = random.randint(0, HEIGHT // BLOCK_SIZE - 1) 
    postion = (x_food, y_food)

    if postion in snake.occupied_squares:
        return generate_food_position(snake)
    elif x_food > WIDTH // BLOCK_SIZE: 
        return generate_food_position(snake)
    elif x_food < 0: 
        return generate_food_position(snake) 
    elif y_food > HEIGHT // BLOCK_SIZE: 
        return generate_food_position(snake) 
    elif y_food < 0: 
        return generate_food_position(snake) 

    return x_food, y_food

def main():
    running = True
    snake = Snake()
    food = Food(5, 5, 1)
    dx, dy = 0, 0
    multip_time = 1

    while running:
        SCREEN.fill(BLACK)
        get_counter_text(snake)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN:
                    dx, dy = 0, +1
                elif event.key == pygame.K_LEFT:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT:
                    dx, dy = +1, 0

        if(snake.move(dx, dy) == False):
            get_end_text()
            

        if snake.check_collision(food):
            if(food.type == 2):
                snake.points.append(Point(food.x, food.y))
                snake.points.append(Point(food.x, food.y))
                snake.food_eaten += 2
            else:
                snake.points.append(Point(food.x, food.y))
                snake.food_eaten += 1

            x_food, y_food = generate_food_position(snake)
            type_of_food = random.randint(1, 10) 

            food.location.x = x_food 
            food.location.y = y_food
            food.time = time.time()
            if(type_of_food > 2): 
                food.type = 1
            else:
                food.type = 2

            if(snake.food_eaten % 4 == 0):
                snake.level += 1
                multip_time *= 1.5

        if(time.time() - food.time > 5):
            x_food, y_food = generate_food_position(snake)
            type_of_food = random.randint(1, 10) 

            food.location.x = x_food 
            food.location.y = y_food
            food.time = time.time()
            if(type_of_food > 2): 
                food.type = 1
            else:
                food.type = 2

        food.update()
        snake.update()
        draw_grid()

        pygame.display.flip()
        clock.tick(3*multip_time)


if __name__ == '__main__':
    main()