import pygame
from Servicios.archivos import Manejador_Archivos
from Modelos.Jugador import Jugador
from copy import deepcopy
from random import randrange, choice
from PygameComponents.Fbutton import FButton
from PygameComponents.FEntry import Fentry
import time
import threading

# Libreria de componentes de Feli
from PygameComponents.Fbutton import FButton
import random

global puntajes, nombre_j, lines

manejador_a = Manejador_Archivos()

jugadores = manejador_a.cargar_jugadores()

nombre_j = ""
puntajes = []
secs = 1
mins = 0
secs_count = 0
flag_jugar = False

W, H = 10, 20
TILE = 37
GAME_RES = W * TILE, H * TILE
RES = 700, 785
FPS = 60
jugando = False
in_ranking = False
pidiendo_nombre = False
in_settings = False
sfx_volume = 1
music_volume = 0.3

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Assets/Music/Tetris_main.mp3')
line_clear_sound = pygame.mixer.Sound("Assets/Music/Tetris_line.mp3")
pygame.mixer.music.set_volume(sfx_volume)
pygame.mixer.music.set_volume(music_volume)
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

anim_count, anim_speed, anim_limit = 0, 40, 2000

bg = pygame.image.load("Assets/bg.jpg")
game_bg = pygame.image.load("Assets/bg2.jpg")

main_font = pygame.font.Font('Assets/font.ttf', 65)
big_font = pygame.font.Font('Assets/font.ttf', 90)
font = pygame.font.Font('Assets/font.ttf', 45)              
small_font = pygame.font.SysFont("Arial", 30)
small_retro_font = pygame.font.Font('Assets/font.ttf', 25)
gear = pygame.image.load("Assets/gear.png")
gear = pygame.transform.scale(gear, (100, 100))

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_tetris_menu = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))
title_time = main_font.render('00:01', True, pygame.Color('white'))
settings_list = [font.render('Music Volume:', True, COLOR_BTN_NORMAL),
                font.render('SFX Volume:', True, COLOR_BTN_NORMAL),
                font.render('Difficulty:', True, COLOR_BTN_NORMAL)] 

figure_index = randrange(len(figures))
next_figure_index = randrange(len(figures))

figure = deepcopy(figures[figure_index])
next_figure = deepcopy(figures[next_figure_index])

color = colors[figure_index]
next_color = colors[next_figure_index]

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

hard_drop = False

name = Fentry(150, 150, 400, 40, place_holder="Type Your Name", max_len=20, bg_color=(200, 200, 222), bg_color_active=(156, 156, 168),
            border_color=(0, 0, 0), border_color_active=(80, 47, 120), place_holder_color=(120, 120, 120), cursor_color=(0, 0, 0),
            txt_color=(0, 0, 0))

name.init()


def verificar_jugador(nombre):
    jugadores_v = manejador_a.cargar_jugadores()
    for jugador in jugadores_v:
        if jugador.nombre == nombre:
            return True
    return False


def check_borders():
    for i in range(4):
        if figure[i].x < 0 or figure[i].x > W - 1:
            return False
        elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
            return False
    return True


def get_record():
    global nombre_j
    jugadores_gr = manejador_a.cargar_jugadores()

    for jugador in jugadores_gr:
        if jugador.nombre == nombre_j:
            return str(jugador.puntaje)
    return "0"


""" def set_record(record, score):
    archivo = manejador_a.cargar_jugadores()
    if int(score) > int(record):
        archivo[0].puntaje = int(score)
        with open("record.txt", "w") as f:
            f.write(str(score))
    else:
        archivo[0].puntaje = int(record)
        with open("record.txt", "w") as f:
            f.write(str(record))
    manejador_a.guardar_jugadores(archivo) """

def set_record(score):
    global nombre_j
    archivo = manejador_a.cargar_jugadores()
    encontrado = False

    for jugador in archivo:
        if jugador.nombre == nombre_j:
            if score > jugador.puntaje:
                jugador.puntaje = score
            encontrado = True
            break
    if not encontrado:
        archivo.append(Jugador(nombre_j, score))

    manejador_a.guardar_jugadores(archivo)

def obtener_puntajes():
    global puntajes
    for j in jugadores:
        puntajes.append(j.puntaje)

def ordenar_puntajes():
    global puntajes
    puntajes = sorted(puntajes)

def format_to_time(time):
    if time < 10:
        return f'0{str(time)}'
    else:
        return str(time)


def set_deafaults():
    global score, lines, color, figure_index, next_color, next_figure_index, hard_drop, figures, figures_pos, figure_rect, anim_count, anim_speed, anim_limit, field, W, H, grid, secs, mins, title_time, main_font, figure, figure_old
    score, lines = 0, 0
    hard_drop = False
    figure_index = randrange(len(figures))
    next_figure_index = randrange(len(figures))
    figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    anim_count, anim_speed, anim_limit = 0, 40, 2000
    field = [[0 for i in range(W)] for i in range(H)]
    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
    secs = 1
    mins = 0
    title_time = main_font.render('00:01', True, pygame.Color('white'))
    y_max = max_y(figure[figure_index + 1])
    for f in figure:
        f.y -= y_max

def max_y(lista):
    maximo = -1
    for i in lista:
        if i > maximo:
            maximo = i
    return maximo

# tarea
# def guardar_puntaje y jugador:

# tarea
# leer de archivo para cargar el ranking

def ranking():
        while ranking:
            sc.blit(bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    exit()

            jugadores_ordenados = sorted(jugadores, key=lambda j: j.puntaje, reverse=True)

            record = get_record()

            lista_pos = [(70, 150), (70, 300), (70, 450), (70, 600)]

            ranking_pos = ["1. ", "2. ", "3. ", "4. "]

            persona_1 = font.render(f"{ranking_pos[0]}{jugadores_ordenados[0].nombre} - Score: {jugadores_ordenados[0].puntaje}", True, (80, 47, 120))
            persona_2 = font.render(f"{ranking_pos[1]}{jugadores_ordenados[1].nombre} - Score: {jugadores_ordenados[1].puntaje}", True, (80, 47, 120))
            persona_3 = font.render(f"{ranking_pos[2]}{jugadores_ordenados[2].nombre} - Score: {jugadores_ordenados[2].puntaje}", True, (80, 47, 120))
            persona_4 = font.render(f"{ranking_pos[3]}{jugadores_ordenados[3].nombre} - Score: {jugadores_ordenados[3].puntaje}", True, (80, 47, 120))

            sc.blit(title_tetris_menu, (222, 20))
            sc.blit(persona_1, lista_pos[0])
            sc.blit(persona_2, lista_pos[1])
            sc.blit(persona_3, lista_pos[2])
            sc.blit(persona_4, lista_pos[3])


            pygame.display.flip()
            clock.tick(FPS)

def settings_funcion():
    global music_volume, sfx_volume
    not_salir = True
    setting_entrys = [Fentry(400, 250, 100, 45, str(sfx_volume), numeric=True, font=small_retro_font ,max_len=5, bg_color=(92, 63, 128), bg_color_active=COLOR_BTN_NORMAL,
                        border_color=(156, 156, 168), border_color_active=(255, 255, 255), place_holder_color=COLOR_BTN_HOVER, cursor_color=(0, 0, 0),
                        txt_color=COLOR_BTN_HOVER), 
                        Fentry(450, 159.5, 100, 45, str(music_volume), numeric=True, font=small_retro_font ,max_len=5, bg_color=(92, 63, 128), bg_color_active=COLOR_BTN_NORMAL,
                        border_color=(156, 156, 168), border_color_active=(255, 255, 255), place_holder_color=COLOR_BTN_HOVER, cursor_color=(0, 0, 0),
                        txt_color=COLOR_BTN_HOVER)]
    while not_salir:
        setting_entrys[0].place_holder = str(sfx_volume)
        setting_entrys[1].place_holder = str(music_volume)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    not_salir = False
                    menu()
            for setting_entry in setting_entrys:
                setting_entry.handle_event(event)
        
        #music_volume = int(setting_entrys[0].get_value())
        #sfx_volume = int(setting_entrys[1].get_value())

        if setting_entrys[1].get_value() != "":
            music_volume = float(setting_entrys[1].get_value())

        if setting_entrys[0].get_value() != "":
            sfx_volume = float(setting_entrys[0].get_value())

        line_clear_sound.set_volume(sfx_volume)
        pygame.mixer.music.set_volume(music_volume)

        for entry in setting_entrys:
            entry.update(clock.tick(60))

        sc.blit(bg, (0, 0))

        sc.blit(title_tetris_menu, (222, 20))
        for setting in settings_list:
            index = settings_list.index(setting)
            index += 1
            sc.blit(setting, (75, index * 100 + 50))
        for entry in setting_entrys:
            entry.init()
            entry.draw(sc)

        pygame.display.flip()
        clock.tick(FPS)
    menu()

def pedir_nombre():
    global puntajes, nombre_j, lines, flag_jugar
    salir = False
    while not salir:
        sc.blit(bg, (0, 0))

        submit = FButton(300, 650, 180, 30, "Submit", (0, 0, 0), (0, 0, 0), small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            name.handle_event(event)

            if submit.click(event):
                if data.replace("_", "") != "":
                    print(data)
                    nombre_j = data
                    flag_jugar = True
                    salir = True
        
        name.update(clock.tick(60))

        submit_txt = submit.txt_img

        sc.blit(title_tetris_menu, (222, 20))
        pygame.draw.rect(sc, (255, 255, 255), (295, 650, 90, 38))
        pygame.draw.rect(sc, (0, 0, 0), (295, 650, 90, 38), 1)
        sc.blit(submit_txt, (300, 650))
        
        name.draw(sc)
        data = name.get_value()
        data = data.replace(" ", "_")

        pygame.display.flip()
        clock.tick(FPS)
    if flag_jugar:
        jugar()

def jugar():
    set_deafaults()
    global puntajes, nombre_j, lines, figure, anim_count, anim_speed, anim_limit, field, score, color, next_color, next_figure, title_time
    global secs_count, secs, mins, next_figure_index, hard_drop, figure_old
    pygame.mixer.music.play(-1)
    salir = False
    while not salir:
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
                    elif event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        salir = True
                        menu()
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
        if lines > 0:
                line_clear_sound.play()

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
        sc.blit(title_time, (465, 345))

        sc.blit(title_record, (465, 510))
        sc.blit(font.render(record, True, pygame.Color('gold')), (525, 570))

        for i in range(W):
            if field[0][i]:
                set_record(score)
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 40, 2000
                secs = 1
                mins = 0
                score = 0
                set_deafaults()
                for i_rect in grid:
                    pygame.draw.rect(game_sc, choice(colors), i_rect)
                    sc.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)

        sc.blit(game_sc, (20, 20))
        pygame.display.flip()
        clock.tick(FPS)
        secs_count += 1
        if secs_count == FPS:
            secs_count = 0
            secs += 1
            title_time = main_font.render(f'{format_to_time(mins)}:{format_to_time(secs)}', True, pygame.Color('white'))
            if secs % 15 == 0:
                anim_speed += 10
            if secs % 60 == 0:
                mins += 1

def menu():
    global in_ranking, in_settings, flag_jugar
    opcion = 0
    while opcion == 0:
        mouse_pos = pygame.mouse.get_pos()

        opcion1 = FButton(232, 280, 215, 65, ">Play", COLOR_BTN_NORMAL, COLOR_BTN_HOVER, main_font)
        opcion2 = FButton(180, 480, 360, 65, ">Ranking", COLOR_BTN_NORMAL, COLOR_BTN_HOVER, main_font)
        settings =FButton(575, 20, 100, 100, "", pygame.Color('White'), pygame.Color('White'), small_font, gear)

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
                opcion = 1

            if opcion2.click(event):
                opcion = 2
            
            if settings.click(event):
                opcion = 3

        sc.blit(bg, (0, 0))

        opcion1_txt = opcion1.txt_img
        opcion2_txt = opcion2.txt_img
        settings_img = settings.img

        sc.blit(title_tetris_menu, (222, 20))
        sc.blit(opcion1_txt, (232, 280))
        sc.blit(opcion2_txt, (180, 480))
        sc.blit(settings_img, (575, 20))

        pygame.display.flip()
        clock.tick(FPS)
    match opcion:
        case 1:
            pedir_nombre()
        case 2:
            ranking()
        case 3:
            settings_funcion()

menu()