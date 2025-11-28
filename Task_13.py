import random  # Модуль для генерации случайных чисел (используется для случайной позиции еды)
import time    # Модуль для работы со временем (используется для таймера появления еды)

import pygame  # Библиотека Pygame для создания игр (окно, ввод, отрисовка)

pygame.init()

# --- Настройки окна и цвета ---
WIDTH, HEIGHT = 800, 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Task 13 - Click the Rectangle')

# --- Основная функция игры ---
def run_click_rectangle(): 
    rect_w, rect_h = 150, 100 
    # start centered
    rect_x = (WIDTH - rect_w) // 2 
    rect_y = (HEIGHT - rect_h) // 2
    rect_color = RED
    clicks = 0

    font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    # toggle color between RED and GREEN
                    rect_color = GREEN if rect_color == RED else RED
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # check if click inside rectangle
                if rect_x <= mx <= rect_x + rect_w and rect_y <= my <= rect_y + rect_h:
                    clicks += 1
                    # move to random position fully inside screen
                    rect_x = random.randint(0, WIDTH - rect_w)
                    rect_y = random.randint(0, HEIGHT - rect_h)

        SCREEN.fill(WHITE)

        # draw rectangle
        pygame.draw.rect(SCREEN, rect_color, (rect_x, rect_y, rect_w, rect_h))

        # draw click counter
        text = font.render(f'Clicks: {clicks}', True, BLACK)
        SCREEN.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    run_click_rectangle()
