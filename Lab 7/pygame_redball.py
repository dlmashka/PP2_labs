import pygame
pygame.init()

size = (1000, 760)
RED = (255, 0, 0)
WHITE =  (255, 255, 255)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Red ball")

x = 500
y = 400
step = 2

done = False    
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= step
            if event.key == pygame.K_RIGHT:
                x += step
            if event.key == pygame.K_UP:
                y -= step
            if event.key == pygame.K_DOWN:
                y += step
    if x < 50:
        x = 50
    if x > 950:
        x = 950
    if y < 50:
        y = 50
    if y > 710:
        y = 710
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, [x, y], 50)
    pygame.display.flip()
pygame.quit
