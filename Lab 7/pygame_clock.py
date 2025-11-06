import pygame
from datetime import datetime
pygame.init()

size = (1120, 820)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Clock")

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((255, 255, 255))
    date = datetime.now()
    minutes = date.minute
    seconds = date.second #+ date.microsecond / 1_000_000  # Добавляем долю секунды для плавности
    clock = pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\MickeyClock_2\MickeyPNG\mickeyclock_body.png')
    left = pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\MickeyClock_2\MickeyPNG\mmc_left.png')
    left_copy = pygame.transform.rotate(left, seconds * (-6))
    right = pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\MickeyClock_2\MickeyPNG\mmc_right.png')
    right_copy = pygame.transform.rotate(right, minutes * (-6))
    screen.blit(clock, (-100, -100))
    screen.blit(left_copy, (605 - int(left_copy.get_width() / 2), 425 - int(left_copy.get_height() / 2)))
    screen.blit(right_copy, (605 - int(right_copy.get_width() / 2), 425 - int(right_copy.get_height() / 2)))

    pygame.display.flip()
pygame.quit()
