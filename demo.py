import pygame
import sys
import random
from pygame.locals import *
import os
import sys
import time
import json
import string

# set up environment variables so it can be displayed on PiTFT
#os.putenv('SDL_VIDEODRIVER', 'fbcon')
#os.putenv('SDL_FBDEV', '/dev/fb1')
# set up to enable touchscreen function
#os.putenv('SDL_MOUSEDRV', 'TSLIB')
#os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


def main():
    # start pygame
    pygame.init()
    # initialize global variables
    global win, score2, location2, usernamemode, username, score_list, json_file, speedLimit, movingLeftSpeed, screenSize, screen, height, width, FPS, life, score, count, press, startAgain, flags, countdown, BLACK, WHITE, bg1, bg2, bg3, bg4, location, mode1, mode2, instruction, history, playmode, singlePlayer, duelPlayer, daytime, nighttime, clock, SCREENWIDTH, SCREENHEIGHT, BASEY, IMAGES, SOUNDS

    # initialze each global varialbes
    win = 0  # which player win the game
    SCREENWIDTH = 320
    SCREENHEIGHT = 240
    BASEY = SCREENHEIGHT * 0.79
    IMAGES, SOUNDS = {}, {}
    username = ""
    clock = pygame.time.Clock()
    speedLimit = 4  # highest speed lime of shifting left
    movingLeftSpeed = 2  # initial shifting left speed
    screenSize = (320, 240)
    height = 32
    width = 28
    FPS = 64
    speed = 5  # bird falling speed
    location = (77, 120)  # first bird location
    location2 = (77, 100)  # second bird locationc
    score = 0  # score of the first player
    score2 = 0  # score of the second player
    life = 3  # how many lives the player have
    count = 15
    startPage = True
    mode1 = False
    mode2 = False
    history = False
    instruction = False
    playmode = False
    usernamemode = False
    singlePlayer = False
    duelPlayer = False
    daytime = False
    nighttime = False
    countdown = False
    press = True
    startAgain = False
    flags = False
    score_list = []

    # make the mouse invisible
    pygame.mouse.set_visible(True)
    # colors code for white and black
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    # set the size for the screen
    screen = pygame.display.set_mode(screenSize)
    # set the caption of the pygame
    pygame.display.set_caption('Flappy Bird')
    # load the images
    bg1 = pygame.image.load("front_page.jpg")
    bg2 = pygame.image.load("front_page2.jpg")
    bg3 = pygame.image.load("background.jpg")
    bg4 = pygame.image.load("background3.png")
    # load the background sound effect
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'
        SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die' + soundExt)
        SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit' + soundExt)
        SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point' + soundExt)
        SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
        SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing' + soundExt)

    while 1:
        time.sleep(0.01)
        # enter different pages
        if startPage:
            start_page()
        elif instruction:
            instruction_page()
        elif history:
            scoreboard_page()
        elif mode1:
            mode_player()
        elif usernamemode:
            mode_username()
            usernamemode = False
            mode2 = True
        elif mode2:
            mode_daynight()
        elif playmode:
            play_mode(score, life)
            # add countdown effect when game starts
            if countdown:
                countdown = False
                for i in range(3):
                    if i == 2:
                        flags = True
                    my_font = pygame.font.Font("ComicSansMS3.ttf", 30)
                    s = str(3-i)
                    text_surface = my_font.render(s, True, WHITE)
                    rect = text_surface.get_rect(center=(170, 110))
                    screen.blit(text_surface, rect)
                    pygame.display.flip()
                    time.sleep(1)
                    play_mode(score, life)

        for event in pygame.event.get():
            # when left click
            if (event.type is MOUSEBUTTONUP):
                # get the location when pressing the touchscreen
                pos = pygame.mouse.get_pos()
                x, y = pos
                # in start page
                if startPage:
                    if x < 160 and x > 10:
                        if y < 155 and y > 130:
                            # hit play button
                            startPage = False
                            mode1 = True
                        elif y < 180 and y > 155:
                            # hit score board button
                            startPage = False
                            history = True
                        elif y < 205 and y > 180:
                            # hit instruction button
                            startPage = False
                            instruction = True
                    # hit quit button
                    elif x < 310 and x > 250:
                        if y < 235 and y > 220:
                            pygame.quit()
                # in score board page
                elif history:
                    # hit back button
                    if x < 310 and x > 250:
                        if y < 235 and y > 220:
                            startPage = True
                            history = False
                # in instruction page
                elif instruction:
                    # hit back button
                    if x < 310 and x > 250:
                        if y < 235 and y > 220:
                            startPage = True
                            mode1 = False
                            instruction = False
                # in single/dual selection page
                elif mode1:
                    if x < 160 and x > 10:
                        # single player
                        if y < 120 and y > 95:
                            mode1 = False
                            mode2 = False
                            singlePlayer = True
                            usernamemode = True
                        # dual player mode
                        elif y < 145 and y > 120:
                            mode1 = False
                            mode2 = True
                            duelPlayer = True
                    elif x < 310 and x > 250:
                        # hit back button
                        if y < 235 and y > 220:
                            startPage = True
                            mode1 = False
                # in day/night selection page
                elif mode2:
                    if x < 160 and x > 10:
                        # daytime mode
                        if y < 120 and y > 95:
                            mode2 = False
                            playmode = True
                            daytime = True
                            cwn = True
                        # night mode
                        elif y < 145 and y > 120:
                            mode2 = False
                            playmode = True
                            nighttime = True
                            countdown = True
                    # hit back button
                    elif x < 310 and x > 250:
                        if y < 235 and y > 220:
                            mode1 = True
                            mode2 = False
                # in play page
                elif playmode:
                    # press the screen
                    press = True

# terminate the game


def terminate():
    pygame.quit()
    sys.exit()

# create pressed button effect


def button(x2, y2, width, height, active_color, action=None):
    cur = pygame.mouse.get_pos()
    if x2 + width > cur[0] > x2 and y2 + height > cur[1] > y2:
        # per-pixel alpha transparent
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        # notice the alpha value in the color
        s.fill((68, 219, 52, 128))
        screen.blit(s, (x2, y2))
    else:
        pass

# create start page


def start_page():
    screen.fill(BLACK)
    screen.blit(bg1, (0, 0))
    # add play button
    playbutton = pygame.image.load("play_button2.png")
    screen.blit(playbutton, (10, 130))
    # add pressed button effect 3 times
    button(10, 130, 150, 25, [68, 219, 52])   # play button
    button(10, 155, 150, 25, [68, 219, 52])   # score board button
    button(10, 180, 150, 25, [68, 219, 52])   # instruction button
    my_font = pygame.font.Font("ComicSansMS3.ttf", 18)
    text_surface = my_font.render("Play", True, BLACK)
    rect = text_surface.get_rect(center=(85, 142))
    screen.blit(text_surface, rect)
    my_font = pygame.font.Font("ComicSansMS3.ttf", 18)
    text_surface = my_font.render("Score Board", True, BLACK)
    rect = text_surface.get_rect(center=(85, 167))
    screen.blit(text_surface, rect)
    my_font = pygame.font.Font("ComicSansMS3.ttf", 18)
    text_surface = my_font.render("Instruction", True, BLACK)
    rect = text_surface.get_rect(center=(85, 192))
    screen.blit(text_surface, rect)
    button(250, 220, 60, 15, [68, 219, 52])   # back button
    my_font = pygame.font.Font("ComicSansMS3.ttf", 13)
    text_surface = my_font.render("Quit", True, BLACK)
    rect = text_surface.get_rect(center=(280, 227.5))
    screen.blit(text_surface, rect)
    pygame.display.flip()

# create score board page


def scoreboard_page():
    screen.fill(BLACK)
    screen.blit(bg3, (0, 0))
    button(250, 220, 60, 15, [68, 219, 52])   # back button
    my_font = pygame.font.Font("ComicSansMS3.ttf", 13)
    text_surface = my_font.render("Back", True, BLACK)
    rect = text_surface.get_rect(center=(280, 227.5))
    screen.blit(text_surface, rect)
    my_font = pygame.font.Font("ComicSansMS3.ttf", 15)
    text_surface = my_font.render("Ranking", True, BLACK)
    rect = text_surface.get_rect(center=(55, 15))
    screen.blit(text_surface, rect)
    text_surface = my_font.render("User Name", True, BLACK)
    rect = text_surface.get_rect(center=(155, 15))
    screen.blit(text_surface, rect)
    text_surface = my_font.render("Score", True, BLACK)
    rect = text_surface.get_rect(center=(255, 15))
    screen.blit(text_surface, rect)
    # create 10 numbers
    my_font = pygame.font.Font("ComicSansMS3.ttf", 13)
    for i in range(10):
        s = str(i+1)
        text_surface = my_font.render(s, True, BLACK)
        rect = text_surface.get_rect(center=(55, 35+i*20))
        screen.blit(text_surface, rect)
    # store the sorted json file content
    score_list = readRecord()
    for j in range(len(score_list)):
        # add user name to each ranking
        text_surface = my_font.render(score_list[j][1], True, BLACK)
        rect = text_surface.get_rect(center=(155, 35 + j*20))
        screen.blit(text_surface, rect)
        # add score to each ranking
        text_surface = my_font.render(str(score_list[j][0]), True, BLACK)
        rect = text_surface.get_rect(center=(255, 35 + j*20))
        screen.blit(text_surface, rect)
        pygame.display.flip()

# read backend json file


def readRecord():
    global json_file, name_list, score_list
    json_file = 'record.json'
    score_list = []
    # read json file
    with open(json_file, 'r') as infile:
        try:
            jsonlist = json.load(infile)
        except:
            jsonlist = []
        # store the json file content
        score_list = jsonlist['Record']
        return score_list
# sort function


def sortRecord(elem):
    return elem[0]

# write to the json file


def writeRecord(score):
    global json_file, name_list, score_list
    json_file = 'record.json'
    # open the json file
    with open(json_file, 'r') as infile:
        try:
            jsonlist = json.load(infile)
        except:
            jsonlist = []
        # add new netid-score pair to the json file
        jsonlist['Record'].append([score, username])
        # sort the json file
        jsonlist['Record'].sort(key=sortRecord, reverse=True)
        # delete useless data
        if len(jsonlist['Record']) > 10:
            del jsonlist['Record'][10]
    # write to json file
    with open(json_file, 'w') as outfile:
        json.dump(jsonlist, outfile)

# get keyboard value


def get_key():
    while True:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass

# display the user input to the screen

def display_box(message):
    screen.fill(BLACK)
    screen.blit(bg2, (0, 0))
    my_font = pygame.font.Font("ComicSansMS3.ttf", 15)
    # draw two rectangles as type in box
    pygame.draw.rect(screen, (0, 0, 0), (10, 110, 150, 25), 1)
    pygame.draw.rect(screen, (255, 255, 255), (8, 108, 154, 29), 1)
    # draw the user input as string to screen
    if len(message) != 0:
        screen.blit(my_font.render(message, True, BLACK), (10, 110))
    pygame.display.flip()

# manage the user input

def ask():
    current_string = []
    question = "NetID: "
    display_box(question + string.join(current_string, ""))
    while True:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            # delete last charactor
            current_string = current_string[0:-1]
        # hit enter button
        elif inkey == K_RETURN:
            break
        # get "_" symbol
        elif inkey == K_MINUS:
            current_string.append("_")
        # get charactors and numbers
        elif (inkey <= 122 and inkey >= 97) or (inkey <= 90 and inkey >= 65) or (inkey <= 57 and inkey >= 48):
            current_string.append(chr(inkey))
        display_box(question + string.join(current_string, ""))
    return string.join(current_string, "")

# get username

def mode_username():
    global username
    username = ask()

# instrction page


def instruction_page():
    screen.fill(BLACK)
    screen.blit(bg4, (0, 0))

    button(250, 220, 60, 15, [68, 219, 52])   # back button
    my_font = pygame.font.Font("ComicSansMS3.ttf", 13)
    text_surface = my_font.render("Back", True, BLACK)
    rect = text_surface.get_rect(center=(280, 227.5))
    screen.blit(text_surface, rect)

    my_font = pygame.font.Font("ComicSansMS3.ttf", 15)
    text_surface = my_font.render("How to play?", True, BLACK)
    rect = text_surface.get_rect(center=(155, 15))
    screen.blit(text_surface, rect)

    my_font = pygame.font.Font("ComicSansMS3.ttf", 12)
    text_surface = my_font.render("Single player", True, BLACK)
    rect = text_surface.get_rect(center=(50, 30))
    screen.blit(text_surface, rect)
    my_font = pygame.font.Font("ComicSansMS3.ttf", 12)
    text_surface = my_font.render("Double player", True, BLACK)
    rect = text_surface.get_rect(center=(52, 95))
    screen.blit(text_surface, rect)

    my_font = pygame.font.Font("ComicSansMS3.ttf", 11)
    text_surface = my_font.render("player", True, BLACK)
    rect = text_surface.get_rect(center=(62, 55))
    screen.blit(text_surface, rect)
    my_font = pygame.font.Font("ComicSansMS3.ttf", 11)
    text_surface = my_font.render("player 1", True, BLACK)
    rect = text_surface.get_rect(center=(65, 117))
    screen.blit(text_surface, rect)
    my_font = pygame.font.Font("ComicSansMS3.ttf", 11)
    text_surface = my_font.render("player 2", True, BLACK)
    rect = text_surface.get_rect(center=(65, 163))
    screen.blit(text_surface, rect)

    my_font = pygame.font.Font("ComicSansMS3.ttf", 11)
    text_surface = my_font.render("or", True, BLACK)
    rect = text_surface.get_rect(center=(117, 55))
    screen.blit(text_surface, rect)

    my_font = pygame.font.Font("ComicSansMS3.ttf", 11)
    text_surface = my_font.render("pause", True, BLACK)
    rect = text_surface.get_rect(center=(190, 55))
    screen.blit(text_surface, rect)
    my_font = pygame.font.Font("ComicSansMS3.ttf", 11)
    text_surface = my_font.render("pause", True, BLACK)
    rect = text_surface.get_rect(center=(190, 127))
    screen.blit(text_surface, rect)
    pygame.display.flip()

# single/dual player selection page


def mode_player():
    screen.fill(BLACK)
    screen.blit(bg2, (0, 0))
    # load the background
    playbutton = pygame.image.load("play_button.png")
    screen.blit(playbutton, (10, 95))
    button(10, 95, 150, 25, [68, 219, 52])   # single player button
    button(10, 120, 150, 25, [68, 219, 52])   # dual player button

    my_font = pygame.font.Font("ComicSansMS3.ttf", 15)
    text_surface = my_font.render("Single Player", True, BLACK)
    rect = text_surface.get_rect(center=(85, 107))
    screen.blit(text_surface, rect)
    text_surface = my_font.render("Duel Player", True, BLACK)
    rect = text_surface.get_rect(center=(85, 132))
    screen.blit(text_surface, rect)

    button(250, 220, 60, 15, [68, 219, 52])   # back button
    my_font = pygame.font.Font("ComicSansMS3.ttf", 13)
    text_surface = my_font.render("Back", True, BLACK)
    rect = text_surface.get_rect(center=(280, 227.5))
    screen.blit(text_surface, rect)
    pygame.display.flip()

# day/night selection page


def mode_daynight():
    screen.fill(BLACK)
    screen.blit(bg2, (0, 0))
    # load the background
    playbutton = pygame.image.load("play_button.png")
    screen.blit(playbutton, (10, 95))
    button(10, 95, 150, 25, [68, 219, 52])   # daytime mode
    button(10, 120, 150, 25, [68, 219, 52])   # night mode

    my_font = pygame.font.Font("ComicSansMS3.ttf", 18)
    text_surface = my_font.render("Daytime", True, BLACK)
    rect = text_surface.get_rect(center=(85, 107))
    screen.blit(text_surface, rect)
    my_font = pygame.font.Font("ComicSansMS3.ttf", 18)
    text_surface = my_font.render("Night", True, BLACK)
    rect = text_surface.get_rect(center=(85, 132))
    screen.blit(text_surface, rect)

    button(250, 220, 60, 15, [68, 219, 52])   # back button
    my_font = pygame.font.Font("ComicSansMS3.ttf", 13)
    text_surface = my_font.render("Back", True, BLACK)
    rect = text_surface.get_rect(center=(280, 227.5))
    screen.blit(text_surface, rect)
    pygame.display.flip()

# pause the game


def pause(stop):
    my_font = pygame.font.Font('ComicSansMS3.ttf', 90)
    text_surface = my_font.render("Paused", True, BLACK)
    rect = text_surface.get_rect(center=(150, 107))
    screen.blit(text_surface, rect)

    while stop:
        for event in pygame.event.get():
            # quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pygame.display.update()
            clock.tick(15)
            # un pause the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stop = False

# create ramdom pipe with fixed gap


def getRandomPipe(PIPEGAPSIZE):
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 15
    return [
        {'x': pipeX, 'y': gapY - pipeHeight},
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE},
    ]

# play page


def play_mode(score, life):
    # load different background in different mode
    if daytime:
        bg = pygame.image.load('background.jpg')
        if singlePlayer:
            bird = pygame.image.load("bird.png")
            bird2 = pygame.image.load("bird2.png")
            bird3 = pygame.image.load("bird3.png")
        elif duelPlayer:
            bird = pygame.image.load("bird.png")
            bird2 = pygame.image.load("bird2.png")
    elif nighttime:
        bg = pygame.image.load('background2.jpg')
        if singlePlayer:
            bird = pygame.image.load("bird2.png")
            bird2 = pygame.image.load("bird.png")
            bird3 = pygame.image.load("bird3.png")
        elif duelPlayer:
            bird = pygame.image.load("bird2.png")
            bird2 = pygame.image.load("bird.png")
    # initialize variables
    rectImg = bg.get_rect()
    bgY1 = 0
    bgX1 = 0
    bgY2 = 0
    bgX2 = rectImg.width
    win = 0
    live1 = True
    live2 = True
    location = (77, 120)
    location2 = (77, 100)
    count = 15
    press = True
    stop = False
    score = 0
    score2 = 0
    PIPEGAPSIZE = 80
    movingLeftSpeed = 2
    # add score display
    my_font = pygame.font.Font("ComicSansMS3.ttf", 13)
    text_surface1 = my_font.render("Score 1:", True, WHITE)
    rect1 = text_surface1.get_rect(center=(30, 15))
    my_font = pygame.font.Font("ComicSansMS3.ttf", 10)
    s = str(score)
    text_surface2 = my_font.render(s, True, WHITE)
    rect2 = text_surface2.get_rect(center=(60, 15))
    # add another score display
    if duelPlayer:
        my_font = pygame.font.Font("ComicSansMS3.ttf", 13)
        text_surface3 = my_font.render("Score 2:", True, WHITE)
        rect3 = text_surface3.get_rect(center=(30, 37.5))
        my_font = pygame.font.Font("ComicSansMS3.ttf", 10)
        s = str(score2)
        text_surface4 = my_font.render(s, True, WHITE)
        rect4 = text_surface4.get_rect(center=(60, 37.5))
        birdRect2 = bird2.get_rect(center=location2)
    # load heart image
    heart = pygame.image.load("heart.png")
    birdRect = bird.get_rect(center=location)
    centerx = screenSize[0] / 2
    centery = screenSize[1] / 2
    speed = 5
    # load pipe image in different mode
    if daytime:
        IMAGES['pipe'] = (
            pygame.transform.rotate(pygame.image.load(
                'pipe.png').convert_alpha(), 180),
            pygame.image.load('pipe.png').convert_alpha(),
        )
    if nighttime:
        IMAGES['pipe'] = (
            pygame.transform.rotate(pygame.image.load(
                'pipe2.png').convert_alpha(), 180),
            pygame.image.load('pipe2.png').convert_alpha(),
        )
    # create two pairs of random pipe with fixed gap size
    newPipe1 = getRandomPipe(PIPEGAPSIZE)
    newPipe2 = getRandomPipe(PIPEGAPSIZE)
    # set the locations of two upper pipes
    upperPipes = [
        {'x': SCREENWIDTH, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+160, 'y': newPipe2[0]['y']},
    ]
    # set locations of two lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+160, 'y': newPipe2[1]['y']},
    ]
    # initialize moving directions
    moveLeft, moveRight, moveUp, moveDown, Jump = False, False, False, False, False
    moveLeft2, moveRight2, moveUp2, moveDown2 = False, False, False, False
    # erase the screen and load the background
    screen.fill(BLACK)
    screen.blit(bg, rectImg)
    # load second score and bird for dual player mode
    if duelPlayer:
        screen.blit(text_surface3, rect3)
        screen.blit(text_surface4, rect4)
        screen.blit(bird2, birdRect2)
        # load score and bird for single player mode
    screen.blit(text_surface1, rect1)
    screen.blit(text_surface2, rect2)
    screen.blit(bird, birdRect)
    pygame.display.flip()

    if flags:
        while True:
            # set the delay
            clock.tick(FPS)
            # set the shifting left speed, upper boundary is 4
            if movingLeftSpeed < 4:
                movingLeftSpeed = movingLeftSpeed + 0.0001
            else:
                movingLeftSpeed = 4
            if PIPEGAPSIZE > 65:
                PIPEGAPSIZE -= 0.05
            else:
                PIPEGAPSIZE = 65
            for event in pygame.event.get():
                # when touch the screen, store this action
                if (event.type is MOUSEBUTTONDOWN) and singlePlayer:
                    Jump = True
                    press = False
                if (event.type is MOUSEBUTTONUP) and singlePlayer:
                    Jump = False
                    press = True
                # quit game
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    # quit the game
                    if event.key == pygame.K_ESCAPE:
                        terminate()
                    # move up the bird
                    if event.key == pygame.K_UP:
                        moveUp = True
                        moveDown = False
                    # move down the bird
                    if event.key == pygame.K_DOWN:
                        moveUp = False
                        moveDown = True
                    # move up the second bird
                    if event.key == pygame.K_w:
                        moveUp2 = True
                        moveDown2 = False
                    # move down the second bird
                    if event.key == pygame.K_s:
                        moveUp2 = False
                        moveDown2 = True
                    # pause the game
                    if event.key == pygame.K_SPACE:
                        stop = True
                        pause(stop)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        moveUp = False
                    if event.key == pygame.K_DOWN:
                        moveDown = False
                    if event.key == pygame.K_w:
                        moveUp2 = False
                    if event.key == pygame.K_s:
                        moveDown2 = False
            birdRect.left, birdRect.bottom = location
            if duelPlayer:
                birdRect2.left, birdRect2.bottom = location2
            # shift the background to left with increasing speed
            bgX1 -= movingLeftSpeed
            bgX2 -= movingLeftSpeed
            # if reach the left boundary, reset the background
            if bgX1 <= -rectImg.width:
                bgX1 = rectImg.width
            if bgX2 <= -rectImg.width:
                bgX2 = rectImg.width
            # move up the bird with fixed height, play the sound
            if moveUp and birdRect.top > 0:
                birdRect.centery -= speed
                SOUNDS['wing'].play()
            # move down the bird with fixed height
            if moveDown and birdRect.bottom < screenSize[1] - 1:
                birdRect.centery += 8
            # move up the bird with fixed height
            if moveUp2 and birdRect2.top > 0:
                birdRect2.centery -= speed
            # move down the bird with fixed height
            if moveDown2 and birdRect2.bottom < screenSize[1] - 1:
                birdRect2.centery += 8
            # move up the bird when touch the screen, play the sound
            if Jump and birdRect.top > 0:
                birdRect.centery -= 2.5
                SOUNDS['wing'].play()
            # if no action made, bird will fall with fixed speed
            if life != 0 and singlePlayer and not press:
                birdRect.bottom = birdRect.bottom + 1
                location = (birdRect.left, birdRect.bottom)
                startAgain = False
                press = True
            elif life != 0 and singlePlayer and press:
                startAgain = False
                if count != 0:
                    birdRect.bottom = birdRect.bottom + 1
                    location = (birdRect.left, birdRect.bottom)
                    count = count - 1
                else:
                    count = 15
                    press = False
            # if no action made, first bird will fall with fixed speed
            if live1 and duelPlayer:
                birdRect.bottom = birdRect.bottom + 1
                location = (birdRect.left, birdRect.bottom)
            # if no action made, second bird will fall with fixed speed
            if live2 and duelPlayer:
                birdRect2.bottom = birdRect2.bottom + 1
                location2 = (birdRect2.left, birdRect2.bottom)
            # if bird hit the ground, lose one life and start the game again
            if birdRect.bottom > 215 and singlePlayer and not startAgain:
                SOUNDS['hit'].play()
                life = life - 1
                startAgain = True
                birdRect.bottom = 120
                birdRect.left = 77
                location = (birdRect.left, birdRect.bottom)
                upperPipes = {}
                lowerPipes = {}
                # generate two random pairs of pipes again
                newPipe1 = getRandomPipe(PIPEGAPSIZE)
                newPipe2 = getRandomPipe(PIPEGAPSIZE)
                upperPipes = [{'x': SCREENWIDTH, 'y': newPipe1[0]['y']},
                              {'x': SCREENWIDTH+160, 'y': newPipe2[0]['y']}, ]

                lowerPipes = [{'x': SCREENWIDTH, 'y': newPipe1[1]['y']},
                              {'x': SCREENWIDTH+160, 'y': newPipe2[1]['y']}, ]
                time.sleep(2)
            # if the first bird hit the ground, remove the first bird from the screen
            if birdRect.bottom > 215 and duelPlayer:
                SOUNDS['hit'].play()
                live1 = False
                birdRect.bottom = -20
                birdRect.left = -20
                location = (birdRect.left, birdRect.bottom)
                if win == 0:
                    win = 2
            # if the second bird hit the ground, remove the first bird from the screen
            if birdRect.bottom > 215 and duelPlayer:
                SOUNDS['hit'].play()
                live2 = False
                birdRect2.bottom = -20
                birdRect2.left = -20
                location2 = (birdRect2.left, birdRect2.bottom)
                if win == 0:
                    win = 1
            screen.blit(bg, (bgX1, bgY1))
            screen.blit(bg, (bgX2, bgY2))
            # shift the pipes to the left with increasing speed
            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                uPipe['x'] -= movingLeftSpeed
                lPipe['x'] -= movingLeftSpeed
            if len(upperPipes) != 0:
                # if one pipe is shifted to the left boundary of the scrren, add a new pipe
                if 0 < upperPipes[0]['x'] < movingLeftSpeed:
                    newPipe = getRandomPipe(PIPEGAPSIZE)
                    upperPipes.append(newPipe[0])
                    lowerPipes.append(newPipe[1])
                    # increment life for two player if alive
                    if live1:
                        score += 1
                    if live2:
                        score2 += 1
                    SOUNDS['point'].play()
                # remove one pair of pipe when gets to the left boundary
                if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
                    upperPipes.pop(0)
                    lowerPipes.pop(0)
            # get the pipe height and width
            pipeW = IMAGES['pipe'][0].get_width()
            pipeH = IMAGES['pipe'][0].get_height()
            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                # get the rects of two birds
                birdRect = bird.get_rect(center=location)
                birdRect2 = bird2.get_rect(center=location2)
                # get the rects of one pair of pipes
                uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
                lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)
                screen.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                screen.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))
                # bird rect hit pipr rect, lose one life, start the game again
                if singlePlayer and (uPipeRect.colliderect(birdRect) or lPipeRect.colliderect(birdRect)):
                    SOUNDS['hit'].play()
                    life = life - 1
                    startAgain = True
                    birdRect.bottom = 120
                    birdRect.left = 77
                    location = (birdRect.left, birdRect.bottom)
                    upperPipes = {}
                    lowerPipes = {}
                    newPipe1 = getRandomPipe(PIPEGAPSIZE)
                    newPipe2 = getRandomPipe(PIPEGAPSIZE)
                    upperPipes = [{'x': SCREENWIDTH, 'y': newPipe1[0]['y']},
                                  {'x': SCREENWIDTH+160, 'y': newPipe2[0]['y']}, ]

                    lowerPipes = [{'x': SCREENWIDTH, 'y': newPipe1[1]['y']},
                                  {'x': SCREENWIDTH+160, 'y': newPipe2[1]['y']}, ]
                    time.sleep(2)
                    break
                # if first bird hit the pipe, remove the first bird
                if duelPlayer and live1 and (uPipeRect.colliderect(birdRect) or lPipeRect.colliderect(birdRect)):
                    SOUNDS['hit'].play()
                    live1 = False
                    birdRect.bottom = -20
                    birdRect.left = -20
                    location = (birdRect.left, birdRect.bottom)
                    if win == 0:
                        win = 2
                # if second bird hit the pipe, remove the second bird
                if duelPlayer and live2 and (uPipeRect.colliderect(birdRect2) or lPipeRect.colliderect(birdRect2)):
                    SOUNDS['hit'].play()
                    live2 = False
                    birdRect2.bottom = -20
                    birdRect2.left = -20
                    location2 = (birdRect2.left, birdRect2.bottom)
                    if win == 0:
                        win = 1
            pygame.display.update()
            # update the score for first player
            s = str(score)
            text_surface2 = my_font.render(s, True, WHITE)
            rect2 = text_surface2.get_rect(center=(60, 15))
            if duelPlayer:
                # update the score for second player
                s = str(score2)
                text_surface4 = my_font.render(s, True, WHITE)
                rect4 = text_surface4.get_rect(center=(60, 37.5))
                screen.blit(text_surface3, rect3)
                screen.blit(text_surface4, rect4)
            screen.blit(text_surface1, rect1)
            screen.blit(text_surface2, rect2)
            # create heart image
            if singlePlayer:
                for i in range(life):
                    heartRect = heart.get_rect(center=(17.5+20*i, 37.5))
                    screen.blit(heart, heartRect)
                # change the bird image when score is greater or equal to 10
                if score < 10:
                    screen.blit(bird, birdRect)
                elif score >= 10:
                    screen.blit(bird3, birdRect)
            if duelPlayer:
                screen.blit(bird, birdRect)
                screen.blit(bird2, birdRect2)
            pygame.display.flip()
            # if no life left, game over and return to start page. write the netid-score pair to json
            if life == 0:
                SOUNDS['die'].play()
                my_font = pygame.font.Font("ComicSansMS3.ttf", 30)
                text_surface = my_font.render("Game Over", True, WHITE)
                rect = text_surface.get_rect(center=(170, 110))
                screen.blit(text_surface, rect)
                pygame.display.flip()
                startAgain = False
                location = (77, 120)
                time.sleep(4)
                life = 3
                writeRecord(score)
                main()
            if duelPlayer:
                # if both birds die, print which player wins
                if live1 == False and live2 == False:
                    if win == 1:
                        my_font = pygame.font.Font("ComicSansMS3.ttf", 30)
                        text_surface = my_font.render(
                            "Player 1 wins", True, WHITE)
                        rect = text_surface.get_rect(center=(170, 110))
                        screen.blit(text_surface, rect)
                    if win == 2:
                        my_font = pygame.font.Font("ComicSansMS3.ttf", 30)
                        text_surface = my_font.render(
                            "Player 2 wins", True, WHITE)
                        rect = text_surface.get_rect(center=(170, 110))
                        screen.blit(text_surface, rect)
                    pygame.display.flip()
                    time.sleep(4)
                    main()


if __name__ == '__main__':
    main()
