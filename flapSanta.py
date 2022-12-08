import random
import sys
import time
import pygame
from pygame import mixer

# tạo hai sàn để khi lùi sàn sẽ k bị mất
def draw_floor():
    screen.blit(floor, (floor_x, 650))
    screen.blit(floor, (floor_x + 432, 650))


# tạo ống
def create_tube():
    # chọn chiều cao ngẫu nhiên cho ống
    random_tube_pos = random.choice(tube_height)  
    
    # ống dưới
    bot_tube = tube_screen.get_rect(midtop=(650, random_tube_pos)) 
    # ống trên 
    top_tube = tube_screen.get_rect(midtop=(650, random_tube_pos - 700))  
    if score > 3 and score < 10:
        # ống dưới
        bot_tube = tube_screen.get_rect(midtop=(650, random_tube_pos))  
        # ống trên
        top_tube = tube_screen.get_rect(midtop=(550, random_tube_pos - 650))  # ống trên
    return bot_tube, top_tube


# vẽ ống
def draw_tube(tubes):
    for tube in tubes:
        if tube.bottom >= 600:
            screen.blit(tube_screen, tube)
        else:
            # lật ống theo chiều Oy
            flip_tube = pygame.transform.flip(tube_screen, False, True)  
            screen.blit(flip_tube, tube)
            
# di chuyển ống sang bên trái trả lại một list mới
def move_tube(tubes):
    for tube in tubes:
        tube.centerx -= 5
    visible_tubes = [tube for tube in tubes if tube.right > -50]
    return visible_tubes



#  va chạm
def collision(tubes):
    global can_score
    for tube in tubes:
        if santa_rect.colliderect(tube):
            hit_sound.play()
            can_score = True
            game_over = pygame.image.load('Santa Claus Images/GameOver.png').convert_alpha()
            game_over_rectt = game_over.get_rect(center=(216, 384))
            screen.blit(game_over, game_over_rectt)
            return False

        if santa_rect.top <= -75 or santa_rect.bottom >= 650:
            hit_sound.play()

            can_score = True
            game_over = pygame.image.load('Santa Claus Images/GameOver.png').convert_alpha()
            game_over_rectt = game_over.get_rect(center=(216, 384))
            screen.blit(game_over, game_over_rectt)
            return False
    return True


def turning_santa(santa1):
    new_santa = pygame.transform.rotozoom(santa1, -santa_movement * 3, 1)
    return new_santa

# hieu ung cho santa
def santa_animation():
    new_santa = santa_list[santa_index]
    new_santa_rect = new_santa.get_rect(center=(100, santa_rect.centery))
    return new_santa, new_santa_rect

# so diem sau khi choi
def score_screen(state):
    
    if state == 'main game':
        score_screen = game_font.render(str(int(score)), True, WHITE)
        score_rect = score_screen.get_rect(center=(216, 100))
        screen.blit(score_screen, score_rect)
        
    if state == 'game over':
        score_screen = game_font.render(f'Score: {int(score)}', True, WHITE)
        score_rect = score_screen.get_rect(center=(216, 100))
        screen.blit(score_screen, score_rect)
        
        
        text_space = game_font.render(f'Press Space To Play', True, WHITE)
        text_rect =  text_space.get_rect(center=(216, 184))
        screen.blit(text_space, text_rect)
        
                
        high_score_screen = game_font.render(f'High Score: {int(high_score)}', True, WHITE)
        high_score_rect = high_score_screen.get_rect(center=(216, 630))
        screen.blit(high_score_screen, high_score_rect)
        

def player_score():
    global score, can_score
  
    if tube_list:
        for tube in tube_list:
            if 95 < tube.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False

            if tube.centerx < 0:
                can_score = True

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score



                
#nhấn p là pause               
def pause(stop):
    
    while stop: 
        my_font = pygame.font.Font('Santa Claus Sounds/ComicSansMS3.ttf', 90)
        text_surface = my_font.render("Paused", True, GRAY)
        rect = text_surface.get_rect(center=(216, 384))
        screen.blit(text_surface, rect)

        for event in pygame.event.get():
            pygame.display.update()
            # un pause the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    stop = False

def main() : 

    global image_icon,screen,clock,gravity,santa_movement, active,score,high_score,stop,WHITE,GRAY,can_score,day_night,day,night,start,play,countdown,background,floor,floor_x,santa_up,santa_down,santa_mid,santa_list,santa_index,santa,santa_rect,santa_flap,tube_screen,tube_list,spawn_tube,tube_height,game_over_screen,game_over_rect,flap_sound,hit_sound,score_sound,score_sound_c,score_event,game_font,flags,can_countdown
    
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
    countdown = False
    flags = False
    can_countdown = True
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
    #Background sound
    mixer.music.load('Santa Claus Sounds/sound/background.wav')
    mixer.music.set_volume(0.3)
    mixer.music.play(-1)
    
    flap_sound = pygame.mixer.Sound('Santa Claus Sounds/sound/sfx_wing.wav')
    flap_sound.set_volume(0.5)

    hit_sound = pygame.mixer.Sound('Santa Claus Sounds/sound/sfx_hit.wav')
    hit_sound.set_volume(0.5)

    score_sound = pygame.mixer.Sound('Santa Claus Sounds/sound/sfx_point.wav')
    score_sound.set_volume(0.5)

    score_sound_c = 100
    score_event = pygame.USEREVENT + 2
    pygame.time.set_timer(score_event, 100)


    # while loop của trò chơi
    while True:

        for event in pygame.event.get():

            # nhấn phím thoát khỏi game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # thoát hệ thống

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and active:
                    santa_movement = 0
                    santa_movement -= 6
                    flap_sound.play()
    
                if event.key == pygame.K_SPACE and active == False:
                    
                    active = True
                    countdown = True
                    tube_list.clear()
                    santa_rect.center = (100, 384)
                    santa_movement = 0
                    score = 0
                
                if event.key == pygame.K_p:
                    stop = True
                    pause(stop)
                            
            if event.type == spawn_tube:
                tube_list.extend(create_tube())
                
            if event.type == santa_flap:
                if santa_index < 2:
                    santa_index += 1
                else:
                    santa_index = 0
                santa, santa_rect = santa_animation()
            
                
                
                
        screen.blit(background, (0, 0))  # thêm background vào của sổ game
        if active:
            # santa
            santa_movement += gravity
            turningd_santa = turning_santa(santa)
            santa_rect.centery += santa_movement  # di chuyển xuống dưới
            screen.blit(turningd_santa, santa_rect)
            active = collision(tube_list)
            # ống
            tube_list = move_tube(tube_list)
            draw_tube(tube_list)
            player_score()
            score_screen('main game')
            if countdown :
                countdown = False
                for i in range(3):
                    my_font = pygame.font.Font("Santa Claus Sounds/ComicSansMS3.ttf", 30)
                    s = str(3-i)
                    text_surface = my_font.render(s, True, WHITE)
                    rect = text_surface.get_rect(center=(216, 384))
                    screen.blit(text_surface, rect)
                    pygame.display.flip()
                    time.sleep(0.5)
        else:

            screen.blit(game_over_screen, game_over_rect)
            high_score = update_score(score, high_score)
            score_screen('game over')
            
        # sàn
        floor_x -= 1  # di chuyển lùi lại phía bên trái
        draw_floor()  # vẽ ống lên màn hình

        if floor_x <= -432:
            floor_x = 0
        screen.blit(floor, (floor_x, 650))
        
        pygame.display.flip()
        clock.tick(90)

if __name__ == '__main__':
    main()
