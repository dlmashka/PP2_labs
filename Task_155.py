import pygame  # Библиотека Pygame для создания игр (окно, ввод, отрисовка)
import sys

pygame.init()

# --- Настройки окна и цвета ---
WIDTH, HEIGHT = 800, 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Task 15 - Hamster')




        # draw click counter
        text = font.render(f'Clicks: {clicks}', True, BLACK)
        SCREEN.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    run_click_rectangle()

