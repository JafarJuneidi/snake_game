import pygame
import random
import datetime

# display 
S_WIDTH, S_HEIGHT = 510, 550  # 20 X 20 blocks
PLAY_WIDTH, PLAY_HEIGHT = 500, 500 
BLOCK_SIZE = 20
PLAY_X = (S_WIDTH - PLAY_WIDTH) // 2
PLAY_Y = (S_HEIGHT - PLAY_HEIGHT) - 5

def check_collision(snake_body):
    head_pos = snake_body[0][0][:2]

    for part in range(1, len(snake_body)):
        if head_pos == snake_body[part][0][:2]:
            return True

    if not (PLAY_X <= head_pos[0]*BLOCK_SIZE + PLAY_X < PLAY_X + PLAY_WIDTH) or not (PLAY_Y <= head_pos[1]*BLOCK_SIZE + PLAY_Y < PLAY_Y + PLAY_HEIGHT):
        return True

    return False

def eat_fruit(snake_body, fruit_pos):
    head = snake_body[0][0][:2]
    if head == fruit_pos:
        return True
    return False

def generate_fruit_pos(snake_body):
    snake_pos = [part[0][:2] for part in snake_body]
    x, y = random.randrange(PLAY_WIDTH//BLOCK_SIZE), random.randrange(PLAY_HEIGHT//BLOCK_SIZE)
    while [x, y] in snake_pos:
        x, y = random.randrange(PLAY_WIDTH//BLOCK_SIZE), random.randrange(PLAY_HEIGHT//BLOCK_SIZE)
    return [x, y]

def move_snake(snake_body):
    x, y, direction = snake_body[0][0]

    if direction == "UP":
        y -= 1
    elif direction == "DOWN":
        y += 1
    elif direction == "RIGHT":
        x += 1
    elif direction == "LEFT":
        x -= 1

    new_snake = [[[x, y, direction], (180,0,0)]]
    for i in range(1, len(snake_body)):
        new_snake.append([snake_body[i - 1][0], (255,255,255)])
            
    return new_snake

def add_part(snake_body):
    tail_x, tail_y, tail_direction = snake_body[-1][0]
    tail_color = snake_body[-1][1]
    
    if tail_direction == "UP":
        tail_y -= 1
    elif tail_direction == "DOWN":
        tail_y += 1
    elif tail_direction == "RIGHT":
        tail_x -= 1
    elif tail_direction == "LEFT":
        tail_x += 1

    snake_body.append([[tail_x, tail_y, tail_direction], tail_color])

    return snake_body

def create_grid(locked_pos = [], fruit_pos=[]):
    grid = [[(0,0,0) for _ in range(PLAY_WIDTH//BLOCK_SIZE)] for _ in range(PLAY_HEIGHT//BLOCK_SIZE)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if [j, i] == fruit_pos:
                grid[i][j] = (0,255,0)
            for k in locked_pos:
                if [j, i] == k[0][:2]:
                    grid[i][j] = k[1]
    return grid

def update_score(new_score):
    with open("best_scores.txt", 'r') as f:
        lines = f.readlines()
        best_score = lines[-1].split(',')[0].strip()

    with open("Best_scores.txt", 'a') as f:
        if new_score > int(best_score):
            f.write(f"\n{new_score}, {datetime.datetime.now()}")

def draw_grid_lines(window):
    for i in range(0, PLAY_HEIGHT + BLOCK_SIZE, BLOCK_SIZE):
        pygame.draw.line(window, (128,128,128), (PLAY_X, PLAY_Y + i), (PLAY_X + PLAY_WIDTH, PLAY_Y + i))
    for j in range(0, PLAY_WIDTH + BLOCK_SIZE, BLOCK_SIZE):
        pygame.draw.line(window, (128,128,128), (PLAY_X + j, PLAY_Y), (PLAY_X + j, PLAY_Y + PLAY_HEIGHT))

def draw_snake(window, grid):
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row][column] != (0,0,0):
                pygame.draw.rect(window, grid[row][column], (PLAY_X + column*BLOCK_SIZE, PLAY_Y + row*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def draw_text_middle(window, text):
    pygame.font.init()

    font = pygame.font.SysFont("comicsans", 60, 1)
    label = font.render(text, 1, (255,0,0))
    window.blit(label, (S_WIDTH//2 - label.get_width()//2, S_HEIGHT//2 - label.get_height()//2))

    pygame.display.update()

def draw_score(window, score):
    pygame.font.init()

    font = pygame.font.SysFont("comicsans", 30, 1)
    label = font.render(f"Score: {score}", 1, (255,255,255))
    window.blit(label, (10, PLAY_Y//2 - label.get_height()//2))

def draw_best_score(window, best_score):
    pygame.font.init()

    font = pygame.font.SysFont("comicsans", 30, 1)
    label = font.render(f"Best Score: {best_score}", 1, (255,255,255))
    window.blit(label, (S_WIDTH - PLAY_X - label.get_width(), PLAY_Y//2 - label.get_height()//2))

def draw(window, grid, score, best_score):
    window.fill((0,0,0))
    draw_grid_lines(window)
    draw_snake(window, grid)
    draw_score(window, score)
    draw_best_score(window, best_score)

    pygame.display.update()

def main(window):
    # game variables
    clock = pygame.time.Clock()
    snake_body = [[[16, 16, "LEFT"], (180,0,0)], [[17, 16, "LEFT"], (255,255,255)], [[18, 16, "LEFT"], (255,255,255)], [[19, 16, "LEFT"], (255,255,255)]]
    fruit_pos = []
    running = True
    move_speed = 0.16
    move_time = 0
    draw_fruit = True
    score = 0
    with open("best_scores.txt", 'r') as f:
        lines = f.readlines()
        best_score = lines[-1].split(',')[0].strip()

    while running:
        move_time += clock.get_rawtime()
        if move_time/1000 > move_speed:
            snake_body = move_snake(snake_body)
            move_time = 0

        if not score%10:
            move_speed *= 0.9997
        
        if draw_fruit:
            fruit_pos = generate_fruit_pos(snake_body)
            draw_fruit = False

        grid = create_grid(snake_body, fruit_pos)

        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_body[0][0][2] != "DOWN":
                    snake_body[0][0][2] = "UP" 
                if event.key == pygame.K_DOWN and snake_body[0][0][2] != "UP":
                    snake_body[0][0][2] = "DOWN"
                if event.key == pygame.K_LEFT and snake_body[0][0][2] != "RIGHT":
                    snake_body[0][0][2] = "LEFT"
                if event.key == pygame.K_RIGHT and snake_body[0][0][2] != "LEFT":
                    snake_body[0][0][2] = "RIGHT"
        

        if eat_fruit(snake_body, fruit_pos):
            score += 1
            fruit_pos = []
            draw_fruit = True
            snake_body = add_part(snake_body)

        draw(window, grid, score, best_score)

        if check_collision(snake_body):
            draw_text_middle(window, "YOU LOST!")
            pygame.time.delay(1000)
            running = False
            update_score(score)

def main_menu(window):
    window.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 50, 1)
    label = font.render("Press any key to play!", 1, (255,255,255))
    window.blit(label, (S_WIDTH//2 - label.get_width()//2, S_HEIGHT//2 - label.get_height()//2))
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                main(window)
                run = False
    main_menu(window)        

WIN = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption("Snake")
main_menu(WIN)