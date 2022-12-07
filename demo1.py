import random
import sys
import time

import pygame
def main():
    global image_icon,screen,clock,gravity,santa_movement, active,score,high_score,stop,WHITE,GRAY,can_score,day_night,day,night,start,play,countdown,background,floor,floor_x,santa_up,santa_down,santa_mid,santa_list,santa_index,santa,santa_rect,santa_flap,tube_screen,tube_list,spawn_tube,tube_height,game_over_screen,game_over_rect,flap_sound,hit_sound,score_sound,score_sound_c,score_event,game_font,flags
    
    pygame.init()
    pygame.display.set_caption('Flapp Santa')
    image_icon = pygame.image.load('Santa Claus Images/santa_icon.PNG')
    pygame.display.set_icon(image_icon)
    screen = pygame.display.set_mode((432, 768))
    clock = pygame.time.Clock()
    game_font = pygame.font.Font('Santa Claus Sounds/04B_19.TTF', 35)

    # tạo các biến cho trò chơi
    gravity = 0.2
    santa_movement = 0
    active = True
    score = 0
    high_score = 0
    can_score = True
    stop =False
    WHITE = (255,255,255)
    GRAY = (150,150,150)
    day_night = False

    #dark mode
    day = False
    night = False
    start = True
    play = False
    countdown = False
    flags = False
    # chèn background
    # convert đổi file hình ảnh thành file nhẹ hơn để pygame load nhanh hơn
    background = pygame.image.load('Santa Claus Images/dark.PNG').convert()



    # chèn sàn
    floor = pygame.image.load('Santa Claus Images/Floor.png').convert()
    floor = pygame.transform.scale2x(floor)
    floor_x = 0

    # tạo santa

    santa_down = pygame.image.load('Santa Claus Images/santa_icon.PNG').convert_alpha()
    santa_mid = pygame.image.load('Santa Claus Images/santa_icon_1.PNG').convert_alpha()
    santa_up = pygame.image.load('Santa Claus Images/santa_icon.PNG').convert_alpha()

    santa_list = [santa_down, santa_mid, santa_up]
    santa_index = 0
    santa = santa_list[santa_index]
    santa_rect = santa.get_rect(center=(100, 384))

    # tạo timer cho santa
    santa_flap = pygame.USEREVENT + 1
    pygame.time.set_timer(santa_flap, 216)

    # tạo cột
    tube_screen = pygame.image.load('Santa Claus Images/tube.PNG').convert()
    tube_screen = pygame.transform.scale2x(tube_screen)
    tube_list = []

    # tạo timer
    spawn_tube = pygame.USEREVENT
    pygame.time.set_timer(spawn_tube, 1700)
    tube_height = [500, 300, 400]

    # tọa màn  hình kết thúc
    game_over_screen = pygame.image.load('Santa Claus Images/Untitled_Artwork 2.png').convert_alpha()
    game_over_rect = game_over_screen.get_rect(center=(216, 384))
    screen.blit(game_over_screen, game_over_rect)

    # chèn âm thanh
    flap_sound = pygame.mixer.Sound('Santa Claus Sounds/sound/sfx_wing.wav')
    flap_sound.set_volume(0.5)

    hit_sound = pygame.mixer.Sound('Santa Claus Sounds/sound/sfx_hit.wav')
    hit_sound.set_volume(0.5)

    score_sound = pygame.mixer.Sound('Santa Claus Sounds/sound/sfx_point.wav')
    score_sound.set_volume(0.5)

    score_sound_c = 100
    score_event = pygame.USEREVENT + 2
    pygame.time.set_timer(score_event, 100)
    
    
    
if __name__ == '__main__':
    main()