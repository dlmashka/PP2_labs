import pygame
import random, time

# - НАСТРОЙКИ И КОНСТАНТЫ -
WIDTH = 800                         # ширина окна
HEIGHT = 600                        # высота окна
FPS = 60                            # кадры в секунду (скорость обновления)

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

score = 0                           # общий счёт игрока

# - ИНИЦИАЛИЗАЦИЯ PYGAME И ЗАГРУЗКА РЕСУРСОВ -
pygame.init()                                            # запускаем pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))        # создаём окно игры
clock = pygame.time.Clock()                              # объект для контроля FPS
pygame.display.set_caption("RACER")                    # заголовок окна

# Загрузите свои изображения по путям ниже. Это абсолютные пути на вашем ПК.
road = pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 9\street.png')

# Шрифты для текста (размеры 50 — для счёта, 150 — для GAME OVER)
font = pygame.font.SysFont(None, 50)
defeat_font = pygame.font.SysFont(None, 150)

a = []  # вспомогательный список: используется как счётчик/индикатор прогресса


# - КЛАСС PLAYER (игрок) -
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Загружаем изображение игрока (машины)
        self.image = pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 9\player.png')
        # Создаём поверхность, на которой будем рисовать изображение (размер под изображение)
        self.surf = pygame.Surface((40, 60), pygame.SRCALPHA)
        # rect хранит позицию и размеры — удобно для движения и коллизий
        self.rect = self.surf.get_rect(center=(400, 500))
        self.speed = 5  # скорость перемещения игрока (в пикселях за шаг)

    def move(self):
        # Считываем состояние всех клавиш
        keys = pygame.key.get_pressed()
        # Движение (WASD) с проверкой границ экрана
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.move_ip(0, -self.speed)  # вверх
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.move_ip(0, self.speed)   # вниз
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)  # влево
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.move_ip(self.speed, 0)   # вправо

    def draw(self):
        # Рисуем изображение на surface и выводим на экран в позиции rect
        # Здесь мы масштабируем изображение под размер surface (40x60)
        self.surf.blit(pygame.transform.scale(self.image, (40, 60)), (0, 0))
        screen.blit(self.surf, (self.rect.x, self.rect.y))


# - КЛАСС ENEMY (вражеская машина) -
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 9\enemy.png')
        self.surf = pygame.Surface((40, 60), pygame.SRCALPHA)
        # Враг появляется случайно по X и выше экрана по Y (-100)
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 40), -100))
        self.speed = random.randint(3, 5)  # случайная скорость
        # Если игрок уже собрал много (len(a) > 5), делаем врагов быстрее
        if len(a) > 5:
            self.speed += 3

    def move(self):
        # Враг двигается вниз с постоянной скоростью
        self.rect.move_ip(0, self.speed)

    def draw(self):
        # Рисуем врага так же, как игрока
        self.surf.blit(pygame.transform.scale(self.image, (40, 60)), (0, 0))
        screen.blit(self.surf, (self.rect.x, self.rect.y))

    def death(self):
        # Если враг ушёл ниже экрана — удаляем его (kill)
        if self.rect.top > HEIGHT:
            self.kill()


# - КЛАСС COIN (монетка) -
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Создаём небольшую поверхность 20x20 для монеты
        self.surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Монета появляется в случайном X и выше экрана по Y
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 40), -100))
        self.speed = random.randint(1, 5)  # скорость падения монеты
        # случайное число — используется для определения, будет ли эта монета "супер"
        self.random_number = random.randint(0, 8)
        # Список изображений: обычная монета и мегамонета
        self.images = [
            pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 9\coin_1.png'),
            pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 9\coin_2.png')
        ]
        # Устанавливаем текущее изображение монеты
        self.supcoin()

    def move(self):
        # Монета опускается вниз
        self.rect.move_ip(0, self.speed)

    # Рисуем изображение монеты на surface и выводим на экран
    def draw(self):
        if self.is_sup_coin():  # если супермонета
            screen.blit(pygame.transform.scale(self.image, (30, 30)), (self.rect.x, self.rect.y))
        else:                   # обычная монета
            screen.blit(pygame.transform.scale(self.image, (20, 20)), (self.rect.x, self.rect.y))

    def death(self):
        # Если монета ушла ниже экрана — удаляем
        if self.rect.top > HEIGHT:
            self.kill()

    def supcoin(self):
        # Правило: если random_number == 4 — это мегамонета (даёт больше очков)
        # В коде random_number выбирается от 0 до 8, значит шанс есть
        if self.random_number == 4:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

    def is_sup_coin(self):
        # Удобный метод — можно спросить у монеты, является ли она супермонетой
        return self.random_number == 4


# - СОЗДАЁМ ОБЪЕКТЫ И ГРУППЫ -
P1 = Player()
# Группы позволяют легко перебирать и проверять коллизии
enemies = pygame.sprite.Group([Enemy() for _ in range(4)])
coins = pygame.sprite.Group([Coin() for _ in range(6)])


# - ГЛАВНЫЙ ЦИКЛ ИГРЫ -
running = True
while running:
    clock.tick(FPS)  # держим фиксированные FPS

    # - обработка событий (закрытие окна и т.п.) -
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # - рисуем фон -
    screen.fill(WHITE)
    # масштабируем фон под размеры окна
    screen.blit(pygame.transform.scale(road, (WIDTH, HEIGHT)), (0, 0 % HEIGHT))

    # - обновляем и рисуем игрока -
    P1.draw()
    P1.move()

    # - обновляем и рисуем врагов -
    for enemy in enemies:
        enemy.draw()
        enemy.move()
        enemy.death()  # удаляет врага, если он ушёл за экран

    # - обновляем и рисуем монеты -
    for coin in coins:
        coin.draw()
        coin.move()
        coin.death()

    # - поддерживаем постоянное число объектов -
    if enemies.__len__() < 4:
        enemies.add(Enemy())  # добавляем нового врага, если их стало меньше

    if coins.__len__() < 6:
        coins.add(Coin())  # добавляем монету, если их стало меньше

    # - проверка столкновения с врагом (GAME OVER) -
    # Если есть пересечение игрока и любого врага — завершаем игру
    if pygame.sprite.spritecollide(P1, enemies, False):
        screen.fill(BLACK)
        text1 = defeat_font.render("GAME OVER!", True, RED)
        text2 = font.render("Your score is " + str(score), True, RED)
        screen.blit(text1, (40, 250))
        screen.blit(text2, (100, 400))
        pygame.display.update()
        time.sleep(2)  # пауза чтобы игрок увидел экран окончания
        running = False

    # - сбор монет -
    # spritecollide с параметром True удаляет монеты, которые собрали
    for coin in pygame.sprite.spritecollide(P1, coins, True):
        score += 1          # обычная монета даёт 1 очко
        a.append(1)         # увеличиваем "прогресс" (используется для усложнения)
        if coin.is_sup_coin():
            score += 10     # супермонета даёт бонус

    # - вывод счёта на экран -
    text = font.render(str(score), True, BLACK)
    screen.blit(text, (20, 20))

    # - применяем все изменения на экран -
    pygame.display.update()

# - выход из игры -
pygame.quit()
