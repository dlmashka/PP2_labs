import pygame                     # Импортируем библиотеку pygame для работы с графикой
from datetime import datetime     # Импортируем datetime для получения текущего времени
pygame.init()                     # Инициализируем все модули pygame

size = (1120, 820)                # Размер окна приложения (ширина, высота)

screen = pygame.display.set_mode(size)  # Создаем окно указанного размера
pygame.display.set_caption("Clock")     # Устанавливаем заголовок окна

done = False                      # Переменная-флаг для завершения основного цикла
while not done:                   # Главный цикл программы (работает пока done == False)
    for event in pygame.event.get():     # Получаем список всех событий
        if event.type == pygame.QUIT:    # Если нажата кнопка закрытия окна
            done = True                 # Завершаем цикл и программу

    screen.fill((255, 255, 255))         # Очищаем экран и заливаем его белым цветом

    date = datetime.now()                # Получаем текущее время
    minutes = date.minute                # Получаем количество минут
    seconds = date.second                # Получаем количество секунд
    hours = date.hour                    # Получаем количество часов

    # Загружаем изображение циферблата
    clock = pygame.image.load(
        r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 7\MickeyPNG\mickeyclock_body.png'
    )

    # Загружаем изображение левой руки (секундная стрелка)
    left = pygame.image.load(
        r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 7\MickeyPNG\mmc_left.png'
    )
    left_copy = pygame.transform.rotate(left, seconds * (-6))  
    # Поворачиваем руку: 1 секунда = 6°, знак минус — чтобы вращение было по часовой стрелке

    # Загружаем изображение правой руки (минутная стрелка)
    right = pygame.image.load(
        r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 7\MickeyPNG\mmc_right.png'
    )
    right_copy = pygame.transform.rotate(right, minutes * (-6))
    # Поворачиваем минутную стрелку: 1 минута = 6°

    # Загружаем изображение третьей руки (часовая стрелка)
    third = pygame.image.load(
        r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 7\MickeyPNG\mmc_right.png'
    )
    third_copy = pygame.transform.rotate(third, hours * (-30) + (minutes * -0.5))
    # Поворачиваем часовую стрелку:
    # 1 час = 30°, добавляем смещение минут: 1 минута = 0.5°

    # Отрисовываем циферблат (смещаем для правильного позиционирования)
    screen.blit(clock, (-150, -110))

    # Отрисовываем секундную стрелку в центре
    screen.blit(
        left_copy,
        (555 - int(left_copy.get_width() / 2), 415 - int(left_copy.get_height() / 2))
    )

    # Отрисовываем минутную стрелку
    screen.blit(
        right_copy,
        (555 - int(right_copy.get_width() / 2), 415 - int(right_copy.get_height() / 2))
    )

    # Отрисовываем часовую стрелку
    screen.blit(
        third_copy,
        (555 - int(third_copy.get_width() / 2), 415 - int(third_copy.get_height() / 2))
    )

    pygame.display.flip()         # Обновляем экран и показываем все изменения

pygame.quit()                     # Корректно завершаем работу pygame
