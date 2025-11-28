import pygame

# - Параметры окна и начальные настройки -
WIDTH, HEIGHT = 1400, 800   # размеры окна программы
FPS = 60                    # частота обновления экрана (кадров в секунду)
draw = False                # флаг: в данный момент пользователь рисует (нажата кнопка мыши)
lastPos = (0, 0)            # предыдущая координата мыши (используется при рисовании линий)
radius = 3                  # текущая "толщина" кисти / радиус при рисовании
color = 'blue'              # текущий цвет кисти (как строка, pygame.Color его распознаёт)
mode = 'pen'                # режим рисования: 'pen', 'erase', 'rectangle', и т.д.

# Инициализация Pygame и создание окна
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # создаём окно
pygame.display.set_caption('Paint')                # заголовок окна
clock = pygame.time.Clock()                        # объект для контроля FPS
screen.fill(pygame.Color('white'))                 # заливаем фон белым цветом
font = pygame.font.SysFont('None', 60)             # шрифт для отображения размера кисти

# - Вспомогательные функции рисования -
# Эти функции реализуют рисование фигур. Их удобно вызывать при отпускании кнопки мыши.

def drawLine(screen, start, end, width, color):
    """
    Рисует "толстую" линию от start до end, рисуя окружности по пути.
    Это простая реализация линии, которая заполняет промежутки между двумя точками.
    start, end: (x, y)
    width: радиус (int)
    color: строка или pygame.Color
    """
    x1 = start[0]
    x2 = end[0]
    y1 = start[1]
    y2 = end[1]

    # Разности по осям (понадобятся для выбора пробежки по x или по y)
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    # Коэффициенты для уравнения прямой в форме A*x + B*y + C = 0
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2

    # Если изменение по x больше — будем итерироваться по x, иначе по y
    if dx > dy:
        # Упорядочиваем точки так, чтобы цикл шёл от меньшего x к большему
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        # Для каждого x вычисляем соответствующий y по уравнению прямой и рисуем круг
        for x in range(x1, x2):
            y = (-C - A * x) / B
            pygame.draw.circle(screen, pygame.Color(color), (x, y), width)
    else:
        # Итерируем по y, если dy >= dx
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        for y in range(y1, y2):
            x = (-C - B * y) / A
            pygame.draw.circle(screen, pygame.Color(color), (x, y), width)

def drawCircle(screen, start, end, width, color):
    """
    Рисует окружность по двум точкам: start и end — определяют диаметр.
    width здесь используется как толщина контура (если width == 0 — залитая).
    """
    x1 = start[0]
    x2 = end[0]
    y1 = start[1]
    y2 = end[1]
    # центр — середина отрезка start-end
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    # радиус считаем как половина ширины по x (можно изменить чтобы учитывать y)
    radius = abs(x1 - x2) / 2
    pygame.draw.circle(screen, pygame.Color(color), (x, y), radius, width)

def drawRectangle(screen, start, end, width, color):
    """
    Рисует прямоугольник по двум противоположным углам: start и end.
    width — толщина рамки (если 0 — залитый).
    """
    x1 = start[0]
    x2 = end[0]
    y1 = start[1]
    y2 = end[1]
    widthr = abs(x1 - x2)   # ширина прямоугольника
    height = abs(y1 - y2)   # высота прямоугольника
    # В зависимости от расположения точек, передаём правильные координаты в pygame.draw.rect
    if x2 > x1 and y2 > y1:
        pygame.draw.rect(screen, pygame.Color(color), (x1, y1, widthr, height), width)
    if y2 > y1 and x1 > x2:
        pygame.draw.rect(screen, pygame.Color(color), (x2, y1, widthr, height), width)
    if x1 > x2 and y1 > y2:
        pygame.draw.rect(screen, pygame.Color(color), (x2, y2, widthr, height), width)
    if x2 > x1 and y1 > y2:
        pygame.draw.rect(screen, pygame.Color(color), (x1, y2, widthr, height), width)

def drawSquare(screen, start, end, color):
    """
    Рисует квадрат, сторона которого равна меньшей из разниц по x и по y.
    Функция всегда рисует заполненный квадрат (без параметра thickness).
    """
    x1 = start[0]
    x2 = end[0]
    y1 = start[1]
    y2 = end[1]
    mn = min(abs(x2 - x1), abs(y2 - y1))  # длина стороны квадрата

    # Проверяем в какой четверти находится вторая точка и рисуем квадрат с корректными координатами
    if x2 > x1 and y2 > y1:
        pygame.draw.rect(screen, pygame.Color(color), (x1, y1, mn, mn))
    if y2 > y1 and x1 > x2:
        pygame.draw.rect(screen, pygame.Color(color), (x2, y1, mn, mn))
    if x1 > x2 and y1 > y2:
        pygame.draw.rect(screen, pygame.Color(color), (x2, y2, mn, mn))
    if x2 > x1 and y1 > y2:
        pygame.draw.rect(screen, pygame.Color(color), (x1, y2, mn, mn))

def drawRightTriangle(screen, start, end, color):
    """
    Рисует прямоугольный треугольник, где прямой угол располагается в одной из вершин.
    Параметры start и end определяют ограничивающий прямоугольник треугольника.
    """
    x1 = start[0]
    x2 = end[0]
    y1 = start[1]
    y2 = end[1]

    # В зависимости от расположения end относительно start, расставляем вершины правильно
    if x2 > x1 and y2 > y1:
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y1), (x2, y2), (x1, y2)))
    if y2 > y1 and x1 > x2:
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y1), (x2, y2), (x1, y2)))
    if x1 > x2 and y1 > y2:
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y1), (x2, y2), (x2, y1)))
    if x2 > x1 and y1 > y2:
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y1), (x2, y2), (x2, y1)))

def drawEquilateralTriangle(screen, start, end, width, color):
    """
    Рисует равносторонний треугольник, вписанный по ширине между x1 и x2.
    width тут используется как толщина линии (если 0 — залитый).
    """
    x1 = start[0]
    x2 = end[0]
    y1 = start[1]
    y2 = end[1]

    width_b = abs(x2 - x1)
    height = (3**0.5) * width_b / 2  # высота равностороннего треугольника

    if y2 > y1:
        # Нижняя база лежит на уровне y2, вершина — выше на height
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y2), (x2, y2), ((x1 + x2) / 2, y2 - height)), width)
    else:
        # Если мышь над началом — рисуем вверх от y1
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y1), (x2, y1), ((x1 + x2) / 2, y1 - height)))

def drawRhombus(screen, start, end, width, color):
    """
    Рисует ромб по центру между start и end.
    Используется pygame.draw.lines с замкнутой фигурой (True).
    """
    x1 = start[0]
    x2 = end[0]
    y1 = start[1]
    y2 = end[1]
    pygame.draw.lines(screen, pygame.Color(color), True, (
        ((x1 + x2) / 2, y1),          # верхняя вершина ромба (по середине по x, на y1)
        (x1, (y1 + y2) / 2),          # левая вершина
        ((x1 + x2) / 2, y2),          # нижняя вершина
        (x2, (y1 + y2) / 2)           # правая вершина
    ), width)

# - Инструкция по клавишам (распечатай/запомни для защиты) -
print('''
r - прямоугольник
c - круг
s - квадрат
t - прямоугольный треугольник
u - равносторонний треугольник
h - ромб
p - ручка
e - стерка
q - очистить экран
1 - черный, 2 - зеленый, 3 - красный, 4 - синий, 5 - жёлтый
+ - увеличить
- - уменьшить  
''')

# - Главный цикл программы -
while True:
    # Обработка всех событий (клавиатура, мышь, закрытие окна)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Пользователь закрыл окно — завершаем программу
            exit()

        # -  Обработка нажатий клавиш -
        if event.type == pygame.KEYDOWN:
            # переключение режимов рисования по клавише
            if event.key == pygame.K_r:
                mode = 'rectangle'
            if event.key == pygame.K_c:
                mode = 'circle'
            if event.key == pygame.K_p:
                mode = 'pen'
            if event.key == pygame.K_e:
                mode = 'erase'
            if event.key == pygame.K_s:
                mode = 'square'
            if event.key == pygame.K_q:
                # очистка экрана — заливаем белым
                screen.fill(pygame.Color('white'))

            # выбор цвета по клавишам 1-5
            if event.key == pygame.K_1:
                color = 'black'
            if event.key == pygame.K_2:
                color = 'green'
            if event.key == pygame.K_3:
                color = 'red'
            if event.key == pygame.K_4:
                color = 'blue'
            if event.key == pygame.K_5:
                color = 'yellow'

            # дополнительные фигуры
            if event.key == pygame.K_t:
                mode = 'right_tri'
            if event.key == pygame.K_u:
                mode = 'eq_tri'
            if event.key == pygame.K_h:
                mode = 'rhombus'

            # изменение радиуса (толщины кисти) на цифровой клавиатуре (+ и -)
            # NOTE: используются клавиши numpad (KP_PLUS / KP_MINUS). Можно заменить на обычные '+'/'-'
            if event.key == pygame.K_KP_PLUS:  # pygame.K_PLUS:
                radius = min(200, radius + 1)  # ограничиваем сверху радиус 200
            if event.key == pygame.K_KP_MINUS:  # pygame.K_MINUS:
                radius = max(1, radius - 1)    # минимальный радиус 1

        # - Мышь: нажатие кнопки -
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw = True  # пользователь начал рисовать
            # Если режим pen — сразу оставляем точку в месте нажатия
            if mode == 'pen':
                pygame.draw.circle(screen, pygame.Color(color), event.pos, radius)
            prevPos = event.pos  # запоминаем позицию, от которой будем рисовать фигуры при отпускании

        # - Мышь: отпускание кнопки -
        if event.type == pygame.MOUSEBUTTONUP:
            # В зависимости от режима рисуем соответствующую фигуру от prevPos до текущей позиции
            if mode == 'rectangle':
                drawRectangle(screen, prevPos, event.pos, radius, color)
            elif mode == 'circle':
                drawCircle(screen, prevPos, event.pos, radius, color)
            elif mode == 'square':
                drawSquare(screen, prevPos, event.pos, color)
            elif mode == 'right_tri':
                drawRightTriangle(screen, prevPos, event.pos, color)
            elif mode == 'eq_tri':
                drawEquilateralTriangle(screen, prevPos, event.pos, radius, color)
            elif mode == 'rhombus':
                drawRhombus(screen, prevPos, event.pos, radius, color)
            draw = False  # закончили рисовать (кнопка отпущена)

        # - Мышь: движение -
        if event.type == pygame.MOUSEMOTION:
            # Если держат кнопку и режим pen — рисуем подряд линии между последней позицией и текущей
            if draw and mode == 'pen':
                drawLine(screen, lastPos, event.pos, radius, color)
            # Если режим erase — рисуем белые круги (стёрка)
            elif draw and mode == 'erase':
                drawLine(screen, lastPos, event.pos, radius, 'white')
            # Обновляем lastPos для следующего движения
            lastPos = event.pos

    # - Отрисовка HUD (индикатора текущего радиуса) -
    # Сначала очищаем область, где показываем размер, чтобы цифра не наслаивалась
    pygame.draw.rect(screen, pygame.Color('white'), (5, 5, 115, 75))
    # Рисуем цифру текущего радиуса кисти
    renderRadius = font.render(str(radius), True, pygame.Color(color))
    screen.blit(renderRadius, (5, 5))

    # Обновляем экран и ждём следующий кадр
    pygame.display.flip()
    clock.tick(FPS)
