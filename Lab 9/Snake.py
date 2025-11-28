import random  # Модуль для генерации случайных чисел (используется для случайной позиции еды)
import time    # Модуль для работы со временем (используется для таймера появления еды)

import pygame  # Библиотека Pygame для создания игр (окно, ввод, отрисовка)

pygame.init()  # Инициализируем все модули Pygame — нужно вызывать перед использованием функций библиотеки

# --- Настройки окна и цвета ---
WIDTH, HEIGHT = 800, 800           # Задаём ширину и высоту окна в пикселях
BLACK = (0, 0, 0)                  # RGB-цвет для чёрного
WHITE = (255, 255, 255)            # RGB-цвет для белого
RED = (255, 0, 0)                  # RGB-цвет для красного
BLUE = (0, 0, 255)                 # RGB-цвет для синего
YELLOW = (255, 255, 0)             # RGB-цвет для жёлтого

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаём окно с размерами WIDTH x HEIGHT
clock = pygame.time.Clock()                        # Объект Clock для управления FPS (частотой кадров)
BLOCK_SIZE = 40                                    # Размер одной клетки поля в пикселях
pygame.display.set_caption('Snake v0')             # Устанавливаем заголовок окна

# --- Класс Point: простая структура для хранения координат в клетках ---
class Point:
    def __init__(self, x, y):  # Конструктор класса Point принимает два числа — x и y
        self.x = x             # Сохраняем координату x (по горизонтали в клетках)
        self.y = y             # Сохраняем координату y (по вертикали в клетках)

# --- Класс Food: отвечает за еду (позицию, тип и время появления) ---
class Food:
    def __init__(self, x, y, type):   # Конструктор принимает координаты (x,y) и тип еды
        self.location = Point(x, y)   # Сохраняем позицию в виде объекта Point
        self.type = type              # type 1 — обычная еда, 2 — большая еда (даёт +2)
        self.time = time.time()       # Сохраняем время появления еды (в секундах с эпохи)

    @property
    def x(self):                      # Свойство x — удобный доступ к location.x
        return self.location.x       # Возвращаем x из объекта location

    @property
    def y(self):                      # Свойство y — удобный доступ к location.y
        return self.location.y       # Возвращаем y из объекта location

    def update(self):                 # Метод рисует еду на экране
        # Если тип 1 — рисуем желтым квадратом
        if self.type == 1:
            pygame.draw.rect(
                SCREEN,               # На каком Surface рисуем (наш экран)
                YELLOW,               # Цвет прямоугольника
                pygame.Rect(
                    self.location.x * BLOCK_SIZE,  # X в пикселях
                    self.location.y * BLOCK_SIZE,  # Y в пикселях
                    BLOCK_SIZE,                     # Ширина прямоугольника
                    BLOCK_SIZE,                     # Высота прямоугольника
                )
            )
        else:
            # Иначе (type == 2) — рисуем красным квадратом
            pygame.draw.rect(
                SCREEN,
                RED,
                pygame.Rect(
                    self.location.x * BLOCK_SIZE,  # X в пикселях
                    self.location.y * BLOCK_SIZE,  # Y в пикселях
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
            )

# --- Класс Snake: хранит сегменты змейки, логику движения и проверки ---
class Snake:
    def __init__(self):  # Конструктор создаёт начальное тело змейки и счётчики
        # Изначально создаём два сегмента: голова и один элемент тела, расположенные в центре
        self.points = [
            Point(WIDTH // BLOCK_SIZE // 2, HEIGHT // BLOCK_SIZE // 2),
            Point(WIDTH // BLOCK_SIZE // 2 + 1, HEIGHT // BLOCK_SIZE // 2),
        ]
        self.occupied_squares = set()  # Множество координат, занятых змейкой (tuple (x,y))
        self.food_eaten = 0            # Счётчик съеденной еды (целое число)
        self.level = 0                 # Уровень игры (увеличивается каждые 4 еды)

    def update(self):  # Метод отрисовки змейки и обновления occupied_squares
        head = self.points[0]  # Считаем первый элемент списка self.points головой
        # Рисуем голову как красный квадрат
        pygame.draw.rect(
            SCREEN,
            RED,
            pygame.Rect(
                head.x * BLOCK_SIZE,  # x в пикселях
                head.y * BLOCK_SIZE,  # y в пикселях
                BLOCK_SIZE,            # ширина
                BLOCK_SIZE,            # высота
            )
        )

        # Рисуем тело (все сегменты, кроме головы) синими квадратами
        for body in self.points[1:]:
            pygame.draw.rect(
                SCREEN,
                BLUE,
                pygame.Rect(
                    body.x * BLOCK_SIZE,  # x тела в пикселях
                    body.y * BLOCK_SIZE,  # y тела в пикселях
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
            )

        # Обновляем множество занятых клеток: очищаем и добавляем текущие координаты чтобы еда не появилась на змейке,проверки, не съела ли змейка сама себя.
        self.occupied_squares = set()            # Очищаем предыдущее множество
        for point in self.points:                # Проходимся по всем сегментам змейки
            self.occupied_squares.add((point.x, point.y))  # Добавляем кортеж (x,y) 

    def move(self, dx, dy):  # Метод перемещения змейки: dx, dy — смещение в клетках
        # Сдвигаем каждый сегмент на место предыдущего: идём с конца к началу
        for idx in range(len(self.points) - 1, 0, -1):  # i = last..1
            self.points[idx].x = self.points[idx - 1].x  # Копируем X предыдущего
            self.points[idx].y = self.points[idx - 1].y  # Копируем Y предыдущего

        # Теперь двигаем голову по заданному вектору (dx, dy)
        self.points[0].x += dx  # Изменяем X головы
        self.points[0].y += dy  # Изменяем Y головы

        head = self.points[0]  # Получаем обновлённую голову
        # Проверяем выход за границы поля (границы в клетках от 0 до WIDTH//BLOCK_SIZE - 1)
        if head.x > WIDTH // BLOCK_SIZE:  # Если X больше количества клеток по ширине
            return False                  # Возвращаем False — сигнал о выходе за границу
        elif head.x < 0:                  # Если X меньше 0 — вышли влево
            return False
        elif head.y > HEIGHT // BLOCK_SIZE:  # Если Y больше количества клеток по высоте
            return False
        elif head.y < 0:                    # Если Y меньше 0 — вышли вверх
            return False
        # Если всё в порядке — метод ничего не возвращает (возвращаем None)

    def check_collision(self, food):  # Метод проверки столкновения головы с едой
        # Если координата X головы не равна координате X еды — не столкновение
        if self.points[0].x != food.x:
            return False
        # Если координата Y головы не равна координате Y еды — не столкновение
        if self.points[0].y != food.y:
            return False
        # Если обе координаты совпали — возвращаем True (еда съедена)
        return True

# --- Вспомогательная функция: рисует сетку клеток на экране ---
def draw_grid():
    # Вертикальные линии (проходим по X с шагом BLOCK_SIZE)
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (x, 0), (x, HEIGHT), width=1)  # Линия сверху вниз
    # Горизонтальные линии (проходим по Y с шагом BLOCK_SIZE)
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (0, y), (WIDTH, y), width=1)  # Линия слева направо

# --- Рисуем счётчик (количество съеденной еды) и уровень ---
def get_counter_text(snake):
    counter = snake.food_eaten            # Получаем количество съеденной еды из объекта snake
    level = snake.level                   # Получаем уровень из объекта snake
    font = pygame.font.SysFont('Arial', 30)  # Создаём объект шрифта Arial размером 30

    # Рендерим текст количества еды в поверхность (surface) для последующего отображения
    count_text = font.render(str(counter), True, WHITE)
    # Получаем прямоугольник текста и ставим его в позицию center=(20,20)
    count_text_rect = count_text.get_rect(center=(20, 20))

    # Рендерим текст уровня и ставим его справа сверху
    level_text = font.render(str(level), True, WHITE)
    level_text_rect = level_text.get_rect(center=(780, 20))

    SCREEN.blit(count_text, count_text_rect)  # Отображаем текст счёта на экране
    SCREEN.blit(level_text, level_text_rect)  # Отображаем текст уровня на экране

# --- Рисуем текст 'END' по центру экрана при проигрыше ---
def get_end_text():
    font = pygame.font.SysFont('Arial', 100)  # Большой шрифт для надписи
    end_text = font.render('END', True, RED)  # Создаём поверхность с текстом 'END' красного цвета
    end_text_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Центрируем прямоугольник текста
    SCREEN.blit(end_text, end_text_rect)  # Рисуем текст на экране (показываем игроку)

# --- Генерация случайной позиции для еды (без попадания на змейку) ---
def generate_food_position(snake):
    x_food = random.randint(0, WIDTH // BLOCK_SIZE - 1)   # Случайный индекс клетки по X
    y_food = random.randint(0, HEIGHT // BLOCK_SIZE - 1)  # Случайный индекс клетки по Y

    position = (x_food, y_food)  # Объединяем в кортеж для удобной проверки

    # Если позиция попала на любую клетку змейки — рекурсивно генерируем новую
    if position in snake.occupied_squares:
        return generate_food_position(snake)
    # Дополнительные проверки на корректность координат (на случай ошибок)
    elif x_food > WIDTH // BLOCK_SIZE:
        return generate_food_position(snake)
    elif x_food < 0:
        return generate_food_position(snake)
    elif y_food > HEIGHT // BLOCK_SIZE:
        return generate_food_position(snake)
    elif y_food < 0:
        return generate_food_position(snake)

    # Возвращаем найденную корректную позицию
    return x_food, y_food

# --- Главная функция игры: создаёт объекты и запускает игровой цикл ---
def main():
    running = True  # Флаг, контролирующий выполнение игрового цикла
    snake = Snake()  # Создаём объект змейки
    food = Food(5, 5, 1)  # Создаём объект еды в позиции (5,5), тип 1
    dx, dy = 0, 0  # Начальное направление движения (нет движения)
    multip_time = 1.5  # Начальный множитель скорости (умножается на базовую частоту кадров)

    # Игровой цикл: выполняется до тех пор, пока running == True
    while running:
        SCREEN.fill(BLACK)  # Заполняем экран чёрным цветом — очищаем предыдущий кадр
        get_counter_text(snake)  # Отрисовываем счёт и уровень сверху

        # Обрабатываем все события, которые пришли от Pygame (нажатия, закрытие окна и т.д.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Если пользователь нажал на крестик окна
                running = False            # Выходим из игрового цикла

            if event.type == pygame.KEYDOWN:  # Если нажата какая-то клавиша
                if event.key == pygame.K_UP:    # Если клавиша стрелка вверх
                    dx, dy = 0, -1             # Движение вверх: dx=0, dy=-1 (уменьшаем y)
                elif event.key == pygame.K_DOWN:  # Стрелка вниз
                    dx, dy = 0, 1              # Движение вниз: увеличиваем y
                elif event.key == pygame.K_LEFT:  # Стрелка влево
                    dx, dy = -1, 0             # Движение влево: уменьшаем x
                elif event.key == pygame.K_RIGHT: # Стрелка вправо
                    dx, dy = 1, 0              # Движение вправо: увеличиваем x

        # Вызываем метод move; если метод вернул False — голова вышла за границу поля
        if snake.move(dx, dy) == False:
            get_end_text()  # Показываем текст 'END' (игра не завершается автоматически здесь)

        # Проверяем: съела ли змейка еду
        if snake.check_collision(food):
            # Если тип еды == 2 (большая) — добавляем два сегмента и даём +2 к счёту
            if food.type == 2:
                snake.points.append(Point(food.x, food.y))  # Добавляем новый сегмент с координатами еды
                snake.points.append(Point(food.x, food.y))  # Повторно добавляем — рост на 2
                snake.food_eaten += 2                        # Увеличиваем счёт на 2
            else:
                # Обычная еда — добавляем один сегмент, +1 к счёту
                snake.points.append(Point(food.x, food.y))
                snake.food_eaten += 1

            # Генерируем новую позицию для следующей еды
            x_food, y_food = generate_food_position(snake)
            type_of_food = random.randint(1, 10)  # Случайное число для определения типа еды

            food.location.x = x_food  # Обновляем координату X объекта еды
            food.location.y = y_food  # Обновляем координату Y объекта еды
            food.time = time.time()    # Обновляем время появления еды (новая метка времени)

            if type_of_food > 2:       # Если число больше 2 → обычная еда (~80% шанс)
                food.type = 1
            else:                      # Иначе — большая еда (~20% шанс)
                food.type = 2

            # Каждые 4 съеденные единицы повышаем уровень и ускоряем игру
            if snake.food_eaten % 4 == 0:
                snake.level += 1
                multip_time *= 1.5  # Увеличиваем множитель скорости

        # Если еда лежит дольше 5 секунд → переносим её в новое место
        if time.time() - food.time > 5:
            x_food, y_food = generate_food_position(snake)  # Новая позиция
            type_of_food = random.randint(1, 10)            # Новый тип еды

            food.location.x = x_food  # Присваиваем новую координату X
            food.location.y = y_food  # Присваиваем новую координату Y
            food.time = time.time()    # Обновляем время появления

            if type_of_food > 2:
                food.type = 1  # 80% — обычная еда
            else:
                food.type = 2  # 20% — большая еда

        # Отрисовываем все объекты и сетку в конце цикла
        food.update()      # Рисуем еду на экране
        snake.update()     # Рисуем змейку и обновляем множество занятых клеток
        draw_grid()        # Рисуем вспомогательную сетку (клетки)
        pygame.display.flip()  # Обновляем экран: показываем нарисованное за этот кадр
        clock.tick(3 * multip_time)  # Ограничиваем частоту кадров (FPS). Базовая скорость 3 FPS

# Точка входа: если файл запускают напрямую, запускаем main()
if __name__ == '__main__':
    main()
