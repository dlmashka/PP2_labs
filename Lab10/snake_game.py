import random
import time
import datetime
import pygame
import psycopg2
from contextlib import contextmanager

# - DATABASE -
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'Lab10_PP2',
    'user': 'postgres',
    'password': 'Dimash2406'
}

@contextmanager
def get_conn_cursor():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    try:
        cur = conn.cursor()
        yield conn, cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def create_tables():
    sql_users = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    """
    sql_scores = """
    CREATE TABLE IF NOT EXISTS user_scores (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id),
        score INT DEFAULT 0,
        level INT DEFAULT 1,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_conn_cursor() as (conn, cur):
        cur.execute(sql_users)
        cur.execute(sql_scores)

def get_or_create_user(username):
    with get_conn_cursor() as (conn, cur):
        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
        row = cur.fetchone()
        if row:
            return row[0]
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        return cur.fetchone()[0]

def get_last_score(user_id):
    with get_conn_cursor() as (conn, cur):
        cur.execute("SELECT score, level FROM user_scores WHERE user_id=%s ORDER BY saved_at DESC LIMIT 1", (user_id,))
        row = cur.fetchone()
        if row:
            return row
        return 0, 1

def save_score(user_id, score, level):
    with get_conn_cursor() as (conn, cur):
        cur.execute(
            "INSERT INTO user_scores (user_id, score, level, saved_at) VALUES (%s, %s, %s, %s)",
            (user_id, score, level, datetime.datetime.now())
        )

# --------------------- PYGAME SETUP ---------------------
pygame.init()
WIDTH, HEIGHT = 800, 800
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake v0.1 with DB")
clock = pygame.time.Clock()
BLOCK_SIZE = 40

# --------------------- CLASSES ---------------------
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Food:
    def __init__(self, x, y, type):
        self.location = Point(x, y)
        self.type = type
        self.time = time.time()

    @property
    def x(self):
        return self.location.x
    @property
    def y(self):
        return self.location.y

    def update(self):
        color = YELLOW if self.type==1 else RED
        pygame.draw.rect(
            SCREEN, color,
            pygame.Rect(self.location.x*BLOCK_SIZE, self.location.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        )

class Snake:
    def __init__(self):
        self.points = [Point(WIDTH//BLOCK_SIZE//2, HEIGHT//BLOCK_SIZE//2),
                       Point(WIDTH//BLOCK_SIZE//2 + 1, HEIGHT//BLOCK_SIZE//2)]
        self.occupied_squares = set()
        self.food_eaten = 0
        self.level = 1

    def update(self):
        head = self.points[0]
        pygame.draw.rect(SCREEN, RED, pygame.Rect(head.x*BLOCK_SIZE, head.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for body in self.points[1:]:
            pygame.draw.rect(SCREEN, BLUE, pygame.Rect(body.x*BLOCK_SIZE, body.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        self.occupied_squares = set((p.x,p.y) for p in self.points)

    def move(self, dx, dy):
        for idx in range(len(self.points)-1,0,-1):
            self.points[idx].x = self.points[idx-1].x
            self.points[idx].y = self.points[idx-1].y
        self.points[0].x += dx
        self.points[0].y += dy
        head = self.points[0]
        if head.x <0 or head.x>=WIDTH//BLOCK_SIZE or head.y<0 or head.y>=HEIGHT//BLOCK_SIZE:
            return False

    def check_collision(self, food):
        return self.points[0].x == food.x and self.points[0].y == food.y

# --------------------- FUNCTIONS ---------------------
def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (x,0),(x,HEIGHT),1)
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (0,y),(WIDTH,y),1)

def get_counter_text(snake):
    font = pygame.font.SysFont('Arial',30)
    count_text = font.render(f"{snake.food_eaten}", True, WHITE)
    SCREEN.blit(count_text,(20,0))
    level_text = font.render(f"Level: {snake.level}", True, WHITE)
    SCREEN.blit(level_text,(700,0))

def get_end_text():
    font = pygame.font.SysFont('Arial',100)
    end_text = font.render('END', True, RED)
    rect = end_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(end_text, rect)

def generate_food_position(snake):
    x = random.randint(0, WIDTH//BLOCK_SIZE -1)
    y = random.randint(0, HEIGHT//BLOCK_SIZE -1)
    if (x,y) in snake.occupied_squares:
        return generate_food_position(snake)
    return x,y

# --------------------- MAIN GAME ---------------------
def main():
    create_tables()
    username = input("Введите имя игрока: ").strip()
    user_id = get_or_create_user(username)
    score, level = get_last_score(user_id)
    print(f"Добро пожаловать, {username}! Уровень: {level}, Очки: {score}")

    snake = Snake()
    snake.food_eaten = score
    snake.level = level
    food = Food(5,5,1)
    dx,dy = 0,0
    multip_time = 3
    paused = False
    running = True

    while running:
        SCREEN.fill(BLACK)
        get_counter_text(snake)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                save_score(user_id, snake.food_eaten, snake.level)
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP: dx,dy=0,-1
                elif event.key==pygame.K_DOWN: dx,dy=0,1
                elif event.key==pygame.K_LEFT: dx,dy=-1,0
                elif event.key==pygame.K_RIGHT: dx,dy=1,0
                elif event.key==pygame.K_s:  # Сохраняем очки
                    save_score(user_id, snake.food_eaten, snake.level)
                    print("Очки сохранены!")
                elif event.key==pygame.K_p:  # Пауза
                    paused = not paused

        if not paused:
            if snake.move(dx,dy) == False:
                get_end_text()

            if snake.check_collision(food):
                snake.points.append(Point(food.x, food.y))
                snake.food_eaten += 1 if food.type==1 else 2
                if food.type==2:
                    snake.points.append(Point(food.x,food.y))
                x,y = generate_food_position(snake)
                food.location.x = x
                food.location.y = y
                food.type = 1 if random.randint(1,10)>2 else 2
                if snake.food_eaten %4==0:
                    snake.level +=1
                    multip_time *=1.5

            if time.time()-food.time>5:
                x,y = generate_food_position(snake)
                food.location.x=x
                food.location.y=y
                food.type = 1 if random.randint(1,10)>2 else 2
                food.time = time.time()

        food.update()
        snake.update()
        draw_grid()
        pygame.display.flip()
        clock.tick(multip_time)

if __name__=='__main__':
    main()
