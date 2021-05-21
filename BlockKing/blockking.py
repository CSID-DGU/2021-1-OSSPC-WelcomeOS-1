# -*-coding:utf-8-*-
# PYTRIS Copyright (c) 2017 Jason Kim All Rights Reserved.

import pygame
import operator
import wave
from mino import *
from random import *
from pygame.locals import *
import os
from ai import Ai

# Unchanged values Define 변하지 않는 변수 선언
computed = 5 # 5 이하 이면 자동으로 블록 쌓아줌 
hint_item_num = 0 #자동 추천 기능 쓸 수 있는 횟수 
weights = [0.39357083734159515, -1.8961941343266449, -5.107694873375318, -3.6314963941589093, -2.9262681134021786, -2.146136640641482, -7.204192964669836, -3.476853402227247, -6.813002842291903, 4.152001386170861, -21.131715861293525, -10.181622180279133, -5.351108175564556, -2.6888972099986956, -2.684925769670947, -4.504495386829769, -7.4527302422826, -6.3489634714511505, -4.701455626343827, -10.502314845278828, 0.6969259450910086, -4.483319180395864, -2.471375907554622, -6.245643268054767, -1.899364785170105, -5.3416512085013395, -4.072687054171711, -5.936652569831475, -2.3140398163110643, -4.842883337741306, 17.677262456993276, -4.42668539845469, -6.8954976464473585, 4.481308299774875] 



block_size = 17  # Height, width of single block
width = 10
height = 20

board_x = 10
board_y = 20
board_width = 800 # Board width
board_height = 450 # Board height
board_rate = 0.5625 #가로세로비율
block_size = int(board_height * 0.045)
mino_matrix_x = 4 #mino는 4*4 배열이어서 이를 for문에 사용
mino_matrix_y = 4 #mino는 4*4 배열이어서 이를 for문에 사용

speed_change = 50 # 레벨별 블록 하강 속도 상승 정도

min_width = 400
min_height = 225
mid_width = 1200

total_time = 60 # 타임 어택 시간
waiting_time= 1 # 블록이 바닥에 닿은 후 다음 블록 생성까지 기다리는 시간

# 기본 볼륨
music_volume = 5
effect_volume = 5

initalize = True

pygame.init()

clock = pygame.time.Clock() #창, 화면을 초당 몇번 출력하는가(FPS) clock.tick 높을수록 cpu많이 사용
screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE) #GUI창 설정하는 변수
pygame.display.set_caption("BLOCK KING") #GUI 창의 이름

class ui_variables:
    font_path = "./assets/fonts/OpenSans-Light.ttf"
    font_path_b = "./assets/fonts/OpenSans-Bold.ttf"
    font_path_i = "./assets/fonts/Inconsolata/Inconsolata.otf"

    # Font(글씨체, 글자크기)
    h1 = pygame.font.Font(font_path_b, 80)
    h2 = pygame.font.Font(font_path_b, 30)
    h3 = pygame.font.Font(font_path_b, 25)
    h4 = pygame.font.Font(font_path_b, 20)
    h5 = pygame.font.Font(font_path_b, 13)
    h6 = pygame.font.Font(font_path_b, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    h2_i = pygame.font.Font(font_path_i, 30)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Sounds
    pygame.mixer.music.load("assets/sounds/SFX_BattleMusic.wav") #음악 불러옴
    pygame.mixer.music.set_volume(0.5) # 이 부분도 필요 없음, set_volume에 추가해야 함
    intro_sound = pygame.mixer.Sound("assets/sounds/SFX_Intro.wav")
    fall_sound = pygame.mixer.Sound("assets/sounds/SFX_Fall.wav")
    break_sound = pygame.mixer.Sound("assets/sounds/SFX_Break.wav")
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav") #여기부터
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav") #여기까지는 기존코드
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")
    LevelUp_sound = pygame.mixer.Sound("assets/sounds/SFX_LevelUp.wav")
    GameOver_sound = pygame.mixer.Sound("assets/sounds/SFX_GameOver.wav")

    # Combo graphic
    combos = []
    large_combos = []
    combo_ring = pygame.image.load("assets/Combo/4combo ring.png")  # 4블록 동시제거 그래픽
    combo_4ring = pygame.transform.smoothscale(combo_ring, (200, 100)) #이미지를 특정 크기로 불러옴, 200=가로크기, 100=세로크기#
    for i in range(1, 11): #10가지의 콤보 이미지 존재. 각 숫자에 해당하는 이미지 불러옴
        combos.append(pygame.image.load("assets/Combo/" + str(i) + "combo.png"))
        large_combos.append(pygame.transform.smoothscale(combos[i - 1], (150, 200))) #콤보이미지를 특정 크기로 불러옴, 150=가로크기, 200=세로크기#

    combos_sound = []
    for i in range(1, 10): #1-9까지 콤보사운드 존재. 각 숫자에 해당하는 음악 불러옴
        combos_sound.append(pygame.mixer.Sound("assets/sounds/SFX_" + str(i + 2) + "Combo.wav"))

    #rainbow 보너스점수 graphic
    rainbow_vector = pygame.image.load('assets/vector/rainbow.png')

    # Background colors. RGB 값에 해당함
    black = (10, 10, 10)  # rgb(10, 10, 10)
    black_pause = (0, 0, 0, 127)
    white = (0, 153, 153)  # rgb(255, 255, 255) # 청록색으로 변경
    real_white = (255, 255, 255)  # rgb(255, 255, 255)
    pinkpurple = (250, 165, 255) #rgb(250, 165, 255) 핑크+보라#

    grey_1 = (70, 130, 180)  # rgb(26, 26, 26) 테두리 파랑색
    grey_2 = (221, 221, 221)  # rgb(35, 35, 35)
    grey_3 = (000, 000, 139)  # rgb(55, 55, 55) #남색
    bright_yellow = (255, 217, 102)  # 밝은 노랑

    # Tetrimino colors. RGB 값에 해당함
    cyan = (10, 255, 226)  # rgb(69, 206, 204) # I
    blue = (64, 105, 255)  # rgb(64, 111, 249) # J
    orange = (245, 144, 12)  # rgb(253, 189, 53) # L
    yellow = (225, 242, 41)  # rgb(246, 227, 90) # O
    green = (22, 181, 64)  # rgb(98, 190, 68) # S
    pink = (242, 41, 195)  # rgb(242, 64, 235) # T
    red = (204, 22, 22)  # rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]
    cyan_image = 'assets/block_images/cyan.png'
    blue_image = 'assets/block_images/blue.png'
    orange_image = 'assets/block_images/orange.png'
    yellow_image = 'assets/block_images/yellow.png'
    green_image = 'assets/block_images/green.png'
    pink_image = 'assets/block_images/purple.png'
    red_image = 'assets/block_images/red.png'
    ghost_image = 'assets/block_images/ghost.png'
    table_image = 'assets/block_images/background.png'
    linessent_image = 'assets/block_images/linessent.png'
    t_block = [table_image, cyan_image, blue_image, orange_image, yellow_image, green_image, pink_image, red_image,
               ghost_image, linessent_image]

#각 이미지 주소
background_image = 'assets/vector/kingdom.jpg' #홈 배경화면
gamebackground_image = 'assets/vector/snowymountains.png' #게임 배경화면

single_button_image = 'assets/vector/single_button.png'
clicked_single_button_image = 'assets/vector/clicked_single_button.png'

pvp_button_image = 'assets/vector/pvp_button.png'
clicked_pvp_button_image = 'assets/vector/clicked_pvp_button.png'

help_button_image = 'assets/vector/help_button.png'
clicked_help_button_image = 'assets/vector/clicked_help_button.png'

quit_button_image = 'assets/vector/quit_button.png'
clicked_quit_button_image = 'assets/vector/clicked_quit_button.png'

gravity_button_image = 'assets/vector/gravity_button.png'
clicked_gravity_button_image = 'assets/vector/clicked_gravity_button.png'

timeattack_button_image = 'assets/vector/timeattack_button.png'
clicked_timeattack_button_image = 'assets/vector/clicked_timeattack_button.png'

leaderboard_vector = 'assets/vector/leaderboard_vector.png'
clicked_leaderboard_vector = 'assets/vector/clicked_leaderboard_vector.png'

setting_vector = 'assets/vector/setting_vector.png'
clicked_setting_vector = 'assets/vector/clicked_setting_vector.png'

pause_board_image = 'assets/vector/pause_board.png'
leader_board_image = 'assets/vector/leader_board.png'
setting_board_image = 'assets/vector/setting_board.png'
gameover_board_image = 'assets/vector/gameover_board.png'
gameover_image = 'assets/vector/gameover.png'

smallsize_board = 'assets/vector/screensize1.png'
midiumsize_board = 'assets/vector/screensize2.png'
bigsize_board = 'assets/vector/screensize3.png'

mute_button_image = 'assets/vector/allmute_button.png'
default_button_image = 'assets/vector/default_button.png'

number_board = 'assets/vector/number_board.png'

resume_button_image = 'assets/vector/resume_button.png'
clicked_resume_button_image = 'assets/vector/clicked_resume_button.png'

restart_button_image = 'assets/vector/restart_button.png'
clicked_restart_button_image = 'assets/vector/clicked_restart_button.png'

setting_button_image = 'assets/vector/setting_button.png'
clicked_setting_button_image = 'assets/vector/clicked_setting_button.png'

back_button_image = 'assets/vector/back_button.png'
clicked_back_button_image = 'assets/vector/clicked_back_button.png'

volume_vector = 'assets/vector/volume_vector.png'
clicked_volume_vector = 'assets/vector/clicked_volume_vector.png'

keyboard_vector = 'assets/vector/keyboard_vector.png'
clicked_keyboard_vector = 'assets/vector/clicked_keyboard_vector.png'

screen_vector = 'assets/vector/screen_vector.png'
clicked_screen_vector = 'assets/vector/clicked_screen_vector.png'

menu_button_image = 'assets/vector/menu_button.png'
clicked_menu_button_image = 'assets/vector/clicked_menu_button.png'

ok_button_image = 'assets/vector/ok_button.png'
clicked_ok_button_image = 'assets/vector/clicked_ok_button.png'

plus_button_image = 'assets/vector/plus_button.png'
clicked_plus_button_image = 'assets/vector/clicked_plus_button.png'

minus_button_image = 'assets/vector/minus_button.png'
clicked_minus_button_image = 'assets/vector/clicked_minus_button.png'
#음소거 추가#
sound_off_button_image = 'assets/vector/sound_off_button.png'
sound_on_button_image = 'assets/vector/sound_on_button.png'

check_button_image = 'assets/vector/checkbox_button.png'
clicked_check_button_image = 'assets/vector/clicked_checkbox_button.png'

pvp_win_image = 'assets/vector/pvp_win.png'
pvp_lose_image = 'assets/vector/pvp_lose.png'


class button(): #버튼객체
    def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img=''): #버튼생성
        self.x = board_width * x_rate #버튼 x좌표
        self.y = board_height * y_rate #버튼 y좌표
        self.width = int(board_width * width_rate) #버튼 너비
        self.height = int(board_height * height_rate) #버튼 높이
        self.x_rate = x_rate #board_width * x_rate = x좌표
        self.y_rate = y_rate #board_height * y_rate = y좌표
        self.width_rate = width_rate #board_width * width_rate = 버튼 너비
        self.height_rate = height_rate #board_height * height_rate = 버튼 높이
        self.image = img #불러올 버튼 이미지

    def change(self, board_width, board_height): #버튼 위치, 크기 바꾸기
        self.x = board_width * self.x_rate #x좌표
        self.y = board_height * self.y_rate #y좌표
        self.width = int(board_width * self.width_rate) #너비
        self.height = int(board_height * self.height_rate) #높이

    def draw(self, win, outline=None): #버튼 보이게 만들기
        if outline:
            draw_image(screen, self.image, self.x, self.y, self.width, self.height)

    def isOver(self, pos): #마우스의 위치에 따라 버튼 누르기 pos[0]은 마우스 x좌표, pos[1]은 마우스 y좌표
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 2) and pos[1] < self.y + (self.height / 2):
                return True
        return False

    def isOver_2(self, pos): #start 화면에서 single,pvp,help,setting을 위해서 y좌표 좁게 인식하도록
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 4) and pos[1] < self.y + (self.height / 4):#243줄에서의 2을 4로 바꿔주면서 좁게 인식할수 있도록함. 더 좁게 인식하고 싶으면 숫자 늘려주기#
                return True
        return False

#버튼객체 생성 class Button에서 확인
#def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img='')
#(현재 보드너비, 현재보드높이, 버튼의 x좌표 위치비율, 버튼의 y좌표 위치비율, 버튼의 너비 길이비율, 버튼의 높이 길이비율) - 전체화면 크기에 대한 비율

mute_button = button(board_width, board_height, 0.5, 0.27, 0.25, 0.45, mute_button_image)
default_button = button(board_width, board_height, 0.5, 0.27, 0.25, 0.45, default_button_image)

single_button = button(board_width,board_height, 0.12, 0.55, 0.235, 0.435, single_button_image)
pvp_button = button(board_width, board_height, 0.35, 0.55, 0.235, 0.435, pvp_button_image)
help_button = button(board_width, board_height, 0.12, 0.8, 0.235, 0.435, help_button_image)
quit_button = button(board_width, board_height, 0.35, 0.8, 0.235, 0.435, quit_button_image)
gravity_button = button(board_width, board_height, 0.58, 0.55, 0.235, 0.435, gravity_button_image)
timeattack_button = button(board_width, board_height, 0.58, 0.8, 0.235, 0.435, timeattack_button_image)
setting_icon = button(board_width, board_height, 0.9, 0.85, 0.10, 0.15, setting_vector)
leaderboard_icon = button(board_width, board_height, 0.77, 0.85, 0.15, 0.2, leaderboard_vector)

resume_button = button(board_width, board_height, 0.5, 0.23, 0.15, 0.35, resume_button_image)
restart_button = button(board_width, board_height, 0.5, 0.43, 0.15, 0.35, restart_button_image)
setting_button = button(board_width, board_height, 0.5, 0.63, 0.15, 0.35, setting_button_image)
pause_quit_button = button(board_width, board_height, 0.5, 0.83, 0.15, 0.35, quit_button_image)

back_button = button(board_width, board_height, 0.5, 0.85, 0.15, 0.35, back_button_image)
volume_icon = button(board_width, board_height, 0.4, 0.5, 0.12, 0.23, volume_vector)
screen_icon = button(board_width, board_height, 0.6, 0.5, 0.12, 0.23, screen_vector)
ok_button = button(board_width, board_height, 0.5, 0.83, 0.15, 0.35, ok_button_image)

volume = 1.0

menu_button = button(board_width, board_height, 0.5, 0.23, 0.15, 0.35, menu_button_image)
gameover_quit_button = button(board_width, board_height, 0.5, 0.43, 0.15, 0.35, quit_button_image)

effect_plus_button = button(board_width, board_height, 0.37, 0.73, 0.0625, 0.1111, plus_button_image)
effect_minus_button = button(board_width, board_height, 0.52, 0.73, 0.0625, 0.1111, minus_button_image)

sound_plus_button = button(board_width, board_height, 0.37, 0.53, 0.0625, 0.1111, plus_button_image)
sound_minus_button = button(board_width, board_height, 0.52, 0.53, 0.0625, 0.1111, minus_button_image)
level_plus_button = button(board_width, board_height, 0.63, 0.7719, 0.0625, 0.1111, plus_button_image)
level_minus_button = button(board_width, board_height, 0.56, 0.7719, 0.0625, 0.1111, minus_button_image)
combo_plus_button = button(board_width, board_height, 0.63, 0.9419, 0.0625, 0.1111, plus_button_image)
combo_minus_button =button(board_width, board_height, 0.56, 0.9419, 0.0625, 0.1111, minus_button_image)
speed_plus_button = button(board_width, board_height, 0.18, 0.12, 0.055, 0.09, plus_button_image)
speed_minus_button =button(board_width, board_height, 0.035, 0.12, 0.055, 0.09, minus_button_image)

#음소거 추가#
effect_sound_off_button = button(board_width, board_height, 0.65, 0.73, 0.08, 0.15, sound_off_button_image)
music_sound_off_button = button(board_width, board_height, 0.65, 0.53, 0.08, 0.15, sound_off_button_image)
effect_sound_on_button = button(board_width, board_height, 0.65, 0.73, 0.08, 0.15, sound_on_button_image)
music_sound_on_button = button(board_width, board_height, 0.65, 0.53, 0.08, 0.15, sound_on_button_image)

mute_check_button = button(board_width, board_height, 0.2, 0.4, 0.0625, 0.1111, check_button_image)
smallsize_check_button = button(board_width, board_height, 0.5, 0.25, 0.1875, 0.1444, smallsize_board)
midiumsize_check_button = button(board_width, board_height, 0.5, 0.45, 0.1875, 0.1444, midiumsize_board)
bigsize_check_button = button(board_width, board_height, 0.5, 0.65, 0.1875, 0.1444, bigsize_board)

#게임 중 버튼 생성하기위한 버튼객체 리스트 (버튼 전체)
button_list = [mute_button, default_button, single_button, pvp_button, help_button, quit_button, gravity_button, timeattack_button, resume_button, restart_button, setting_button, pause_quit_button, back_button,
        ok_button, menu_button, gameover_quit_button, effect_plus_button, effect_minus_button, sound_plus_button, sound_minus_button, level_plus_button,
        effect_sound_off_button, music_sound_off_button, effect_sound_on_button, music_sound_on_button, mute_check_button, smallsize_check_button, midiumsize_check_button, bigsize_check_button,
        setting_icon, leaderboard_icon, volume_icon, screen_icon, level_minus_button, combo_minus_button, combo_plus_button, speed_minus_button, speed_plus_button]


def set_volume():
    ui_variables.fall_sound.set_volume(effect_volume / 10) #set_volume의 argument는 0.0~1.0으로 이루어져야하기 때문에 소수로 만들어주기 위해 10으로 나눔#
    ui_variables.click_sound.set_volume(effect_volume / 10)
    ui_variables.break_sound.set_volume(effect_volume / 10)
    ui_variables.move_sound.set_volume(effect_volume / 10)
    ui_variables.drop_sound.set_volume(effect_volume / 10)
    ui_variables.single_sound.set_volume(effect_volume / 10)
    ui_variables.double_sound.set_volume(effect_volume / 10)
    ui_variables.triple_sound.set_volume(effect_volume / 10)
    ui_variables.tetris_sound.set_volume(effect_volume / 10)
    ui_variables.LevelUp_sound.set_volume(effect_volume / 10)
    ui_variables.GameOver_sound.set_volume(music_volume / 10)
    ui_variables.intro_sound.set_volume(music_volume / 10)
    pygame.mixer.music.set_volume(music_volume / 10)
    for i in range(1, 10): #10가지의 combo 사운드를 한번에 조절함
        ui_variables.combos_sound[i - 1].set_volume(effect_volume / 10)


def draw_image(window, img_path, x, y, width, height):
    x = x - (width / 2) #해당 이미지의 가운데 x좌표, 가운데 좌표이기 때문에 2로 나눔
    y = y - (height / 2) #해당 이미지의 가운데 y좌표, 가운데 좌표이기 때문에 2로 나눔
    image = pygame.image.load(img_path)
    image = pygame.transform.smoothscale(image, (width, height))
    window.blit(image, (x, y))


# Draw block
def draw_block(x, y, color):
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )


def draw_block_image(x, y, image):
    draw_image(screen, image, x, y, block_size, block_size) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)


# grid[i][j] = 0 / matrix[tx + j][ty + i] = 0에서
# 0은 빈 칸 / 1-7은 테트리스 블록 종류 / 8은 ghost / 9은 장애물(벽돌) 에 해당함 = t_block 참고

# Draw game screen
def draw_board(next1, next2, hold, score, level, goal):
    sidebar_width = int(board_width * 0.5312) #크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.pinkpurple,
        Rect(sidebar_width, 0, int(board_width * 0.2375), board_height) #크기 비율 고정
    )

    # Draw next mino 다음 블록
    grid_n1 = tetrimino.mino_map[next1 - 1][0] #(배열이라-1) 다음 블록의 원래 모양
    grid_n2 = tetrimino.mino_map[next2 - 1][0] #(배열이라-1) 다음 블록의 원래 모양

    for i in range(mino_matrix_y): #다음 블록
        for j in range(mino_matrix_x):
            dx1 = int(board_width * 0.025) + sidebar_width + block_size * j #위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy1 = int(board_height * 0.3743) + block_size * i #위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n1[i][j] != 0: #해당 부분에 블록 존재하면
                draw_block_image(dx1, dy1, ui_variables.t_block[grid_n1[i][j]]) #블록 이미지 출력

    for i in range(mino_matrix_y): #다다음블록
        for j in range(mino_matrix_x):
            dx2 = int(board_width * 0.145) + sidebar_width + block_size * j #위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy2 = int(board_height * 0.3743) + block_size * i #위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n2[i][j] != 0: #해당 부분에 블록 존재하면
                draw_block_image(dx2, dy2, ui_variables.t_block[grid_n2[i][j]]) #블록 이미지 출력

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  #(배열이라-1) 기본 모양

    if hold_mino != -1: #hold 존재X
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + block_size * j #위치 비율 고정
                dy = int(board_height * 0.1336) + block_size * i #위치 비율 고정
                if grid_h[i][j] != 0: #해당 부분에 블록이 존재하면
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]]) #hold 블록 출력

    # Set max score
    if score > 999999:
        score = 999999 #최대 점수가 999999를 넘기지 못하도록 설정#

    # Draw texts
    #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
    if textsize==False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h4.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.real_white)
        text_hint = ui_variables.h5.render("HINT", 1, ui_variables.real_white)
        hint_value = ui_variables.h4.render(str(hint_item_num), 1, ui_variables.real_white)
        if debug:
            speed_value = ui_variables.h5.render("SPEED : "+str(framerate), 1, ui_variables.real_white) #speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        if time_attack:
            time = total_time - elapsed_time
            value = ui_variables.h5.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
            screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015))) #각각 전체 board 가로길이, 세로길이에 대한 원하는 비율을 곱해줌#

    if textsize==True: #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        text_hold = ui_variables.h3.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h3.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h3.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h2.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h3.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h2.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h3.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h2.render(str(combo_count), 1, ui_variables.real_white)
        text_hint = ui_variables.h3.render("HINT", 1, ui_variables.real_white)
        hint_value = ui_variables.h2.render(str(hint_item_num), 1, ui_variables.real_white)
        if debug:
            speed_value = ui_variables.h3.render("SPEED : "+str(framerate), 1, ui_variables.real_white) #speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        if time_attack:
            time = total_time - elapsed_time
            value = ui_variables.h2.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
            screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015)))

    #if time_attack:
    #    time = total_time - elapsed_time
    #    value = ui_variables.h5.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
    #    screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015)))
    # Place texts. 위치 비율 고정, 각각 전체 board 가로길이, 세로길이에 대한 원하는 비율을 곱해줌#
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))#
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.6791)))#
    screen.blit(level_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.7219)))
    screen.blit(text_combo, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.8395)))#
    screen.blit(combo_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.8823)))
    screen.blit(text_hint, (int(board_width * 0.045) + sidebar_width * 1.2, int(board_height * 0.8395)))
    screen.blit(hint_value, (int(board_width * 0.055) + sidebar_width * 1.2, int(board_height * 0.8823)))
    if debug:
        screen.blit(speed_value, (int(board_width * 0.065), int(board_height * 0.1)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.25) + block_size * x  #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.055) + block_size * y #위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])


def draw_1Pboard(next, hold, score, level, goal):
    sidebar_width = int(board_width * 0.31) #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.pinkpurple,
        Rect(sidebar_width, 0, int(board_width * 0.1875), board_height) #크기비율 고정, board 가로길이에 원하는 비율을 곱해줌#
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]  #(배열이라-1) 다음 블록의 원래 모양

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.045) + sidebar_width + block_size * j #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.3743) + block_size * i #위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  #(배열이라-1) 기본 모양

    if hold_mino != -1: #기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + block_size * j #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
                dy = int(board_height * 0.1336) + block_size * i #위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
                if grid_h[i][j] != 0:
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]]) #hold 블록 그림

    # Set max score
    if score > 999999:
        score = 999999 #최대 점수가 999999가 넘지 않도록 설정해줌

    # Draw texts
    #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
    if textsize==False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h4.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.real_white)
        
    if textsize==True:
        text_hold = ui_variables.h3.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h3.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h3.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h2.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h3.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h2.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h3.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h2.render(str(combo_count), 1, ui_variables.real_white)
        
    if debug:
        speed_value = ui_variables.h5.render("SPEED : "+str(framerate), 1, ui_variables.real_white) #speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.015))) #각각 전체 board 가로길이, 세로길이에 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width*0.045) + sidebar_width, int(board_height*0.6791)))
    screen.blit(level_value, (int(board_width*0.055) + sidebar_width , int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) + sidebar_width , int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) + sidebar_width, int(board_height*0.8823)))
    

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.05) + block_size * x #위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.055) + block_size * y #위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])


def draw_2Pboard(next, hold, score, level, goal):
    sidebar_width = int(board_width * 0.82) #위치 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.pinkpurple,
        Rect(sidebar_width, 0, int(board_width * 0.1875), board_height) #크기 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌, Rect(x축, y축, 가로길이, 세로길이)#
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(mino_matrix_y):  # 16개의 그리드 칸에서 true인 값만 뽑아서 draw.rect
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.05) + sidebar_width + block_size * j  #위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.3743) + block_size * i  #위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino_2P != -1:  #기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + block_size * j  #위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
                dy = int(board_height * 0.1336) + block_size * i  #위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
                if grid_h[i][j] != 0:
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]])

    # Set max score
    if score > 999999:
        score = 999999 #최대 점수가 999999가 넘지 못하도록 설정#

    #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래 코드의 숫자 1=안티에일리어싱 적용에 대한 코드
    if textsize==False: # 창모드일 때 
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h4.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(str(combo_count_2P), 1, ui_variables.real_white) # 2P의 combo count를 문자열로 바꾸어 화면에 띄운다.
    if textsize==True: # 전체화면일 때
        text_hold = ui_variables.h4.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h4.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h4.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h3.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h4.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h3.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h4.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h3.render(str(combo_count_2P), 1, ui_variables.real_white) # 2P의 combo count를 문자열로 바꾸어 화면에 띄운다.
    if debug:
        speed_value = ui_variables.h5.render("SPEED : "+str(framerate_2P), 1, ui_variables.real_white) #speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.015))) #각각 전체 board의 가로길이, 세로길이에 대해 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width*0.045) + sidebar_width, int(board_height*0.6791)))
    screen.blit(level_value, (int(board_width*0.055) + sidebar_width , int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) + sidebar_width , int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) + sidebar_width, int(board_height*0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.54) + block_size * x #위치비율 고정
            dy = int(board_height * 0.055) + block_size * y #위치비율 고정
            draw_block_image(dx, dy, ui_variables.t_block[matrix_2P[x][y + 1]])


# Draw a tetrimino
def draw_mino(x, y, mino, r, matrix): #mino는 모양, r은 회전된 모양 중 하나
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r, matrix): #테트리스가 바닥에 존재하면 true -> not이니까 바닥에 없는 상태
        ty += 1 #한칸 밑으로 하강

    # Draw ghost
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면              
                matrix[tx + j][ty + i] = 8 #테트리스가 쌓일 위치에 8 이라는 ghost 만듦

    # Draw mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = grid[i][j] #해당 위치에 블록 만듦

# Erase a tetrimino
def erase_mino(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(board_y+1):
        for i in range(board_x):
            if matrix[i][j] == 8: #테트리스 블록에서 해당 행렬위치에 ghost블록 존재하면
                matrix[i][j] = 0  #없애서 빈 곳으로 만들기

    # Erase mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = 0 #해당 위치에 블록 없애서 빈 곳으로 만들기

# Returns true if mino is at bottom
def is_bottom(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (y + i + 1) > board_y :   #바닥의 y좌표에 있음(바닥에 닿음)
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8: #그 블록위치에 0, 8 아님(즉 블록 존재 함)
                    return True

    return False

def gravity(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for j in range(mino_matrix_x-1, -1, -1): #mino_matrix 4*4 배열이므로 -1 해서 3, 2, 1, 0 index로 for문을 돎
        for i in range(mino_matrix_y-1, -1, -1):  #mino_matrix 4*4 배열이므로 -1 해서 3, 2, 1, 0 index로 for문을 돎
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                dy = y
                if ((dy + i) == board_y or (matrix[x + j][dy + i+1] != 0)) : #바닥에 닿았거나, 해당 위치 아랫칸에 블록이 이미 존재하는 경우
                    matrix[x+j][dy+i] = grid[i][j] #그 위치에 그대로 테트리스 블록을 둠
                else :
                    while((dy + 1 + i) <= board_y and (matrix[x + j][dy + i + 1] == 0)): #바닥에 닿지 않았으며, 해당 위치 아랫칸에 블록이 없는 경우 (= 공중에 떠있는 경우)
                        dy+=1 #이 조건에서 벗어날 때까지 계속해서 한 칸씩 밑으로 떨어뜨림
                        matrix[x+j][dy+i] = 9  #떨어지는 블록은 장애물 블록으로 표현
                        matrix[x+j][dy+i-1] = 0  #블록이 한칸 떨어졌으니, 그 위의 기존블록 또는 만들어두었던 장애물 블록은 빈칸으로 처리함(없앰)


# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j - 1) < 0:  #맨 왼쪽에 위치함
                    return True
                elif matrix[x + j - 1][y + i] != 0:  #그 위치의 왼쪽에 이미 무엇인가 존재함
                    return True

    return False

# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j + 1) >= board_x :  #맨 오른쪽에 위치
                    return True
                elif matrix[x + j + 1][y + i] != 0:   #그 위치의 오른쪽에 이미 무엇인가 존재함
                    return True

    return False

def is_turnable_r(x, y, mino, r, matrix):
    if r != 3:  #회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r + 1] #3이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][0] #3이면 0번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y :  #테트리스 matrix크기 벗어나면 못돌림
                    return False
                elif matrix[x + j][y + i] != 0:  #해당 자리에 이미 블록이 있으면 못돌림
                    return False
    return True

# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r, matrix):
    if r != 0:  #회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r - 1]  #0이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][3] #0이면 3번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y:  #테트리스 matrix크기 벗어나면 못돌림
                    return False
                elif matrix[x + j][y + i] != 0: #해당 자리에 이미 블록이 있으면 못돌림
                    return False

    return True

# Returns true if new block is drawable
def is_stackable(mino, matrix):
    grid = tetrimino.mino_map[mino - 1][0] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0 and matrix[3 + j][i] != 0: ###
                return False

    return True

def draw_multiboard(next_1P, hold_1P, next_2P, hold_2P, score1P, score2P, level1P, level2P, goal1P, goal2P):
    screen.fill(ui_variables.real_white)
    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
    draw_1Pboard(next_1P, hold_1P, score1P, level1P, goal1P)
    draw_2Pboard(next_2P, hold_2P, score2P, level2P, goal2P)


def set_vol(val):
    volume = int(val) / 100 #set_volume argenment로 넣기 위해서(소수점을 만들어주기 위해서) 100으로 나눠줌
    print(volume)
    ui_variables.click_sound.set_volume(volume)

def set_music_playing_speed(CHANNELS, swidth, Change_RATE):
    spf = wave.open('assets/sounds/SFX_BattleMusic.wav', 'rb')
    RATE = spf.getframerate()
    signal = spf.readframes(-1)
    if os.path.isfile('assets/sounds/SFX_BattleMusic_Changed.wav'):
        pygame.mixer.quit()
        os.remove('assets/sounds/SFX_BattleMusic_Changed.wav')
        pygame.mixer.init()
    wf = wave.open('assets/sounds/SFX_BattleMusic_Changed.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE * Change_RATE)
    wf.writeframes(signal)
    wf.close()

    pygame.mixer.music.load('assets/sounds/SFX_BattleMusic_Changed.wav')
    pygame.mixer.music.play(-1) #위 노래를 반복재생하기 위해 play(-1)로 설정

def set_initial_values():
    global combo_count, combo_count_2P, score, level, goal, score_2P, level_2P, goal_2P, bottom_count, bottom_count_2P, hard_drop, hard_drop_2P, attack_point, attack_point_2P, dx, dy, dx_2P, dy_2P, rotation, rotation_2P, mino, mino_2P, next_mino1, next_mino2, next_mino1_2P, hold, hold_2P, hold_mino, hold_mino_2P, framerate, framerate_2P, matrix, matrix_2P, Change_RATE, blink, start, pause, done, game_over, leader_board, setting, volume_setting, screen_setting, pvp, help, gravity_mode, debug, d, e, b, u, g, time_attack, start_ticks, textsize, CHANNELS, swidth, name_location, name, previous_time, current_time, previous_time_2P, current_time_2P,pause_time, lines, leaders, volume, game_status, framerate_blockmove, framerate_2P_blockmove, game_speed, game_speed_2P
    framerate = 30 # Bigger -> Slower  기본 블록 하강 속도, 2도 할만 함, 0 또는 음수 이상이어야 함
    framerate_blockmove = framerate * 3 # 블록 이동 시 속도
    game_speed = framerate * 20 # 게임 기본 속도
    framerate_2P = 30 # 2P
    framerate_2P_blockmove = framerate_2P * 3 # 블록 이동 시 속도
    game_speed_2P = framerate_2P * 20 # 2P 게임 기본 속도

    # Initial values
    blink = False
    start = False
    pause = False
    done = False
    game_over = False
    leader_board = False
    setting = False
    volume_setting = False
    screen_setting = False
    pvp = False
    help = False
    gravity_mode = False #이 코드가 없으면 중력모드 게임을 했다가 Restart해서 일반모드로 갈때 중력모드로 게임이 진행됨#
    debug = True #False
    d = False
    e = False
    b = False
    u = False
    g = False
    time_attack = False
    start_ticks = pygame.time.get_ticks()
    textsize = False

    # 게임 음악 속도 조절 관련 변수
    CHANNELS = 1
    swidth = 2
    Change_RATE = 2

    combo_count = 0
    combo_count_2P = 0
    score = 0
    level = 1
    goal = level * 5
    score_2P = 0
    level_2P = 1
    goal_2P = level_2P * 5
    bottom_count = 0
    bottom_count_2P = 0
    hard_drop = False
    hard_drop_2P = False
    attack_point = 0
    attack_point_2P = 0

    dx, dy = 3, 0  # Minos location status
    dx_2P, dy_2P = 3, 0
    rotation = 0  # Minos rotation status
    rotation_2P = 0
    mino = randint(1, 7)  # Current mino #테트리스 블록 7가지 중 하나
    mino_2P = randint(1, 7)
    next_mino1 = randint(1, 7)  # Next mino1 # 다음 테트리스 블록 7가지 중 하나
    next_mino2 = randint(1, 7)  # Next mino2 # 다음 테트리스 블록 7가지 중 하나
    next_mino1_2P = randint(1, 7)
    hold = False  # Hold status
    hold_2P = False
    hold_mino = -1  # Holded mino #현재 hold하는 것 없는 상태
    hold_mino_2P = -1
    textsize = False

    name_location = 0
    name = [65, 65, 65]

    previous_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    previous_time_2P = pygame.time.get_ticks()
    current_time_2P = pygame.time.get_ticks()
    pause_time = pygame.time.get_ticks()

    with open('leaderboard.txt') as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]  #leaderboard.txt 한줄씩 읽어옴

    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
    for i in lines:
        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

    matrix = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix

    volume = 1.0 # 필요 없는 코드, effect_volume으로 대체 가능
    ui_variables.click_sound.set_volume(volume) # 필요 없는 코드, 전체 코드에서 click_sound를 effect_volume로 설정하는 코드 하나만 있으면 됨
    pygame.mixer.init()
    ui_variables.intro_sound.set_volume(music_volume / 10)
    ui_variables.break_sound.set_volume(effect_volume / 10) # 소리 설정 부분도 set_volume 함수에 넣으면 됨
    ui_variables.intro_sound.play()
    game_status = ''
    pygame.mixer.music.load("assets/sounds/SFX_BattleMusic.wav")


def matrix_changer(matrix):
    ai_matrix = []
    for j in range(len(matrix[0])):#20
        ai_matrix.append([])
        for i in range(len(matrix)): #10
            ai_matrix[j].append(matrix[i][j])
    del ai_matrix[0]
    return ai_matrix

def mino_converter(next,type): #블록 모양 변환 type==0: 현재 블록 반환 type=1:다음블록 반환
    if type==0:
        grid_n1 = tetrimino.mino_map[next - 1][0] #(배열이라-1) 현재 블록의 원래 모양
    elif type==1:
        grid_n1 = tetrimino.mino_map[next - 1][0] #(배열이라-1) 다음 블록의 원래 모양

    if grid_n1==tetrimino.mino_map[0][0] :
        return  [[0, 0, 0, 0], [6, 6, 6, 6]]
    if grid_n1==tetrimino.mino_map[1][0] :
        return [[4, 0, 0, 0], [4, 4, 4, 0]]
    if grid_n1==tetrimino.mino_map[2][0] :
        return [[0, 0, 5, 0], [5, 5, 5, 0]]
    if grid_n1==tetrimino.mino_map[3][0] :
        return [[0, 7, 7, 0], [0, 7, 7, 0]]
    if grid_n1==tetrimino.mino_map[4][0] :
        return [[0, 2, 2, 0], [2, 2, 0, 0]]
    if grid_n1==tetrimino.mino_map[5][0] :
        return [[0, 1, 0, 0], [1, 1, 1, 0]]
    if grid_n1==tetrimino.mino_map[6][0] :
        return [[3, 3, 0, 0], [0, 3, 3, 0]]
    
def stone_x(next):
    stone = tetrimino.mino_map[next-1][0] #(배열이라-1) 다음 블록의 원래 모양
    stone_x = int(10 / 2 - len(stone[0])/2)
    return stone_x
 
set_initial_values()
pygame.time.set_timer(pygame.USEREVENT, 10)

###########################################################
# Loop Start
###########################################################

while not done:

    # Pause screen
    # ui_variables.click_sound.set_volume(volume)

    if volume_setting:
        #배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색#
        pause_surface = screen.convert_alpha() #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0)) #위치 비율 고정

        #draw_image(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3), board_height)
        draw_image(screen, number_board, board_width * 0.45, board_height * 0.53, int(board_width * 0.09), int(board_height * 0.1444))
        draw_image(screen, number_board, board_width * 0.45, board_height * 0.73, int(board_width * 0.09), int(board_height * 0.1444))
        mute_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색#
        effect_plus_button.draw(screen, (0, 0, 0))
        effect_minus_button.draw(screen, (0, 0, 0))
        sound_plus_button.draw(screen, (0, 0, 0))
        sound_minus_button.draw(screen, (0, 0, 0))
        #음소거 추가#
        effect_sound_on_button.draw(screen,(0,0,0))
        music_sound_on_button.draw(screen,(0,0,0))
        back_button.draw(screen, (0, 0, 0))

        #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        music_volume_text = ui_variables.h5.render('Music Volume', 1, ui_variables.grey_1)
        effect_volume_text = ui_variables.h5.render('Effect Volume', 1, ui_variables.grey_1)
        screen.blit(music_volume_text, (board_width * 0.4, board_height * 0.4)) #위치 비율 고정
        screen.blit(effect_volume_text, (board_width * 0.4, board_height * 0.6)) #위치 비율 고정

        music_volume_text = ui_variables.h5.render('Music On/Off', 1, ui_variables.grey_1)
        effect_volume_text = ui_variables.h5.render('Effect On/Off', 1, ui_variables.grey_1)
        screen.blit(music_volume_text, (board_width * 0.6, board_height * 0.4)) #위치 비율 고정
        screen.blit(effect_volume_text, (board_width * 0.6, board_height * 0.6)) #위치 비율 고정

        music_volume_size_text = ui_variables.h4.render(str(music_volume), 1, ui_variables.grey_1)
        effect_volume_size_text = ui_variables.h4.render(str(effect_volume), 1, ui_variables.grey_1)
        screen.blit(music_volume_size_text, (board_width * 0.43, board_height * 0.5)) #위치 비율 고정
        screen.blit(effect_volume_size_text, (board_width * 0.43, board_height * 0.7)) #위치 비율 고정

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정

                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

                if effect_plus_button.isOver(pos):
                    effect_plus_button.image = clicked_plus_button_image
                else:
                    effect_plus_button.image = plus_button_image

                if effect_minus_button.isOver(pos):
                    effect_minus_button.image = clicked_minus_button_image
                else:
                    effect_minus_button.image = minus_button_image

                if sound_plus_button.isOver(pos):
                    sound_plus_button.image = clicked_plus_button_image
                else:
                    sound_plus_button.image = plus_button_image

                if sound_minus_button.isOver(pos):
                    sound_minus_button.image = clicked_minus_button_image
                else:
                    sound_minus_button.image = minus_button_image

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    volume_setting = False
                if sound_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume >= 10: #음량 최대크기
                        music_volume = 10
                    else:
                        music_sound_on_button.image=sound_on_button_image
                        music_volume += 1
                if sound_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume <= 0: #음량 최소크기
                        music_volume = 0
                        music_sound_on_button.image=sound_off_button_image
                    else:
                        if music_volume == 1:
                            music_sound_on_button.image=sound_off_button_image
                            music_volume -= 1
                        else:
                            music_sound_on_button.image=sound_on_button_image
                            music_volume -= 1
                if effect_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume >= 10: #음량 최대크기
                        effect_volume = 10
                    else:
                        effect_sound_on_button.image=sound_on_button_image
                        effect_volume += 1
                if effect_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume <= 0: #음량 최소크기
                        effect_volume = 0
                        effect_sound_on_button.image=sound_off_button_image
                    else:
                        if effect_volume == 1:
                            effect_sound_on_button.image=sound_off_button_image
                            effect_volume -= 1
                        else:
                            effect_sound_on_button.image=sound_on_button_image
                            effect_volume -= 1
                #음소거 추가#
                if music_sound_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume == 0 :
                        music_volume = 5 #중간 음량으로
                        music_sound_on_button.image=sound_on_button_image
                    else:
                        music_volume = 0
                        music_sound_off_button.draw(screen,(0,0,0)) #rgb(0,0,0) = 검정색
                        music_sound_on_button.image=sound_off_button_image
                if effect_sound_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume == 0 :
                        effect_volume = 5  #중간 음량으로
                        effect_sound_on_button.image=sound_on_button_image
                    else:
                        effect_volume = 0
                        effect_sound_off_button.draw(screen,(0,0,0))
                        effect_sound_on_button.image=sound_off_button_image
                if mute_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if (effect_volume == 0) and (music_volume == 0):
                        music_volume = 5  #중간 음량으로
                        effect_volume = 5  #중간 음량으로
                        mute_button.image=mute_button_image
                    else:
                        music_volume = 0 #최소 음량으로
                        effect_volume = 0 #최소 음량으로
                        default_button.draw(screen,(0,0,0))
                        mute_button.image=default_button_image

                set_volume()

    elif screen_setting:
        screen.fill(ui_variables.pinkpurple)
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        single_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        pvp_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        gravity_button.draw(screen,(0, 0, 0))
        timeattack_button.draw(screen,(0, 0, 0))
        setting_icon.draw(screen, (0, 0, 0))
        leaderboard_icon.draw(screen, (0, 0, 0))
        #배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))
        pause_surface = screen.convert_alpha() #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)

        screen.blit(pause_surface, (0, 0))

        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3), board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        smallsize_check_button.draw(screen, (0, 0, 0))
        bigsize_check_button.draw(screen, (0, 0, 0))
        midiumsize_check_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    screen_setting = False
                if smallsize_check_button.isOver(pos):
                    ui_variables.click_sound.play()
                    board_width = 800
                    board_height = 450
                    block_size = int(board_height * 0.045) #블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize=False

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
                    pygame.display.update()

                if midiumsize_check_button.isOver(pos):
                    ui_variables.click_sound.play()
                    board_width = 1200
                    board_height = 675
                    block_size = int(board_height * 0.045) #블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize=True

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

                    pygame.display.update()

                if bigsize_check_button.isOver(pos):
                    ui_variables.click_sound.play()
                    board_width = 1600
                    board_height = 900
                    block_size = int(board_height * 0.045) #블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize=True

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
                    pygame.display.update()

    elif setting:
        single_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        pvp_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        gravity_button.draw(screen,(0, 0, 0))
        timeattack_button.draw(screen,(0, 0, 0))
        setting_icon.draw(screen, (0, 0, 0))
        #배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))
        pause_surface = screen.convert_alpha() #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        if start:
            screen.fill(ui_variables.real_white)
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
            #배경 약간 어둡게
            leaderboard_icon.draw(screen, (0, 0, 0))
            pause_surface = screen.convert_alpha() #투명 가능하도록
            pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))
        if pvp:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
            #배경 약간 어둡게
            leaderboard_icon.draw(screen, (0, 0, 0))
            pause_surface = screen.convert_alpha() #투명 가능하도록
            pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3), board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        screen_icon.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        volume_icon.draw(screen, (0, 0, 0))

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

                if volume_icon.isOver(pos):
                    volume_icon.image = clicked_volume_vector
                else:
                    volume_icon.image = volume_vector

                if screen_icon.isOver(pos):
                    screen_icon.image = clicked_screen_vector
                else:
                    screen_icon.image = screen_vector

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = False

                if volume_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    volume_setting = True

                if screen_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    screen_setting = True

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045) #블록 크기 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif pause:
        pygame.mixer.music.pause()

        if start:
            screen.fill(ui_variables.real_white)
            draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
            #화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha() #투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  #투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)])  #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

        if pvp:
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
            #화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha() #투명 가능하도록
            pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)])  #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

        draw_image(screen, pause_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 0.7428), board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        resume_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        restart_button.draw(screen, (0, 0, 0))
        setting_button.draw(screen, (0, 0, 0))
        pause_quit_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.mixer.music.unpause()
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초

            elif event.type == pygame.MOUSEMOTION:
                if resume_button.isOver_2(pos):
                    resume_button.image = clicked_resume_button_image
                else:
                    resume_button.image = resume_button_image

                if restart_button.isOver_2(pos):
                    restart_button.image = clicked_restart_button_image
                else:
                    restart_button.image = restart_button_image

                if setting_button.isOver_2(pos):
                    setting_button.image = clicked_setting_button_image
                else:
                    setting_button.image = setting_button_image
                if pause_quit_button.isOver_2(pos):
                    pause_quit_button.image = clicked_quit_button_image
                else:
                    pause_quit_button.image = quit_button_image
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_quit_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True
                if setting_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if restart_button.isOver_2(pos):
                    ui_variables.click_sound.play()

                    pause = False
                    start = False

                    if pvp:
                        pvp = False

                if resume_button.isOver_2(pos):
                    pygame.mixer.music.unpause()
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif help:
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        single_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        pvp_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        gravity_button.draw(screen,(0, 0, 0))
        timeattack_button.draw(screen,(0, 0, 0))
        setting_icon.draw(screen, (0, 0, 0))
        leaderboard_icon.draw(screen, (0, 0, 0))
        #배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))
        pause_surface = screen.convert_alpha()  #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)])  #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        draw_image(screen, 'assets/vector/help_board.png', board_width * 0.5, board_height * 0.5, int(board_width * 0.8), int(board_height * 0.9)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, 'assets/vector/help_image.png', board_width * 0.5, board_height * 0.5, int(board_width * 0.7), int(board_height * 0.55)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image
                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    help = False

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045) #board 세로길이에 원하는 비율을 곱해줌
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    # Game screen
    elif leader_board:
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        single_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        pvp_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        gravity_button.draw(screen,(0, 0, 0))
        timeattack_button.draw(screen,(0, 0, 0))
        setting_icon.draw(screen, (0, 0, 0))
        leaderboard_icon.draw(screen, (0, 0, 0))
        #배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))
        pause_surface = screen.convert_alpha() #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)])  #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        draw_image(screen, leader_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3), #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                   board_height)

        back_button.draw(screen, (0, 0, 0))

        #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        leader_1 = ui_variables.h1_b.render('1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1, ui_variables.grey_1)
        leader_2 = ui_variables.h1_b.render('2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1, ui_variables.grey_1)
        leader_3 = ui_variables.h1_b.render('3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1, ui_variables.grey_1)
        screen.blit(leader_1, (board_width * 0.3, board_height * 0.15)) #위치 비율 고정
        screen.blit(leader_2, (board_width * 0.3, board_height * 0.35)) #위치 비율 고정
        screen.blit(leader_3, (board_width * 0.3, board_height * 0.55)) #위치 비율 고정

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image
                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    leader_board = False

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif start:
        if debug:
            level_plus_button.draw(screen, (0, 0, 0))
            level_minus_button.draw(screen, (0, 0, 0))
            combo_plus_button.draw(screen, (0, 0, 0))
            combo_minus_button.draw(screen, (0, 0, 0))
            speed_plus_button.draw(screen, (0, 0, 0))
            speed_minus_button.draw(screen, (0, 0, 0))
        if time_attack:
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과 시간 계산
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, game_speed)
                
                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                screen.fill(ui_variables.real_white)
                draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                pygame.display.update()

                current_time = pygame.time.get_ticks()
                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1


                # Create new mino: 중력 모드
                elif gravity_mode:
                    if hard_drop or bottom_count == waiting_time:
                        if gravity(dx, dy, mino, rotation, matrix):
                            erase_mino(dx, dy, mino, rotation, matrix)
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            ui_variables.GameOver_sound.play()
                            start = False
                            game_status = 'start'
                            game_over = True
                            gravity_mode = False
                            pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초
                    else:
                        bottom_count += 1

                # Create new mino: 일반 모드
                else:
                    if hard_drop or bottom_count == waiting_time:                        
                        computed += 1
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation, matrix)
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                      
                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            ui_variables.GameOver_sound.play()
                            start = False
                            game_status = 'start'
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초
                    else:
                        bottom_count += 1

                        
                if computed < 4: #h버튼 누르는 순간의 블록부터 자동으로 쌓아줘서 4미만으로 해야 5블록 쌓아줌
                    moves_list = []                                  
                    moves_list = Ai.choose(matrix_changer(matrix), mino_converter(mino,0), mino_converter(next_mino1,1), stone_x(mino), weights) 
                    for i in range(len(moves_list)):
                        if moves_list[i] == 'UP':
                            if rotation != 3:
                                rotation += 1
                            else:
                                rotation = 0                                                                    
                        elif moves_list[i] == 'LEFT': 
                            if not is_leftedge(dx, dy, mino, rotation, matrix):
                                ui_variables.move_sound.play()
                                dx -= 1                                               
                        elif moves_list[i ]== 'RIGHT':
                            if not is_rightedge(dx, dy, mino, rotation, matrix):
                                ui_variables.move_sound.play()
                                dx += 1
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    
                # Erase line
                erase_count = 0
                rainbow_count = 0
                matrix_contents = []
                combo_value = 0

                for j in range(board_y+1):
                    is_full = True
                    for i in range(board_x):
                        if matrix[i][j] == 0 or matrix[i][j] == 9 : #빈 공간이거나, 장애물블록
                            is_full = False
                    if is_full: # 한 줄 꽉 찼을 때
                        erase_count += 1
                        k = j
                        combo_value += 1
                        combo_count += 1 # 콤보 버그 수정. 가로줄 꽉 찼는지 확일할 때마다 combo count를 늘린다.
                        if combo_count % 3 == 0:
                            hint_item_num += 1
                        total_time += 5 # 콤보 시 시간 5초 연장. 여러줄 콤보시 1콤보당 5초가 늘어나도록 가로줄 꽉 찼는지 확일할 때마다 제한 시간을 늘린다.

                        #rainbow보너스 점수
                        rainbow = [1,2,3,4,5,6,7] #각 mino에 해당하는 숫자
                        for i in range(board_x):
                            matrix_contents.append(matrix[i][j]) #현재 클리어된 줄에 있는 mino 종류들 저장
                        rainbow_check = list(set(matrix_contents).intersection(rainbow)) #현재 클리어된 줄에 있는 mino와 mino의 종류중 겹치는 것 저장
                        if rainbow == rainbow_check: #현재 클리어된 줄에 모든 종류 mino 있다면
                            rainbow_count += 1

                        while k > 0:
                            for i in range(board_x):
                                matrix[i][k] = matrix[i][k - 1]  # 남아있는 블록 한 줄씩 내리기(덮어쓰기)
                            k -= 1
                if erase_count >= 1:
                    if rainbow_count >= 1:
                        score += 500 * rainbow_count #임의로 rainbow는 한 줄당 500점으로 잡음
                        rainbow_count = 0 #다시 초기화
                        screen.blit(ui_variables.rainbow_vector, (board_width * 0.28, board_height * 0.1)) #blit(이미지, 위치)
                        pygame.display.update()
                        pygame.time.delay(400) #0.4초

                    previous_time = current_time
                    
                    #점수 계산
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score += 50 * level * erase_count + combo_count
                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score += 150 * level * erase_count + 2 * combo_count
                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score += 350 * level * erase_count + 3 * combo_count
                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score += 1000 * level * erase_count + 4 * combo_count
                        screen.blit(ui_variables.combo_4ring, (250, 160)) #blit(이미지, 위치)

                    for i in range(1, 11):
                        if combo_count == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1], (board_width * 0.27, board_height * 0.35)) #각 콤보 이미지에 대해 blit(이미지, 위치)
                            pygame.display.update()
                            pygame.time.delay(500)
                        elif combo_count > 10:  # 11 이상 콤보 이미지
                            pygame.display.update()
                            pygame.time.delay(300)

                    for i in range(1, 9): # 1~8의 콤보 사운드
                        if combo_count == i + 2:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - 1].play()
                        if combo_count > 11:
                            ui_variables.combos_sound[8].play()
                if current_time - previous_time > 10000: #10초가 지나면
                    previous_time = current_time #현재 시간을 과거시간으로 하고
                    combo_count = 0 #콤보 수 초기화


                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    ui_variables.LevelUp_sound.play()
                    goal += level * 5
                    game_speed = int(game_speed-speed_change)
                    pygame.time.set_timer(pygame.USEREVENT, game_speed)
                    Change_RATE += 1
                    set_music_playing_speed(CHANNELS, swidth, Change_RATE)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    #pygame.time.set_timer(pygame.USEREVENT, game_speed)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                    pygame.display.update()
                elif event.key == K_j :
                    framerate = int(framerate-speed_change)
                    print(framerate)

                # Hold
                elif event.key == K_RSHIFT : #keyboard 변경하기
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                #dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
                # Turn right
                elif event.key == K_UP:
                    if is_turnable_r(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_m:
                    if is_turnable_l(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                
                # Set speed 기본값
                elif event.key == K_DOWN:
                    if not is_bottom(dx, dy, mino, rotation, matrix):
                        dy=dy+1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                    pygame.display.update()

                #자동 추천 기능 아이템 시작
                elif event.key == K_h:
                    if hint_item_num > 0:
                        computed = 0
                        hint_item_num -= 1

                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # rainbow test
                elif event.key == K_F1:
                    ui_variables.click_sound.play()
                    matrix[0][20] = 7 #빨
                    matrix[1][20] = 7 #빨
                    matrix[2][20] = 3#주
                    matrix[3][20] = 3#주
                    matrix[4][20] = 4#노
                    matrix[5][20] = 5#초
                    matrix[6][20] = 5#초
                    matrix[7][20] = 1#하
                    matrix[8][20] = 2#파
                    mino = 6
                # debug mode block change
                elif debug:
                    if event.key == K_1:
                        ui_variables.click_sound.play()
                        mino = 1 #빨
                    if event.key == K_2:
                        ui_variables.click_sound.play()
                        mino = 2 #빨
                    if event.key == K_3:
                        ui_variables.click_sound.play()
                        mino = 3 #빨
                    if event.key == K_4:
                        ui_variables.click_sound.play()
                        mino = 4 #빨
                    if event.key == K_5:
                        ui_variables.click_sound.play()
                        mino = 5 #빨
                    if event.key == K_6:
                        ui_variables.click_sound.play()
                        mino = 6 #빨
                    if event.key == K_7:
                        ui_variables.click_sound.play()
                        mino = 7 #빨

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

            elif event.type == pygame.MOUSEMOTION:
                if debug:
                    if level_plus_button.isOver(pos):
                        level_plus_button.image = clicked_plus_button_image
                    else:
                        level_plus_button.image = plus_button_image
                    if level_minus_button.isOver(pos):
                        level_minus_button.image = clicked_minus_button_image
                    else:
                        level_minus_button.image = minus_button_image
                    if combo_plus_button.isOver(pos):
                        combo_plus_button.image = clicked_plus_button_image
                    else:
                        combo_plus_button.image = plus_button_image
                    if combo_minus_button.isOver(pos):
                        combo_minus_button.image = clicked_minus_button_image
                    else:
                        combo_minus_button.image = minus_button_image
                    if speed_plus_button.isOver(pos):
                        speed_plus_button.image = clicked_plus_button_image
                    else:
                        speed_plus_button.image = plus_button_image
                    if speed_minus_button.isOver(pos):
                        speed_minus_button.image = clicked_minus_button_image
                    else:
                        speed_minus_button.image = minus_button_image

                    pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if debug:
                    if level_plus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if level < 15:
                            level += 1
                            goal += level * 5
                            Change_RATE = level + 1
                            set_music_playing_speed(CHANNELS, swidth, Change_RATE)
                    if level_minus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if level > 1:
                            level -= 1
                            goal += level * 5
                            Change_RATE = level + 1
                            set_music_playing_speed(CHANNELS, swidth, Change_RATE)
                    if combo_plus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        combo_count += 1
                    if combo_minus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if combo_count > 0:
                            combo_count -= 1
                    if speed_plus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if framerate <= 28:
                            framerate = int(framerate + speed_change)
                    if speed_minus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if framerate > 2:
                            framerate = int(framerate - speed_change)
                    pygame.display.update()

        if time_attack and total_time - elapsed_time < 0: #타임어택 모드이면서, 60초가 지났으면
            ui_variables.GameOver_sound.play()
            start = False
            game_status = 'start'
            game_over = True
            time_attack = False
            pygame.time.set_timer(pygame.USEREVENT, 1)

        pygame.display.update()
    elif pvp:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, game_speed)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                current_time = pygame.time.get_ticks()
                current_time_2P = pygame.time.get_ticks() # 2P 블록이 생성될 때 현재 시간 

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)
                    erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == waiting_time:
                        hard_drop = False
                        
                        bottom_count = 0
                        draw_mino(dx, dy, mino, rotation, matrix)

                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            # next_mino1 = next_mino2
                            next_mino1 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                            score += 10 * level
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            pvp = True
                            game_status = 'pvp'

                            if score >= score_2P :
                                draw_image(screen, gameover_image,board_width * 0.15, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.45)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                            else :
                                ui_variables.GameOver_sound.play()
                                draw_image(screen,pvp_lose_image,board_width * 0.15, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.6)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                draw_image(screen,pvp_win_image,board_width * 0.6, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.55)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                pvp = False
                                pygame.mixer.music.stop()
                                if game_status == 'start':
                                    start = True
                                    pygame.mixer.music.play(-1)
                                if game_status == 'pvp':
                                    pvp = True
                                    pygame.mixer.music.play(-1)
                                ui_variables.click_sound.play()
                                game_over = False
                                pause = False
                    else:
                        bottom_count += 1

                # Move mino down
                if not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                    dy_2P += 1

                # Create new mino
                else:
                    if hard_drop_2P or bottom_count_2P == waiting_time:
                        hard_drop_2P = False
                        bottom_count_2P = 0
                        draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                        if is_stackable(next_mino1_2P, matrix_2P):
                            mino_2P = next_mino1_2P
                            next_mino1_2P = randint(1, 7)
                            dx_2P, dy_2P = 3, 0
                            rotation_2P = 0
                            hold_2P = False
                            score_2P += 10 * level_2P
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            pvp = True
                            gagame_status = 'pvp'
                            if score <= score_2P :
                                draw_image(screen, gameover_image,board_width * 0.6, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.45)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                            else :
                                ui_variables.GameOver_sound.play()
                                draw_image(screen,pvp_win_image,board_width * 0.15, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.55)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                draw_image(screen,pvp_lose_image,board_width * 0.6, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.6)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                pvp = False
                                pygame.mixer.music.stop()
                                if game_status == 'start':
                                    start = True
                                    pygame.mixer.music.play(-1)
                                if game_status == 'pvp':
                                    pvp = True
                                    pygame.mixer.music.play(-1)
                                ui_variables.click_sound.play()
                                game_over = False
                                pause = False
                    else:
                        bottom_count_2P += 1

                # Erase line
                # 콤보 카운트
                erase_count = 0
                erase_count_2P = 0
                combo_value = 0
                combo_value_2P = 0
                attack_line = 0
                attack_line_2P = 0

                for j in range(board_y+1):
                    is_full = True
                    for i in range(board_x):
                        if matrix[i][j] == 0 or matrix[i][j] == 9: #빈 곳이거나 장애물 블록이 있는 경우
                            is_full = False #클리어 되지 못함
                    if is_full:
                        erase_count += 1
                        attack_line += 1
                        k = j
                        combo_value += 1
                        combo_count += 1  # 콤보 버그 수정. 가로줄 꽉 찼는지 확일할 때마다 1P의 combo count를 늘린다.
                        while k > 0: #y좌표가 matrix 안에 있는 동안
                            for i in range(board_x): #해당 줄의 x좌표들 모두
                                matrix[i][k] = matrix[i][k - 1] #한줄씩 밑으로 내림
                            k -= 1

                for j in range(board_y+1):
                    is_full = True
                    for i in range(board_x):
                        if matrix_2P[i][j] == 0 or matrix_2P[i][j] == 9: #빈 곳이거나 장애물 블록이 있는 경우
                            is_full = False #클리어 되지 못함
                    if is_full:
                        erase_count_2P += 1
                        attack_line_2P += 1
                        k = j
                        combo_value_2P += 1  
                        combo_count_2P += 1 # 콤보 버그 수정. 가로줄 꽉 찼는지 확일할 때마다 2P의 combo count를 늘린다.
                        while k > 0:  #y좌표가 matrix 안에 있는 동안
                            for i in range(board_x): #해당 줄의 x좌표들 모두
                                matrix_2P[i][k] = matrix_2P[i][k - 1] #한줄씩 밑으로 내림
                            k -= 1

                while attack_line >= 1 : #2p에게 공격 보내기
                    for i in range(board_x):
                        if matrix_2P[i][board_y-attack_point] == 0 : #비어있는 공간을
                            matrix_2P[i][board_y-attack_point] = 9 #모두 장애물 블록으로 채움
                    attack_line -= 1
                    attack_point += 1


                while attack_line_2P >= 1 :  #1p에게 공격 보내기
                    for i in range(board_x):
                        if matrix[i][board_y-attack_point_2P] == 0 : #비어있는 공간을
                            matrix[i][board_y-attack_point_2P] = 9 #모두 장애물 블록으로 채움
                    attack_line_2P -= 1
                    attack_point_2P += 1

                
                #1P
                if erase_count >= 1:
                    previous_time = current_time # 1P가 줄을 지우면 예전 시간을 현재 시간으로 바꾼다.
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score += 50 * level * erase_count + combo_count

                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score += 150 * level * erase_count + 2 * combo_count

                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score += 350 * level * erase_count + 3 * combo_count

                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score += 1000 * level * erase_count + 4 * combo_count

                        screen.blit(ui_variables.combo_4ring, (250, 160)) #blit(이미지, 위치)


                    for i in range(1, 11):
                        if combo_count == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1], (board_width * 0.07, board_height * 0.35)) # single combo image 코드에서 이미지의 x축 위치만 바꿈
                            pygame.display.update()
                            pygame.time.delay(500)
                        elif combo_count > 10:  # 11 이상 콤보 이미지
                            pygame.display.update()
                            pygame.time.delay(300)
    
                    
                    for i in range(1, 9): # 1~8의 콤보 사운드
                        if combo_count == i + 2:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - 1].play()
                        if combo_count > 11:
                            ui_variables.combos_sound[8].play()
                if current_time - previous_time > 10000: #10초가 지나면
                    previous_time = current_time #현재 시간을 과거시간으로 하고
                    combo_count = 0 #콤보 수 초기화

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    ui_variables.LevelUp_sound.play()
                    goal += level * 5
                    game_speed = int(game_speed - speed_change)
                if level > level_2P and Change_RATE < level + 1:
                    Change_RATE += 1
                    set_music_playing_speed(CHANNELS, swidth, Change_RATE)
                
                
                #2P
                if erase_count_2P >= 1:
                    previous_time_2P = current_time_2P # 2P가 줄을 지우면 예전 시간을 현재 시간으로 바꾼다.
                    if erase_count_2P == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score_2P += 50 * level_2P * erase_count_2P + combo_count_2P

                    elif erase_count_2P == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score_2P += 150 * level_2P * erase_count_2P + 2 * combo_count_2P

                    elif erase_count_2P == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score_2P += 350 * level_2P * erase_count_2P + 3 * combo_count_2P

                    elif erase_count_2P == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score_2P += 1000 * level_2P * erase_count_2P + 4 * combo_count_2P

                        screen.blit(ui_variables.combo_4ring, (250, 160)) #blit(이미지, 위치)

                    for i in range(1, 11):
                        if combo_count_2P == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1], (board_width * 0.55, board_height * 0.35)) # single combo image 코드에서 이미지의 x축 위치만 바꿈
                            pygame.display.update()
                            pygame.time.delay(500)
                        elif combo_count_2P > 10:  # 11 이상 콤보 이미지
                            pygame.display.update()
                            pygame.time.delay(300)

                    for i in range(1, 9): # 1~8의 콤보 사운드
                        if combo_count_2P == i + 2:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - 1].play()
                        if combo_count_2P > 11:
                            ui_variables.combos_sound[8].play()
                if current_time_2P - previous_time_2P > 10000: #10초가 지나면
                    previous_time_2P = current_time_2P #현재 시간을 과거시간으로 하고
                    combo_count_2P = 0 #콤보 수 초기화

                # Increase level
                goal_2P -= erase_count_2P
                if goal_2P < 1 and level_2P < 15:
                    level_2P += 1
                    ui_variables.LevelUp_sound.play()
                    goal_2P += level_2P * 5
                    game_speed_2P = int(game_speed_2P - speed_change)
                if level < level_2P and Change_RATE < level_2P + 1:
                    Change_RATE += 1
                    set_music_playing_speed(CHANNELS, swidth, Change_RATE)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True

                #dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
                # Hard drop
                elif event.key == K_e: #왼쪽창#
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    #pygame.time.set_timer(pygame.USEREVENT, game_speed)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                elif event.key == K_SPACE: #오른쪽창#
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        dy_2P += 1
                    hard_drop_2P = True
                    #pygame.time.set_timer(pygame.USEREVENT, game_speed_2P)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Hold
                elif event.key == K_LSHIFT:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                elif event.key == K_RSHIFT:
                    if hold_2P == False:
                        ui_variables.move_sound.play()
                        if hold_mino_2P == -1:
                            hold_mino_2P = mino_2P
                            mino_2P = next_mino1_2P
                            next_mino1_2P = randint(1, 7)
                        else:
                            hold_mino_2P, mino_2P = mino_2P, hold_mino_2P
                        dx_2P, dy_2P = 3, 0
                        rotation_2P = 0
                        hold_2P = True
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Turn right
                elif event.key == K_w: #왼쪽창#
                    if is_turnable_r(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                elif event.key == K_UP: #오른쪽창#
                    if is_turnable_r(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        rotation_2P += 1
                    # Kick
                    elif is_turnable_r(dx_2P, dy_2P - 1, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P + 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P - 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P, dy_2P - 2, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P + 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P - 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P += 1
                    if rotation_2P == 4:
                        rotation_2P = 0
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Turn left
                elif event.key == K_q:
                    if is_turnable_l(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation -= 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation -= 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation -= 1
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                elif event.key == K_m: #오른쪽창#
                    if is_turnable_l(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        rotation_2P -= 1
                    # Kick
                    elif is_turnable_l(dx_2P, dy_2P - 1, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P + 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P - 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P, dy_2P - 2, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P + 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P - 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P -= 1
                    if rotation_2P == -1:
                        rotation_2P = 3
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)  

                # Set speed pvp모드(1p)
                elif event.key == K_s:
                    if not is_bottom(dx, dy, mino, rotation, matrix):
                        dy=dy+1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                
                # Set speed pvp모드(2P)
                elif event.key == K_DOWN:
                    if not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):                        
                        dy_2P=dy_2P+1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                     
                # Move left
                elif event.key == K_a:  # key = pygame.key.get_pressed()
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_blockmove)
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                # Move right
                elif event.key == K_d:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_blockmove)
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P -= 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P += 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

        pygame.display.update()

    # Game over screen
    elif game_over:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.mixer.music.stop()
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초

                draw_image(screen, gameover_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 0.7428), board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                menu_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
                restart_button.draw(screen, (0, 0, 0))
                ok_button.draw(screen, (0, 0, 0))

                #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
                name_1 = ui_variables.h1_b.render(chr(name[0]), 1, ui_variables.pinkpurple)
                name_2 = ui_variables.h1_b.render(chr(name[1]), 1, ui_variables.pinkpurple)
                name_3 = ui_variables.h1_b.render(chr(name[2]), 1, ui_variables.pinkpurple)

                underbar_1 = ui_variables.h1_b.render("_", 1, ui_variables.pinkpurple)
                underbar_2 = ui_variables.h1_b.render("_", 1, ui_variables.pinkpurple)
                underbar_3 = ui_variables.h1_b.render("_", 1, ui_variables.pinkpurple)

                screen.blit(name_1, (int(board_width * 0.434), int(board_height * 0.55))) #blit(요소, 위치), 각각 전체 board의 가로길이, 세로길이에다가 원하는 비율을 곱해줌
                screen.blit(name_2, (int(board_width * 0.494), int(board_height * 0.55))) #blit(요소, 위치)
                screen.blit(name_3, (int(board_width * 0.545), int(board_height * 0.55))) #blit(요소, 위치)

                if blink:
                    blink = False
                else:
                    if name_location == 0:
                        screen.blit(underbar_1, ((int(board_width * 0.437), int(board_height * 0.56)))) #위치 비율 고정
                    elif name_location == 1:
                        screen.blit(underbar_2, ((int(board_width * 0.497), int(board_height * 0.56)))) #위치 비율 고정
                    elif name_location == 2:
                        screen.blit(underbar_3, ((int(board_width * 0.557), int(board_height * 0.56)))) #위치 비율 고정
                    blink = True

                pygame.display.update()

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()

                    #1p점수만 저장함
                    outfile = open('leaderboard.txt', 'a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()

                    game_over = False
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초

                #name은 3글자로 name_locationd은 0~2, name[name_location]은 영어 아스키코드로 65~90.
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초
                elif event.key == K_LEFT:
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_UP:
                    ui_variables.click_sound.play()
                    if name[name_location] != 90:
                        name[name_location] += 1
                    else:
                        name[name_location] = 65
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_DOWN:
                    ui_variables.click_sound.play()
                    if name[name_location] != 65:
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90
                    pygame.time.set_timer(pygame.USEREVENT, 1)

            elif event.type == pygame.MOUSEMOTION:
                if resume_button.isOver_2(pos):
                    menu_button.image = clicked_menu_button_image
                else:
                    menu_button.image = menu_button_image

                if restart_button.isOver_2(pos):
                    restart_button.image = clicked_restart_button_image
                else:
                    restart_button.image = restart_button_image

                if ok_button.isOver_2(pos):
                    ok_button.image = clicked_ok_button_image
                else:
                    ok_button.image = ok_button_image

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.isOver(pos):
                    ui_variables.click_sound.play()
                    #현재 1p점수만 저장함
                    outfile = open('leaderboard.txt', 'a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()
                    game_over = False
                    pygame.time.set_timer(pygame.USEREVENT, 1)

                if menu_button.isOver(pos):
                    ui_variables.click_sound.play()
                    game_over = False

                if restart_button.isOver_2(pos):
                    if game_status == 'start':
                        start = True
                        pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    if game_status == 'pvp':
                        pvp = True
                        pygame.mixer.music.play(-1)
                    if game_status == 'gravity_mode':
                        gravity_mode = True
                        pygame.mixer.music.play(-1)
                    if game_status == 'time_attack':
                        time_attack = True
                        pygame.mixer.music.play(-1)
                    ui_variables.click_sound.play()
                    game_over = False
                    pause = False

                if resume_button.isOver_2(pos):
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    # Start screen
    else:
        # 변수 선언 및 초기화
        if initalize:
            set_initial_values()
        initalize = False

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초

            elif event.type == KEYDOWN:
                # space로 start loop 진입하면 배경음악 안 들려서 주석 처리
                # if event.key == K_SPACE:
                #     ui_variables.click_sound.play()
                #     start = True

                #F1 버튼으로 중력모드 진입
                if event.key == K_F1:
                    ui_variables.click_sound.play()
                    if not gravity_mode:
                        gravity_mode = True
                    else:
                        gravity_mode = False

                #d, e, b, u, g 입력으로 디버그모드 진입
                if event.key == K_d:
                    if not d:
                        d = True
                    else:
                        d = False
                if event.key == K_e:
                    if not e:
                        e = True
                    else:
                        e = False
                if event.key == K_b:
                    if not b:
                        b = True
                    else:
                        b = False
                if event.key == K_u:
                    if not u:
                        u = True
                    else:
                        u = False
                if event.key == K_g:
                    if not g:
                        g = True
                    else:
                        g = False

                #t 입력으로 타임어택모드 진입
                if event.key == K_t:
                    if not time_attack:
                        ui_variables.click_sound.play()
                        time_attack = True # 이 상태로 start loop 들어가면 time_attack 모드 실행
                    else:
                        ui_variables.click_sound.play()
                        time_attack = False

            elif event.type == pygame.MOUSEMOTION:
                if single_button.isOver_2(pos):
                    single_button.image = clicked_single_button_image
                else:
                    single_button.image = single_button_image

                if pvp_button.isOver_2(pos):
                    pvp_button.image = clicked_pvp_button_image
                else:
                    pvp_button.image = pvp_button_image

                if help_button.isOver_2(pos):
                    help_button.image = clicked_help_button_image
                else:
                    help_button.image = help_button_image

                if quit_button.isOver_2(pos):
                    quit_button.image = clicked_quit_button_image
                else:
                    quit_button.image = quit_button_image

                if gravity_button.isOver_2(pos):
                    gravity_button.image = clicked_gravity_button_image
                else:
                    gravity_button.image = gravity_button_image

                if timeattack_button.isOver_2(pos):
                    timeattack_button.image = clicked_timeattack_button_image
                else:
                    timeattack_button.image = timeattack_button_image

                if setting_icon.isOver(pos):
                    setting_icon.image = clicked_setting_vector
                else:
                    setting_icon.image = setting_vector

                if leaderboard_icon.isOver(pos):
                    leaderboard_icon.image = clicked_leaderboard_vector
                else:
                    leaderboard_icon.image = leaderboard_vector
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if single_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    previous_time = pygame.time.get_ticks()
                    start = True
                    initalize = True
                    pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    ui_variables.intro_sound.stop()
                if pvp_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    pvp = True
                    initalize = True
                    pygame.mixer.music.play(-1)
                    ui_variables.intro_sound.stop()
                if gravity_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    start = True
                    gravity_mode = True
                    initalize = True
                    pygame.mixer.music.play(-1)
                    ui_variables.intro_sound.stop()
                if timeattack_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    start = True
                    time_attack = True
                    initalize = True
                    pygame.mixer.music.play(-1)
                    ui_variables.intro_sound.stop()
                if leaderboard_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    leader_board = True
                if setting_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if quit_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True
                if help_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    help = True

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045) #board 세로길이에 대해 원하는 비율로 곱해줌
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        single_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        pvp_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        gravity_button.draw(screen,(0, 0, 0))
        timeattack_button.draw(screen,(0, 0, 0))
        setting_icon.draw(screen, (0, 0, 0))
        leaderboard_icon.draw(screen, (0, 0, 0))

        if d == e == b == u == g == True:
            ui_variables.click_sound.play() # 디버그 상태에서는 Start Screen에서 계속 소리 남
            debug = True # 이 상태로 start loop 들어가면 debug 모드 실행
        else:
            debug = False

        if not start:
            pygame.display.update()

pygame.quit()

