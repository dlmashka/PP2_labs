import pygame 
import random, time 
 
WIDTH = 800                         #size of screen 
HEIGHT = 600                        
FPS = 60                            #number of frames per second 
BLACK = (0, 0, 0)                   #colours
WHITE = (255, 255, 255)             
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
score = 0                           #counter of points 
 
pygame.init()                                            #starting pygame 
screen = pygame.display.set_mode((WIDTH, HEIGHT))        #creating a screen 
clock = pygame.time.Clock()                              #frequency of updates 
pygame.display.set_caption("RACER")                      #screen name 
road = pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 9\street.png')                 #background loading 
font = pygame.font.SysFont(None, 50)        #fonts 
defeat_font = pygame.font.SysFont(None, 150)
a = []                                               #points counter 
 
class Player(pygame.sprite.Sprite): 
    def __init__(self): 
        super().__init__() 
        self.image = pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 9\player.png')              #loading the player's car 
        self.surf = pygame.Surface((40, 60))                       #creating a surface for an object with size 
        self.rect = self.surf.get_rect(center=(400, 500))      #creating a rectangle as the surface of an object 
        self.speed = 5                                         #number of steps on which car will move                                     #Amount of steps 
 
    def move(self):                                            #machine movement function 
        keys = pygame.key.get_pressed()                            #a variable that will accept keystrokes on the keyboard 
        if keys[pygame.K_w] and self.rect.top > 0:                #the condition when the up button is pressed and the car is not located on the upper border of the screen 
            self.rect.move_ip(0, -self.speed)                  #moving the object up the specified number of steps vertically 
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT: 
            self.rect.move_ip(0, self.speed) 
        if keys[pygame.K_a] and self.rect.left > 0: 
            self.rect.move_ip(-self.speed, 0) 
        if keys[pygame.K_d] and self.rect.right < WIDTH: 
            self.rect.move_ip(self.speed, 0) 
    
    def draw(self):                                                            #function for inserting an object 
        self.surf.blit(pygame.transform.scale(self.image, (40, 60)), (0, 0))       #resizing the image 
        screen.blit(self.surf, (self.rect.x, self.rect.y))                     #superimposing a photo on a rectangle of an object 
 
 
class Enemy(pygame.sprite.Sprite): #Enemy car 
    def __init__(self): 
        super().__init__() 
        self.image = pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 9\enemy.png')          #loading the enemy car
        self.surf = pygame.Surface((40, 60)) 
        self.rect = self.surf.get_rect(center=(random.randint(40, WIDTH - 40), -100))   #the appearance of objects outside the screen 
        self.speed = random.randint(3, 5)                                              #random speed in the specified range 
        if len(a) > 5:                                                                 #checking for the score to increase the speed 
            self.speed +=3                                                             #enemy`s speed increase` 
 
    def move(self): 
        self.rect.move_ip(0, self.speed)                  #the movement of an object with a constant vertical velocity 
        
    def draw(self): 
        self.surf.blit(pygame.transform.scale(self.image, (40, 60)), (0, 0)) 
        screen.blit(self.surf, (self.rect.x, self.rect.y)) 
 
    def death(self):                                      #object deletion function 
        if self.rect.top > HEIGHT:                        #conditions that the coordinates of the object exceed the height of the screen 
            self.kill()                                   #object deletion 
 
 
class Coin(pygame.sprite.Sprite): 
    def __init__(self): 
        super().__init__() 
        self.surf =pygame.Surface((20, 20)) 
        self.rect = self.surf.get_rect(center=(random.randint(40, WIDTH - 40), -100)) 
        self.speed = random.randint(1, 5) 
        self.random_number = random.randint(0, 8) 
        self.images = [pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 9\coin_1.png') , pygame.image.load(r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Lab8_2version\coin_2.png')] 
        self.supcoin() 
 
    def move(self): 
        self.rect.move_ip(0, self.speed) 
 
    def draw(self):      
        self.surf.blit(pygame.transform.scale(self.image, (20, 20)), (0, 0)) 
        screen.blit(self.surf, (self.rect.x, self.rect.y)) 
 
    def death(self): 
        if self.rect.top > HEIGHT: 
            self.kill() 
 

    def supcoin(self): 
        if self.random_number == 7: 
            self.image = self.images[1]                          #creating a megacoin 
        else: 
            self.image = self.images[0] 
    def is_sup_coin(self): 
        return self.random_number == 7 
 
 
P1 = Player()                                                    #assigning a class to a variable 
enemies = pygame.sprite.Group([Enemy() for _ in range(4)])           #assigning a class to a variable, determining the number of objects 
coins = pygame.sprite.Group([Coin() for _ in range(6)])              #assigning a class to a variable, determining the number of objects 
 
running = True                                              #variable for loop operation 
while running:                                              #start of the cycle 
    clock.tick(FPS) 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:                           #when the screen is closed, the cycle stops 
            running = False 
        
    screen.fill(WHITE) 
    screen.blit(pygame.transform.scale(road, (WIDTH, HEIGHT)), (0, 0 % HEIGHT))      #stretching an image to fit the screen 
 
    P1.draw()                                       #function call 
    P1.move() 
 
    for enemy in enemies: 
        enemy.draw() 
        enemy.move() 
        enemy.death() 
 
    for coin in coins: 
        coin.draw() 
        coin.move() 
        coin.death() 
 
    if enemies.__len__() < 4: 
        enemies.add(Enemy())                        #creating new objects 
 
    if coins.__len__() < 6: 
        coins.add(Coin()) 
 
    if pygame.sprite.spritecollide(P1, enemies, False):         #conditions for stopping the cycle 
        screen.fill(BLACK)
        text1 = defeat_font.render("GAME OVER!", True, RED)
        text2 = font.render("Your score is "+str(score), True, RED)
        screen.blit(text1, (40, 250))
        screen.blit(text2, (100, 400))
        pygame.display.update()
        time.sleep(2)
        running = False 
 
    for coin in pygame.sprite.spritecollide(P1, coins, True): 
        score += 1                                          #increasing the number of points 
        a.append(1)                                         #counter increasing 
        if coin.is_sup_coin(): 
            score += 20 
 
 
    text = font.render(str(score), True, BLACK)            #displaying the number of points on the screen 
    screen.blit(text, (20, 20)) 
 
    pygame.display.update()                                    #updating the screen with changes 
pygame.quit()          
