"""snake_game.py
Simple snake game (pygame) with DB integration.
- Before game asks username.
- Loads latest level for user (if exists).
- Press 'p' to pause and save current score/state to DB.
This is a minimal template. Tune constants and DB settings as needed.
"""
import pygame, sys, json, random
from snake_game_db import create_user_tables, get_or_create_user, get_latest_score_for_user, save_user_score

# Basic game settings
CELL = 20
W = 30
H = 20
WIDTH = CELL * W
HEIGHT = CELL * H

# Levels definition: each level is dict with walls (list of rects) and speed
LEVELS = {
    1: {'speed': 8, 'walls': []},
    2: {'speed': 12, 'walls': [ (5,5,20,1), (10,10,10,1) ]},  # example walls (not used directly here)
    3: {'speed': 16, 'walls': [ (i,0,1,1) for i in range(W) ]}
}

def serialize_state(snake, direction, food, score, level):
    return {
        'snake': snake,
        'direction': direction,
        'food': food,
        'score': score,
        'level': level
    }

def deserialize_state(state):
    return state['snake'], state['direction'], state['food'], state['score'], state['level']

def main():
    create_user_tables()
    username = input('Enter your username: ').strip()
    user_id = get_or_create_user(username)
    last = get_latest_score_for_user(user_id)
    if last:
        print('Found previous save -> level', last['level'], 'score', last['score'])
        snake, direction, food, score, level = deserialize_state(last['saved_state']) if last['saved_state'] else ([(5,5)], 'RIGHT', (10,10), 0, 1)
    else:
        level = 1
        score = 0
        snake = [(5,5)]
        direction = 'RIGHT'
        food = (10,10)

    level_conf = LEVELS.get(level, LEVELS[1])
    speed = level_conf['speed']

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # Pause and save state
                    state = serialize_state(snake, direction, food, score, level)
                    save_user_score(user_id, score, level, state)
                    print('Saved state for user', username)
                elif event.key == pygame.K_UP:
                    direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'

        # simple movement update
        head_x, head_y = snake[0]
        if direction == 'RIGHT':
            head_x += 1
        elif direction == 'LEFT':
            head_x -= 1
        elif direction == 'UP':
            head_y -= 1
        elif direction == 'DOWN':
            head_y += 1
        new_head = (head_x % W, head_y % H)
        if new_head in snake:
            print('Game over. Final score', score)
            running = False
            continue
        snake.insert(0, new_head)
        # eat food
        if new_head == food:
            score += 1
            food = (random.randint(0, W-1), random.randint(0, H-1))
        else:
            snake.pop()

        screen.fill((0,0,0))
        # draw food
        pygame.draw.rect(screen, (255,0,0), (food[0]*CELL, food[1]*CELL, CELL, CELL))
        # draw snake
        for s in snake:
            pygame.draw.rect(screen, (0,255,0), (s[0]*CELL, s[1]*CELL, CELL, CELL))
        # HUD
        txt = font.render(f'User: {username}  Score: {score}  Level: {level}  (Press P to save)', True, (255,255,255))
        screen.blit(txt, (5,5))
        pygame.display.flip()
        clock.tick(speed)


if __name__ == '__main__':
    main()
