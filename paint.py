import pygame
import random
screen = pygame.display.set_mode((900, 700))
canvas = pygame.Surface((900, 700))
canvas.fill((255, 255, 255))

pygame.display.set_caption('Paint')

draw_on = False
last_pos = (0, 0)
radius = 5

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (102, 204, 0)
BLUE = (51, 51, 255)
BLACK = (0, 0, 0)
PINK = (255, 0, 255)

# интерфейс
pygame.draw.rect(canvas, RED, (0, 50, 20, 20))
pygame.draw.rect(canvas, YELLOW, (0, 70, 20, 20))
pygame.draw.rect(canvas, GREEN, (20, 50, 20, 20))
pygame.draw.rect(canvas, BLUE, (20, 70, 20, 20))
pygame.draw.rect(canvas, BLACK, (0, 90, 20, 20))
pygame.draw.rect(canvas, PINK, (20, 90, 20, 20))
eraser = pygame.transform.scale(pygame.image.load("eraser.png"), (40, 40))
canvas.blit(eraser, [0, 110])

# флаги для инструментов
drawing_rect = False
drawing_circle = False
drawing_square = False
drawing_right_triangle = False
drawing_equilateral_triangle = False
drawing_rhombus = False
active_color = BLACK
active_size = 5

# рисование
def roundline(canvas, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + (dx/distance) * i)
        y = int(start[1] + (dy/distance) * i)
        pygame.draw.circle(canvas, color, (x, y), radius)

# фигуры
def draw_rectangle(start, end, color):
    pygame.draw.rect(canvas, color, (start[0], start[1], end[0]-start[0], end[1]-start[1]))

def draw_circle(start, end, color):
    radius = int(((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5)
    pygame.draw.circle(canvas, color, start, radius)

def draw_square(start, end, color):
    width = end[0] - start[0]
    height = end[1] - start[1]
    size = min(abs(width), abs(height))  # минимальная сторона
    # направление рисования
    if width < 0:
        start = (start[0] - size, start[1])
    if height < 0:
        start = (start[0], start[1] - size)
    pygame.draw.rect(canvas, color, (start[0], start[1], size, size))

def draw_right_triangle(start, end, color):
    points = [
        start,  # прямой угол
        (start[0], end[1]),  # вертикальный катет
        end  # Ггипотенуза
    ]
    pygame.draw.polygon(canvas, color, points)

def draw_equilateral_triangle(start, end, color):
    width = end[0] - start[0]
    height = int(abs(width) * (3 ** 0.5) / 2)  #высота
    points = [
        start,  # левая
        (start[0] + width, start[1]),  # правя
        (start[0] + width // 2, start[1] - height)  # верхняя
    ]
    pygame.draw.polygon(canvas, color, points)

def draw_rhombus(start, end, color):
    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2
    width = abs(end[0] - start[0]) // 2
    height = abs(end[1] - start[1]) // 2
    points = [
        (center_x, center_y - height),  # верхняя точка
        (center_x + width, center_y),  # правая точка
        (center_x, center_y + height),  # нижняя точка
        (center_x - width, center_y)  # левая точка
    ]
    pygame.draw.polygon(canvas, color, points)

try:
    while True:
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            raise StopIteration

        if e.type == pygame.MOUSEBUTTONDOWN:
            spot = e.pos
            if spot[0] < 20:
                if 50 <= spot[1] < 70:
                    active_color = RED
                elif 70 <= spot[1] < 90:
                    active_color = YELLOW
                elif 90 <= spot[1] < 110:
                    active_color = BLACK
                elif 110 <= spot[1] < 150:
                    active_color = WHITE
            elif 20 <= spot[0] < 40:
                if 50 <= spot[1] < 70:
                    active_color = GREEN
                elif 70 <= spot[1] < 90:
                    active_color = BLUE
                elif 90 <= spot[1] < 110:
                    active_color = PINK

            # активация рисования
            if spot[0] > 60:
                draw_on = True
                last_pos = e.pos
                start_pos = e.pos

        if e.type == pygame.MOUSEBUTTONUP:
            if draw_on:
                if drawing_rect:
                    end_pos = e.pos
                    draw_rectangle(start_pos, end_pos, active_color)
                elif drawing_circle:
                    end_pos = e.pos
                    draw_circle(start_pos, end_pos, active_color)
                elif drawing_square:
                    end_pos = e.pos
                    draw_square(start_pos, end_pos, active_color)
                elif drawing_right_triangle:
                    end_pos = e.pos
                    draw_right_triangle(start_pos, end_pos, active_color)
                elif drawing_equilateral_triangle:
                    end_pos = e.pos
                    draw_equilateral_triangle(start_pos, end_pos, active_color)
                elif drawing_rhombus:
                    end_pos = e.pos
                    draw_rhombus(start_pos, end_pos, active_color)
                draw_on = False

        # то как двигается мышь во время рисования
        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                if drawing_rect or drawing_circle or drawing_square or drawing_right_triangle or drawing_equilateral_triangle or drawing_rhombus:
                    #обновление экрана
                    screen.blit(canvas, (0, 0))
                    current_pos = e.pos
                    if drawing_rect:
                        pygame.draw.rect(screen, active_color, (start_pos[0], start_pos[1], current_pos[0]-start_pos[0], current_pos[1]-start_pos[1]))
                    elif drawing_circle:
                        radius = int(((current_pos[0]-start_pos[0])**2 + (current_pos[1]-start_pos[1])**2)**0.5)
                        pygame.draw.circle(screen, active_color, start_pos, radius)
                    elif drawing_square:
                        width = current_pos[0] - start_pos[0]
                        height = current_pos[1] - start_pos[1]
                        size = min(abs(width), abs(height))
                        if width < 0:
                            rect_start = (start_pos[0] - size, start_pos[1])
                        else:
                            rect_start = start_pos
                        if height < 0:
                            rect_start = (rect_start[0], start_pos[1] - size)
                        pygame.draw.rect(screen, active_color, (rect_start[0], rect_start[1], size, size))
                    elif drawing_right_triangle:
                        points = [start_pos, (start_pos[0], current_pos[1]), current_pos]
                        pygame.draw.polygon(screen, active_color, points)
                    elif drawing_equilateral_triangle:
                        width = current_pos[0] - start_pos[0]
                        height = int(abs(width) * (3 ** 0.5) / 2)
                        points = [start_pos, (start_pos[0] + width, start_pos[1]), (start_pos[0] + width // 2, start_pos[1] - height)]
                        pygame.draw.polygon(screen, active_color, points)
                    elif drawing_rhombus:
                        center_x = (start_pos[0] + current_pos[0]) // 2
                        center_y = (start_pos[1] + current_pos[1]) // 2
                        width = abs(current_pos[0] - start_pos[0]) // 2
                        height = abs(current_pos[1] - start_pos[1]) // 2
                        points = [(center_x, center_y - height), (center_x + width, center_y), (center_x, center_y + height), (center_x - width, center_y)]
                        pygame.draw.polygon(screen, active_color, points)
                    pygame.display.update()
                else:
                    # обычное рисование
                    pygame.draw.circle(canvas, active_color, e.pos, active_size)
                    roundline(canvas, active_color, e.pos, last_pos, active_size)
                    last_pos = e.pos

        # условия для выбора инстумента
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                drawing_rect = True
                drawing_circle = False
                drawing_square = False
                drawing_right_triangle = False
                drawing_equilateral_triangle = False
                drawing_rhombus = False
            elif e.key == pygame.K_c:
                drawing_circle = True
                drawing_rect = False
                drawing_square = False
                drawing_right_triangle = False
                drawing_equilateral_triangle = False
                drawing_rhombus = False
            elif e.key == pygame.K_s:  # квадрат
                drawing_square = True
                drawing_rect = False
                drawing_circle = False
                drawing_right_triangle = False
                drawing_equilateral_triangle = False
                drawing_rhombus = False
            elif e.key == pygame.K_t:  # прямоугольный треуг
                drawing_right_triangle = True
                drawing_rect = False
                drawing_circle = False
                drawing_square = False
                drawing_equilateral_triangle = False
                drawing_rhombus = False
            elif e.key == pygame.K_e:  #равносторонний треуг
                drawing_equilateral_triangle = True
                drawing_rect = False
                drawing_circle = False
                drawing_square = False
                drawing_right_triangle = False
                drawing_rhombus = False
            elif e.key == pygame.K_h:  # ромб
                drawing_rhombus = True
                drawing_rect = False
                drawing_circle = False
                drawing_square = False
                drawing_right_triangle = False
                drawing_equilateral_triangle = False

        screen.blit(canvas, (0, 0))
        pygame.display.flip()

except StopIteration:
    pass

pygame.quit()