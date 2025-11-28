import random
import pygame
import sys

pygame.init()

# Window
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Task 7 - Rectangle touches Triangle')
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (40, 160, 40)
TRI_COLOR = (30, 144, 255)    # original triangle color (DodgerBlue)
TRI_HIT_COLOR = (255, 215, 0) # hit color (Gold)

# Player rectangle (at the top, moves left/right)
PLAYER_W, PLAYER_H = 100, 24
player_x = (WIDTH - PLAYER_W) // 2
player_y = 20
player_speed = 6


def clamp(v, a, b):
    return max(a, min(b, v))


def make_triangle():
    # choose triangle bounding box
    tw = random.randint(80, 160)
    th = random.randint(60, 140)
    tx = random.randint(50, WIDTH - tw - 50)
    ty = random.randint(100, HEIGHT - th - 50)
    # define triangle points (isosceles pointing up)
    p1 = (tx + tw // 2, ty)
    p2 = (tx, ty + th)
    p3 = (tx + tw, ty + th)
    return {'points': (p1, p2, p3), 'bbox': (tx, ty, tw, th)}


def triangle_mask_from_points(points):
    surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (255, 255, 255, 255), points)
    mask = pygame.mask.from_surface(surf)
    return mask


def rect_mask(w, h):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(surf, (255, 255, 255, 255), (0, 0, w, h))
    return pygame.mask.from_surface(surf)


def main():
    global player_x

    triangle = make_triangle()
    tri_points = triangle['points']
    tri_mask = triangle_mask_from_points(tri_points)

    rect_m = rect_mask(PLAYER_W, PLAYER_H)

    tri_color = TRI_COLOR
    hit_time = None
    HIT_DURATION = 2000  # ms

    font = pygame.font.SysFont(None, 28)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        # keep player inside window
        player_x = clamp(player_x, 0, WIDTH - PLAYER_W)

        # collision detection using masks
        # tri_mask is full-screen mask with triangle drawn at its absolute positions
        # rect_mask anchored at (player_x, player_y)
        overlap_point = tri_mask.overlap(rect_m, (int(player_x), int(player_y)))
        now = pygame.time.get_ticks()
        if overlap_point and hit_time is None:
            # started hit
            hit_time = now
            tri_color = TRI_HIT_COLOR

        # if hit and duration passed, reset color
        if hit_time is not None and now - hit_time >= HIT_DURATION:
            tri_color = TRI_COLOR
            hit_time = None

        # draw
        SCREEN.fill(WHITE)

        # draw triangle
        pygame.draw.polygon(SCREEN, tri_color, tri_points)

        # draw player rect
        pygame.draw.rect(SCREEN, PLAYER_COLOR, (int(player_x), int(player_y), PLAYER_W, PLAYER_H))

        # instructions
        txt = font.render('Move: ← → or A D    Touch triangle to change its color (2s)', True, BLACK)
        SCREEN.blit(txt, (10, HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
