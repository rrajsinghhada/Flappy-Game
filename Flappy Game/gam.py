import random #for generating the random pipes
import sys  #We will use sys.exit to exit the game
import pygame
from pygame.locals import* #Basic pygame imports



#global variable for the game

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY =  int(SCREENHEIGHT *0.8)
GAME_SPIRIT = {}
GAME_SOUNDS = {}
BACKGROUND = 'Gallary/sprites/background.png'
PLAYER = 'Gallary/sprites/bird.png'
PIPE = 'Gallary/sprites/pipe.png'

#reading file high_score to extract the high_score 

refl = open('high_score.txt')
High_score = ''
for al in refl.read():
    if al.isnumeric():
        High_score += al
High_score = int(High_score)
refl.close()
def welcomeScreen():
    """
    shows welcome image on the screen
    """

    
    messagex = int((SCREENWIDTH - GAME_SPIRIT['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.26)
    basex = int(0)

    while True:
        for event in pygame.event.get():
            # if user clicks on cross button , close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #if the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPIRIT['background'],(0,0))
                SCREEN.blit(GAME_SPIRIT['message'],(messagex,messagey))
                # SCREEN.blit(pygame.image.load('/Users/rishirajsinghhada/Downloads/images (1).jpg'),(playerx,playery))
                # SCREEN.blit(GAME_SPIRIT['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPIRIT['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def maingame():
    score = 0
    PLAYERx = int(SCREENWIDTH/5) 
    PLAYERy = int(SCREENHEIGHT/2)
    basex = 0
    global lvl
    # create two pipe for the game
    newpipe1 = getRandomPipe(score)
    newpipe2 = getRandomPipe(score)

    #my list of upper pipes
    upperpipes = [
        {'x':SCREENWIDTH+200,'y':newpipe1[0]['y']},
        {'x':SCREENWIDTH+200+SCREENWIDTH/2,'y':newpipe2[1]['y']},
    ]
    #my list of lower pipes
    lowerpipes = [
        {'x':SCREENWIDTH+200,'y':newpipe1[0]['y']},
        {'x':SCREENWIDTH+200+SCREENWIDTH/2,'y':newpipe2[1]['y']},
    ]
    
    pipevelx = -4
    
    playervely = -9
    playermaxvely = 10
    # playerMinVelY = -8
    playerAccY = 1
    # last = 0

    PlayerFlapAccv = -8#velocity while flapping
    playerFlapped = False # it is true when the bird is flapping

    while True:
        # Icreasing the speed after the score reaches 50
        # if score == 50 and last != score:
        #     pipevelx -= 1
        #     last = score

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.exit()
                sys.exit()
            if event.type == pygame.KEYDOWN and(event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                if PLAYERy > 0:
                    playervely = PlayerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['WINGS'].play()

        crashTest = isCollide(PLAYERx,PLAYERy,upperpipes,lowerpipes)#this true returns true if the funcrion is crashed

        if crashTest:
            global High_score
            if High_score< score:
                refl =  open('high_score.txt','w')
                refl.write('High_score = '+str(score))
                refl.close()
                High_score = score
            return score

        
        #check score
        PlayerMidPos = PLAYERx + GAME_SPIRIT['player'].get_width()/2
        for pipe in upperpipes:

            pipeMidPos = pipe['x'] +int((GAME_SPIRIT['pipe'][0]).get_width()/2)
            if pipeMidPos <= PlayerMidPos < pipeMidPos+4:
                score += 1

                GAME_SOUNDS['POINT'].play() 
        
        if playervely < playermaxvely and not playerFlapped:
            playervely +=playerAccY

        if playerFlapped:
            playerFlapped = False 
        playerheight = GAME_SPIRIT['player'].get_height()
        PLAYERy = PLAYERy + min(playervely, GROUNDY-PLAYERy-playerheight)

        #MOVE PIPES TO THE LEFT
        for upperpipe ,lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x'] += pipevelx
            lowerpipe['x'] += pipevelx

        #add a new pipe when the first is about to go to leftmost part of the screen
        if 0<upperpipes[0]['x']<5:
            newpipe = getRandomPipe(score)
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])



        # if the pipe is out of the screen remove it
        if upperpipes[0]['x'] < -GAME_SPIRIT['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        # lets built our spirites now
        SCREEN.blit(GAME_SPIRIT['background'],(0,0))
        for upperpipe ,lowerpipe in zip(upperpipes,lowerpipes):
            SCREEN.blit(GAME_SPIRIT['pipe'][0],(upperpipe['x'],upperpipe['y']))
            SCREEN.blit(GAME_SPIRIT['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
            
        SCREEN.blit(GAME_SPIRIT['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPIRIT['player'],(PLAYERx,PLAYERy))
        MyDigit = [int(x) for x in list(str(score))]
        width = 0
        for digit in MyDigit:
            width += GAME_SPIRIT['numbers'][digit].get_width()
        xoffset = int((SCREENWIDTH - width)/2)



        for digit in MyDigit:
            SCREEN.blit(GAME_SPIRIT['numbers'][digit],(xoffset,int(SCREENHEIGHT*0.12)))
            xoffset += GAME_SPIRIT['numbers'][digit].get_width()
            pygame.display.update()
        FPSCLOCK.tick(FPS)
 
def isCollide(PLAYERx,PLAYERy,upperpipes,lowerpipes):
    if PLAYERy>GROUNDY - 25 or PLAYERy < 0:
        GAME_SOUNDS['DIE'].play()
        return True
    for pipe in upperpipes:
        if pipe['y'] <=0:
            pipeheight = GAME_SPIRIT['pipe'][0].get_height()
            if (PLAYERy + 10 < pipeheight + pipe['y'] and (abs(PLAYERx - pipe['x'])+20 < GAME_SPIRIT['pipe'][0].get_width())):
                GAME_SOUNDS['DIE'].play()
                return True
    for pipe1 in lowerpipes:
        
        if pipe1['y'] > 0:
            if(((PLAYERy + GAME_SPIRIT['player'].get_height()) > pipe1['y']+10) and (abs(PLAYERx - pipe1['x'])+20 < GAME_SPIRIT['pipe'][1].get_width())):
                GAME_SOUNDS['DIE'].play()
                return True

    return False
  


def getRandomPipe(score):
    '''
    generate positions of two pipe(one bottom one straight)
    '''

    
    pipeHeight = GAME_SPIRIT['pipe'][0].get_height()
    offset = SCREENHEIGHT/3 - score%30
    y2 = offset+random.randrange(0,int(SCREENHEIGHT - GAME_SPIRIT['base'].get_height() -1.2*offset))
    pipex = SCREENWIDTH + 10 
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x':pipex, 'y': -y1},
        {'x':pipex,'y': y2}
    ]
    return pipe


def final_score(sc):
    while True:
        pygame.display.update()
        # blue = (50, 50, 150)
        yellow = (238,255,65)
        white = (255, 255, 255)
        font = pygame.font.Font('freesansbold.ttf', 14)
        text = font.render(str(sc), True, white)
        tex = font.render(str(High_score), True, yellow)
        textRect = text.get_rect()
        textRec = tex.get_rect()
        textRect.center = (289 // 2, 511 // 2 - 50)
        textRec.center = (289 // 2, 511 // 2 - 80)
        SCREEN.blit(GAME_SPIRIT['background'],(0,0))
        SCREEN.blit(GAME_SPIRIT['base'],(0,GROUNDY))
        SCREEN.blit(GAME_SPIRIT['game_over'],(int(-205),int(1)))
        SCREEN.blit(text, textRect)
        SCREEN.blit(tex, textRec)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and event.key == K_RETURN:
                return

if __name__ == '__main__':
    #this will be the main point where the game will start
    pygame.init()#Initialise pygame modules
    ico = pygame.image.load('bir.png')
    pygame.display.set_icon(ico)

    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Rishiraj Singh')
    GAME_SPIRIT['numbers'] = (
        pygame.image.load('Gallary/sprites/iloveimg-resized/0.png').convert_alpha(),
        pygame.image.load('Gallary/sprites/iloveimg-resized/1.png').convert_alpha(),
        pygame.image.load('Gallary/sprites/iloveimg-resized/2.png').convert_alpha(),
        pygame.image.load('Gallary/sprites/iloveimg-resized/3.png').convert_alpha(),
        pygame.image.load('Gallary/sprites/iloveimg-resized/4.png').convert_alpha(),
        pygame.image.load('Gallary/sprites/iloveimg-resized/5.png').convert_alpha(),
        pygame.image.load('Gallary/sprites/iloveimg-resized/6.png').convert_alpha(),
        pygame.image.load('Gallary/sprites/iloveimg-resized/7.png').convert_alpha(),
        pygame.image.load('Gallary/sprites/iloveimg-resized/8.png').convert_alpha(),
        pygame.image.load('Gallary/sprites/iloveimg-resized/9.png').convert_alpha(),
    )

    GAME_SPIRIT['message'] = pygame.image.load('Gallary/sprites/download (2).png').convert_alpha()
    GAME_SPIRIT['base'] = pygame.image.load('Gallary/sprites/ground.png').convert_alpha()
    GAME_SPIRIT['FINAL'] = pygame.image.load('Gallary/sprites/d.png').convert_alpha()
    GAME_SPIRIT['game_over'] = pygame.image.load('Gallary/sprites/Untitled_presentation-removebg-preview.png').convert_alpha()
    GAME_SPIRIT['pipe'] = (
        pygame.transform.rotate(pygame.image.load('Gallary/sprites/pipe.png').convert_alpha(),180),
        pygame.image.load('Gallary/sprites/pipe.png').convert_alpha(),
    )

    # game sounds
    GAME_SOUNDS['DIE'] = pygame.mixer.Sound('Gallary/audio/mixkit-arcade-fast-game-over-233.wav')
    # GAME_SOUNDS['HIT'] = pygame.mixer.music.load('Gallary/audio/hit-sound-effect-12445.mp3')
    GAME_SOUNDS['POINT'] = pygame.mixer.Sound('Gallary/audio/mixkit-unlock-game-notification-253.wav')
    GAME_SOUNDS['WINGS'] = pygame.mixer.Sound('Gallary/audio/mixkit-quick-jump-arcade-game-239.wav')
    # GAME_SOUNDS['SWOOSH'] = pygame.mixer.music.load('Gallary/audio/whoosh-6316.mp3')
    # GAME_SOUNDS['WINGS'] = pygame.mixer.music.load('/Users/rishirajsinghhada/Downloads/python harry/python code/Flappy Bird/Gallary/audio/wingflap_fast-7139.mp3')

    GAME_SPIRIT['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPIRIT['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()  ##shows welcome screen untill the user presses a button
        score = maingame()#this is the main game function
        final_score(score)
 
 