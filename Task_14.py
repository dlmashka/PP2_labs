import random
import pygame

pygame.init()

# --- Настройки ---
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (50, 120, 200)
ENEMY_COLOR = (200, 50, 50)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Task 14 - Ball vs Rectangles')


def clamp(v, a, b):
    return max(a, min(b, v))


def circle_rect_collision(cx, cy, r, rx, ry, rw, rh):
    nearest_x = clamp(cx, rx, rx + rw)
    nearest_y = clamp(cy, ry, ry + rh)
    dx = cx - nearest_x
    dy = cy - nearest_y
    return dx * dx + dy * dy <= r * r


def make_enemy():
    w = random.randint(100, 180)
    h = random.randint(20, 40)
    x = random.randint(WIDTH, WIDTH + 600)
    y = random.randint(0, HEIGHT - h)
    s = random.uniform(3.0, 6.0)
    return {'x': x, 'y': y, 'w': w, 'h': h, 's': s}


def run():
    # player ball
    ball_r = 20
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed = 6

    # enemies
    enemies = [make_enemy() for _ in range(4)]

    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 72)

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    # restart
                    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                    enemies = [make_enemy() for _ in range(4)]
                    game_over = False
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                ball_x -= ball_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                ball_x += ball_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                ball_y -= ball_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                ball_y += ball_speed

            # keep inside window
            ball_x = clamp(ball_x, ball_r, WIDTH - ball_r)
            ball_y = clamp(ball_y, ball_r, HEIGHT - ball_r)

            # update enemies (move right->left)
            for e in enemies:
                e['x'] -= e['s']
                if e['x'] + e['w'] < 0:
                    # respawn on the right
                    new = make_enemy()
                    e.update(new)

            # collision check
            for e in enemies:
                if circle_rect_collision(ball_x, ball_y, ball_r, e['x'], e['y'], e['w'], e['h']):
                    game_over = True
                    break

        # draw
        SCREEN.fill(WHITE)
        for e in enemies:
            pygame.draw.rect(SCREEN, ENEMY_COLOR, (int(e['x']), int(e['y']), e['w'], e['h']))

        pygame.draw.circle(SCREEN, BALL_COLOR, (int(ball_x), int(ball_y)), ball_r)

        if game_over:
            go = big_font.render('GAME OVER', True, (180, 0, 0))
            sub = font.render('Press R to restart or ESC to quit', True, BLACK)
            SCREEN.blit(go, ((WIDTH - go.get_width()) // 2, (HEIGHT - go.get_height()) // 2 - 30))
            SCREEN.blit(sub, ((WIDTH - sub.get_width()) // 2, (HEIGHT - sub.get_height()) // 2 + 40))

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    run()
