import pygame
import os

pygame.init()
pygame.mixer.init()  #инициализация звука

size = (600, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 35)

#путь к папке с музыкой
path = r'C:\Users\User\OneDrive\Документы\4 курс 7 семестр\Принципы программирования II Нүптебек Е.Н\Лабки\Lab 7\Music\\'
songs = [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]
if not songs:
    print("xxx В папке нет музыкальных файлов! xxx")
    quit()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Music Player")

i = 0  # текущий трек
done = False

screen.fill(BLACK)
text = font.render("Press SPACE to start the player", True, WHITE)
screen.blit(text, (10, 10))
pygame.display.update()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        #Play ⏯ Воспроизведение
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pygame.mixer.music.load(path + songs[i])
            pygame.mixer.music.play()
            screen.fill(BLACK)
            text = font.render(f"Playing: {songs[i]}", True, WHITE)
            screen.blit(text, (10, 10))
            pygame.display.update()

        # Stop ⏹ Пауза/Возобновление
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                text = font.render(f"Stopped: {songs[i]}", True, WHITE)
            else:
                pygame.mixer.music.unpause()
                text = font.render(f"Playing: {songs[i]}", True, WHITE)
            screen.fill(BLACK)
            screen.blit(text, (10, 10))
            pygame.display.update()

        # ⏮ Предыдущая песня
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if i > 0:
                i -= 1
                pygame.mixer.music.load(path + songs[i])
                pygame.mixer.music.play()
                screen.fill(BLACK)
                text = font.render(f"Playing: {songs[i]}", True, WHITE)
                screen.blit(text, (10, 10))
                pygame.display.update()

        # ⏭ Следующая песня
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if i < len(songs) - 1:
                i += 1
                pygame.mixer.music.load(path + songs[i])
                pygame.mixer.music.play()
                screen.fill(BLACK)
                text = font.render(f"Playing: {songs[i]}", True, WHITE)
                screen.blit(text, (10, 10))
                pygame.display.update()

pygame.quit()
