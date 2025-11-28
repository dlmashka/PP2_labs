import pygame
import sys

pygame.init()

# Window
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Task 6 - Coin Collector')
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (50, 150, 50)
COIN_COLOR = (212, 175, 55)

# Player (rectangle at the top)
PLAYER_W, PLAYER_H = 100, 20
player_x = (WIDTH - PLAYER_W) // 2
player_y = 20
player_speed = 7

# Coins: each coin is dict {'x', 'y', 'vy', 'r'}
coins = []
GRAVITY = 0.4

# Score
score = 0

font = pygame.font.SysFont(None, 36)


def spawn_coin(x, y):
    # spawn coin slightly below the player
    return {'x': x, 'y': y, 'vy': 0.0, 'r': 8}


def draw():
    SCREEN.fill(WHITE)

    # draw player
    pygame.draw.rect(SCREEN, PLAYER_COLOR, (player_x, player_y, PLAYER_W, PLAYER_H))

    # draw coins
    for c in coins:
        pygame.draw.circle(SCREEN, COIN_COLOR, (int(c['x']), int(c['y'])), c['r'])

    # draw floor line
    pygame.draw.line(SCREEN, BLACK, (0, HEIGHT - 2), (WIDTH, HEIGHT - 2), 2)

    # draw score
    txt = font.render(f'Coins: {score}', True, BLACK)
    SCREEN.blit(txt, (10, 10))

    # instructions
    ins = font.render('Move: ← → or A D    Drop: SPACE', True, BLACK)
    SCREEN.blit(ins, (10, HEIGHT - 40))


def update_physics():
    global score
    # update coins
    to_remove = []
    for i, c in enumerate(coins):
        c['vy'] += GRAVITY
        c['y'] += c['vy']

        # if coin touches floor (bottom of window)
        if c['y'] + c['r'] >= HEIGHT - 2:
            score += 1
            to_remove.append(i)

    # remove collected coins (from end to start)
    for i in reversed(to_remove):
        coins.pop(i)


def main():
    global player_x
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # drop a coin from center-bottom of player rectangle
                    cx = player_x + PLAYER_W // 2
                    cy = player_y + PLAYER_H + 5
                    coins.append(spawn_coin(cx, cy))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        # keep player inside window
        player_x = max(0, min(WIDTH - PLAYER_W, player_x))

        update_physics()
        draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
