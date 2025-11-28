import pygame
import sys

pygame.init()

# Window
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Task 15 - Hamster')
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HAM_COLOR = (255, 0, 0)  # Hamster color (Red)  


def clamp(v, a, b): 
    return max(a, min(b, v)) # clamp value v between a and b


def run():
    # hamster parameters
    base_r = 30
    hamster_x = WIDTH // 2
    hamster_y = HEIGHT // 2
    clicks = 0

    grown = False # has the hamster grown
    moved = False # has the hamster moved
    moving = False # is the hamster currently moving
    move_target_x = hamster_x # target x position when moving
    move_speed = 4 # pixels per frame

    font = pygame.font.SysFont(None, 36) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # current radius
                cur_r = base_r * (2 if grown else 1)
                # check click inside hamster
                dx = mx - hamster_x
                dy = my - hamster_y
                if dx * dx + dy * dy <= cur_r * cur_r:
                    clicks += 1
                    # on 5 clicks grow x2 (only once)
                    if clicks >= 5 and not grown:
                        grown = True
                    # on 10 clicks move right for 50px (only once)
                    if clicks >= 10 and not moved and not moving:
                        move_target_x = clamp(hamster_x + 50, cur_r, WIDTH - cur_r)
                        moving = True

        # handle movement animation
        if moving:
            # move hamster_x towards move_target_x
            if abs(move_target_x - hamster_x) <= move_speed:
                hamster_x = move_target_x
                moving = False
                moved = True
            else:
                dir = 1 if move_target_x > hamster_x else -1
                hamster_x += move_speed * dir

        # draw
        SCREEN.fill(WHITE)

        cur_r = base_r * (2 if grown else 1)
        pygame.draw.circle(SCREEN, HAM_COLOR, (int(hamster_x), int(hamster_y)), cur_r)

        # draw score
        txt = font.render(f'Hamster Coins: {clicks}', True, BLACK)
        SCREEN.blit(txt, (10, 10))

        # small instructions
        ins = font.render('Click the hamster. ESC to quit.', True, BLACK)
        SCREEN.blit(ins, (10, HEIGHT - 36))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    run()
