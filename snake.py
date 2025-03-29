import pygame
import random
import time  # Import time to track when fruit is created

pygame.init()

# экран
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# переменные
score = 0
level = 1
speed = 200  # скорость начальная
fruit_eaten = False
fruit_creation_time = 0  # начало отсчета
fruit_timeout = 10  # конец отчета
# змея
head_square = [100, 100]
squares = [[30, 100], [40, 100], [50, 100], [60, 100], [70, 100], [80, 100], [90, 100], [100, 100]]
direction = "right"
next_dir = "right"
done = False
# генерируем координаты фрукта, ток чтобы они не были на змее
def generate_fruit():
    while True:
        fr_x = random.randrange(1, width // 10) * 10
        fr_y = random.randrange(1, height // 10) * 10
        fruit_coor = [fr_x, fr_y]
        if fruit_coor not in squares:  # чтобы он не заспавнился на змее
            return fruit_coor

fruit_coor = generate_fruit()


def game_over(font, size, color):
    global done
    g_o_font = pygame.font.SysFont(font, size)
    g_o_surface = g_o_font.render(f"Game Over! Score: {score} | Level: {level}", True, color)
    g_o_rect = g_o_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(g_o_surface, g_o_rect)
    pygame.display.update()
    pygame.time.delay(4000)
    pygame.quit()
    exit()

# игровая механика
while not done:
    #првоеряем время отчета фрукта
    if time.time() - fruit_creation_time > fruit_timeout:
        fruit_coor = generate_fruit()  # если время вышло создаем новый фрукта
        fruit_creation_time = time.time()  # включаем таймер заново

    # движение
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                next_dir = "down"
            if event.key == pygame.K_UP:
                next_dir = "up"
            if event.key == pygame.K_LEFT:
                next_dir = "left"
            if event.key == pygame.K_RIGHT:
                next_dir = "right"
    
    # столкновение с собой
    for square in squares[:-1]:
        if head_square == square:
            game_over("times new roman", 45, (255, 0, 0))
    
    if next_dir == "right" and direction != "left":
        direction = "right"
    if next_dir == "up" and direction != "down":
        direction = "up"
    if next_dir == "left" and direction != "right":
        direction = "left"
    if next_dir == "down" and direction != "up":
        direction = "down"
    
    # движения
    if direction == "right":
        head_square[0] += 10
    if direction == "left":
        head_square[0] -= 10
    if direction == "up":
        head_square[1] -= 10
    if direction == "down":
        head_square[1] += 10
    
    # столкновение со стенками
    if head_square[0] < 0 or head_square[0] >= width or head_square[1] < 0 or head_square[1] >= height:
        game_over("times new roman", 45, (255, 0, 0))
    
    # анимация самой змеи
    new_square = [head_square[0], head_square[1]]
    squares.append(new_square)
    squares.pop(0)
    
    # съедение фрукта
    if head_square == fruit_coor:
        weight = random.randint(1, 10)
        fruit_eaten = True
        score += weight
        squares.insert(0, squares[0])  # рост
    
    # генерируем новый фрукт
    if fruit_eaten:
        fruit_coor = generate_fruit()
        fruit_creation_time = time.time() 
        fruit_eaten = False
    
    # каждые 30 очков лвл ап
    if score // 30 + 1 > level:
        level += 1
        speed = max(50, speed - 20)  # понижаем дилей , увеличивая скорость
    
    screen.fill((0, 0, 0))
    
    # лвл и очки
    font = pygame.font.SysFont("times new roman", 20)
    score_surface = font.render(f"Score: {score} | Level: {level}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))
    
    # рисовка фрукта
    pygame.draw.circle(screen, (0, 255, 0), (fruit_coor[0] + 5, fruit_coor[1] + 5), 5)
    
    # рисовка змеи
    for el in squares:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(el[0], el[1], 10, 10))
    
    pygame.display.flip()
    pygame.time.delay(speed)  # скорость игры

pygame.quit()
