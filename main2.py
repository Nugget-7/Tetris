import pygame
from copy import deepcopy
from random import randrange, choice

# Libreria de componentes de Feli
from PygameComponents.Fbutton import FButton

W, H = 10, 20
TILE = 37
GAME_RES = W * TILE, H * TILE
RES = 700, 785
FPS = 60
jugando = False
ranking = False

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

figures_pos = [
    [(-1, 0), (-2, 0), (0, 0), (1, 0)],
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, 0)]
]

colors = [
    (0, 255, 255),    # I - cyan
    (255, 255, 0),    # O - yellow
    (255, 0, 0),      # S - red
    (0, 255, 0),      # Z - green
    (255, 165, 0),    # L - orange
    (255, 105, 180),  # J - pink
    (160, 0, 160)     # T - purple
]

# Colores constantes
COLOR_BTN_NORMAL = (80, 47, 120)
COLOR_BTN_HOVER = (176, 201, 15)

# Tarea
# IMAGEN_NORMAL = "imagenes/folder_Vacio.png"
# IMAGEN_ON_HOVER = "imagenes/folder_lleno.png"
# button1 = FButton(....... IMAGEN_NORMAL, IMAGEN_ON_HOVER)


figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)

field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

bg = pygame.image.load("Assets/bg.jpg")
game_bg = pygame.image.load("Assets/bg2.jpg")

main_font = pygame.font.Font('Assets/font.ttf', 65)
big_font = pygame.font.Font('Assets/font.ttf', 90)
font = pygame.font.Font('Assets/font.ttf', 45)

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_tetris_menu = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))

figure_index = randrange(len(figures))
next_figure_index = randrange(len(figures))

figure = deepcopy(figures[figure_index])
next_figure = deepcopy(figures[next_figure_index])

color = colors[figure_index]
next_color = colors[next_figure_index]

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

hard_drop = False


def check_borders():
    for i in range(4):
        if figure[i].x < 0 or figure[i].x > W - 1:
            return False
        elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
            return False
    return True


def get_record():
    try:
        with open('record.txt') as f:
            return f.readline().strip()
    except FileNotFoundError:
        with open('record.txt', 'w') as f:
            f.write('0')
        return '0'


def set_record(record, score):
    rec = max(int(record), score)
    with open('record.txt', 'w') as f:
        f.write(str(rec))

# tarea
# def guardar_puntaje y jugador:

# tarea
# leer de archivo para cargar el ranking

while True:
    mouse_pos = pygame.mouse.get_pos()

    opcion1 = FButton(232, 280, 215, 65, ">Play", COLOR_BTN_NORMAL, COLOR_BTN_HOVER, main_font)
    opcion2 = FButton(180, 480, 360, 65, ">Ranking", COLOR_BTN_NORMAL, COLOR_BTN_HOVER, main_font)

    hover_1 = opcion1.hover(mouse_pos)
    # if opcion1.hover(mouse_pos):
        # 1color_opcion1 = (176, 201, 15)

    # VERSION ANTIGUA
    # if opcion1.click():
        # jugando = True

    # MEJORA

    # 2 else:
    #  3   color_opcion1 = (80, 47, 120)

    hover_2 = opcion2.hover(mouse_pos)
    # if opcion2.hover(mouse_pos):
        # 4 color_opcion2 = (176, 201, 15)
    # 5else:
    # 6 color_opcion2 = (80, 47, 120)

    # Tarea 
    #if opcion2.click():
        #ranking = True 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if opcion1.click(event):
            jugando = True

        if opcion2.click(event):
            ranking = True

    sc.blit(bg, (0, 0))

    opcion1_txt = opcion1.txt_img
    opcion2_txt = opcion2.txt_img

    sc.blit(title_tetris_menu, (222, 20))
    sc.blit(opcion1_txt, (232, 280))
    sc.blit(opcion2_txt, (180, 480))

    if jugando:
        break
    if ranking:
        break

    pygame.display.flip()
    clock.tick(FPS)

if jugando:
    while True:
        record = get_record()
        dx, rotate = 0, False

        sc.blit(bg, (0, 0))
        sc.blit(game_sc, (20, 20))
        game_sc.blit(game_bg, (0, 0))

        for i in range(lines):
            pygame.time.wait(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        dx = -1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        dx = 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        anim_limit = 100
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        rotate = True
                    elif event.key == pygame.K_SPACE:
                        hard_drop = True
                        anim_limit = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    anim_limit = 2000

        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break

        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break

        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color
                    figure_index = next_figure_index
                    figure, color = next_figure, next_color
                    next_figure_index = randrange(len(figures))
                    next_figure = deepcopy(figures[next_figure_index])
                    next_color = colors[next_figure_index]

                    if hard_drop:
                        hard_drop = False

                    anim_limit = 2000
                    break

        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                lines += 1

        score += scores[lines]

        [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

        for i in range(4):
            pygame.draw.rect(game_sc,color,(figure[i].x * TILE, figure[i].y * TILE, TILE - 2, TILE - 2))

            pygame.draw.rect(sc,next_color,(next_figure[i].x * TILE + 330,next_figure[i].y * TILE + 100,TILE - 2,TILE - 2))

        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    pygame.draw.rect(game_sc, col, (x * TILE, y * TILE, TILE - 2, TILE - 2))

        for i in range(4):
            figure_rect.x = next_figure[i].x * TILE + 330
        figure_rect.y = next_figure[i].y * TILE + 100
        pygame.draw.rect(sc, next_color, figure_rect)

        sc.blit(title_tetris, (415, 20))
        sc.blit(title_score, (465, 640))
        sc.blit(font.render(str(score), True, pygame.Color('white')), (525, 700))

        sc.blit(title_record, (465, 510))
        sc.blit(font.render(record, True, pygame.Color('gold')), (525, 570))

        for i in range(W):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                for i_rect in grid:
                    pygame.draw.rect(game_sc, choice(colors), i_rect)
                    sc.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)

        sc.blit(game_sc, (20, 20))
        pygame.display.flip()
        clock.tick(FPS)

#elif ranking:
        #while ranking:
            #sc.fill((0, 0, 0)) # Clean empty screen
            #for event in pygame.event.get():
                #if event.type == pygame.QUIT: exit()
                #if event.type == pygame.KEYDOWN: ranking = False
            #pygame.display.flip()
            #clock.tick(FPS)