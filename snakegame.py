import pygame #Video Game 2D
import random #Random Numbers
import os #Operating System

#Screen Size and FPS of the game
display_width = 900
display_height = 600
block_size = 30
FPS = 10


os.environ['SDL_VIDEO_CENTERED'] = '1' #Center 
pygame.init() #Initializing 
pygame.font.init() #Font
pygame.mixer.init() #Audioo
gameDisplay = pygame.display.set_mode((display_width, display_height)) #Window Display
pygame.display.set_caption('Snake Game') # Title of The Game
clock = pygame.time.Clock() #Timer


#Colors
bialy = (255,255,255) #White
czarny = (0,0,0) #Black
czerwony = (255,0,0) #Red
LIGHT_RED = (155,0,0) #Crimson

ciemnyZielony = (0,120,0) #Green

HEAD = pygame.image.load('head.png') 
TAIL = pygame.image.load('tail.png')
BODY = pygame.image.load('body.png')
TURNLEFT = pygame.image.load('TL.png')
TURNRIGHT = pygame.image.load('TR.png')

SUPERHEAD = pygame.image.load('head2.png')
SUPERTAIL = pygame.image.load('tail2.png')
SUPERBODY = pygame.image.load('body2.png')
SUPERTURNLEFT = pygame.image.load('TL2.png')
SUPERTURNRIGHT = pygame.image.load('TR2.png')

BACKGROUND = pygame.image.load('ground.jpg')
WALL = pygame.image.load('wall_frame.png')
FRUIT = pygame.image.load('fruit.png')
BIG_FRUIT = pygame.image.load('big_fruit.png')
BOMB = pygame.image.load('bomb.png')
BIG_BOMB= pygame.image.load('big_bomb.png')
START = pygame.image.load('Home.jpg')
CONTROLS = pygame.image.load('Ins.jpg')
GAMEOVER = pygame.image.load('GAMEOVER.png')
RED_DIAMOND = pygame.image.load('RED_DIAMOND.png')
WHITE_DIAMOND = pygame.image.load('WHITE_DIAMOND.png')
WHITE_DIAMOND_BIG = pygame.image.load('WHITE_DIAMOND_BIG.png')
BLACK_DIAMOND = pygame.image.load('BLACK_DIAMOND.png')
BLACK_DIAMOND_BIG = pygame.image.load('BLACK_DIAMOND_BIG.png')
TIMERBACKGROUND = pygame.image.load('TIMERBACKGROUND.png')

ACTIVE_B = pygame.image.load('ACTIVE.png')
INACTIVE_B = pygame.image.load('INACTIVE.png')

POINT = pygame.mixer.Sound("sfx_point.mp3")
BUTTON_PLAY = pygame.mixer.Sound("button_sfx.mp3")
HIT = pygame.mixer.Sound("sfx_hit.mp3")
EVOLUTION = pygame.mixer.Sound("March.mp3")
BOMBDESTROY = pygame.mixer.Sound("BOMBDESTROY.mp3")

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(40) #Volume of music

    
#Bombs
class bombs:
    
    def __init__(self): #init
        self.list = []

    def add(self, other): #add
    
        newBombX, newBombY = randLocationGen(self.list, other.list) #location
        newBomb = [newBombX, newBombY] #bomb
        self.list.append(newBomb) #append
        
    def show(self): #display

        for i in range(len(self.list)):
            gameDisplay.blit(BOMB, (self.list[i][0],self.list[i][1])) #render
            
    def destroy(self, bomb): #remove
         
        self.list.remove(bomb) #delete

#Fruit     
class fruit:
    
    def __init__(self, bombs, snake):
        self.renew(bombs, snake)
    
    def renew(self, bombs, snake):
        self.x, self.y = randLocationGen(bombs.list, snake.list) #renew
        
    def show(self):
        gameDisplay.blit(FRUIT, (self.x, self.y))

#Diamonds  
class diamond:
    
    def __init__(self):
        self.timer = 0 #reset
        self.x = None
        self.y = None
        
    def renew(self, bombs, snake, FPS):
        self.timer = 10*FPS
        self.x, self.y = randLocationGen(bombs.list, snake.list)
    
    def kill(self):
        self.timer = 0
        self.x = None
        self.y = None
        
    def show(self, color):
        if self.timer > 0: #countdown
            self.timer -= 1 #decrement
            if color == 'red':
                gameDisplay.blit(RED_DIAMOND, (self.x, self.y))
            elif color =='white':
                gameDisplay.blit(WHITE_DIAMOND, (self.x, self.y))
            elif color =='black':
                gameDisplay.blit(BLACK_DIAMOND, (self.x, self.y))
        else:
            self.kill() #terminate
            
#snake        
class snake:
    
    def __init__(self, lead_x, lead_y):
        self.direction = "right"
        
        self.list = [["right", lead_x-2*block_size, lead_y],
                     ["right", lead_x-block_size, lead_y],
                     ["right", lead_x, lead_y]]
                          
        self.head = ["right", lead_x, lead_y]
        self.length = 3
        self.superTimer = 0
        
    def superSnake(self, FPS):
        self.superTimer = 10*FPS
        
    def update(self, lead_x, lead_y):
        self.head = []
        self.head.append(self.direction)
            
        self.head.append(lead_x)
        self.head.append(lead_y)
        
        self.list.append(self.head)
        
        if len(self.list) > self.length:
            del self.list[0]

        if self.superTimer > 0:
            self.superTimer -= 1

    def show(self, FPS):
        
        if self.superTimer > 0:
            self.view(SUPERHEAD, SUPERTAIL, SUPERBODY, SUPERTURNLEFT, SUPERTURNRIGHT)
            
            gameDisplay.blit(TIMERBACKGROUND, (800, 529))
            font = pygame.font.Font('flup.ttf', 25)
            text = font.render(str(self.superTimer/FPS), True, czarny)
            gameDisplay.blit(text, [830,537])
            
        else:
            self.view(HEAD, TAIL, BODY, TURNLEFT, TURNRIGHT)
        

                
    def view(self, head, tail, body, turnleft, turnright):
        
        gameDisplay.blit(rotate(self.list[-1],head), (self.list[-1][1],self.list[-1][2]))       
        gameDisplay.blit(rotate(self.list[1],tail), (self.list[0][1],self.list[0][2]))
            
        for i in range(1, self.length-1):
            
            if self.list[i][0] == self.list[i+1][0]:
                gameDisplay.blit(rotate(self.list[i],body), (self.list[i][1],self.list[i][2]))
            
            elif (self.list[i][0] == "down" and self.list[i+1][0] == "right") or (self.list[i][0] == "right" and self.list[i+1][0] == "up") or (self.list[i][0] == "up" and self.list[i+1][0] == "left") or (self.list[i][0] == "left" and self.list[i+1][0] == "down"):       
                gameDisplay.blit(rotate(self.list[i+1],turnleft), (self.list[i][1],self.list[i][2]))
            
            elif (self.list[i][0] == "right" and self.list[i+1][0] == "down") or (self.list[i][0] == "down" and self.list[i+1][0] == "left") or (self.list[i][0] == "left" and self.list[i+1][0] == "up") or (self.list[i][0] == "up" and self.list[i+1][0] == "right"):        
                gameDisplay.blit(rotate(self.list[i+1],turnright), (self.list[i][1],self.list[i][2]))
        
    def isDead(self, other):
        
        for eachSegment in self.list[:-1]:
            if eachSegment[1] == self.head[1] and eachSegment[2] == self.head[2]:
                HIT.play()
                pygame.mixer.music.set_volume(0.2)
                return True
                
        if self.superTimer <= 0:
            
            for eachBomb in other.list:
                if eachBomb[0] == self.head[1] and eachBomb[1] == self.head[2]:
                    HIT.play()
                    return  True
                    
            if self.head[1] >= display_width-block_size or self.head[1] < block_size or self.head[2] >= display_height-block_size or self.head[2] < block_size:
                HIT.play()
                return True
                
        return False
        
    def trim(self):
        if len(self.list) > 13:
            self.list = self.list[10:]
            self.length -= 10

def rotate(segment, image):
    if segment[0] == "right":
        rotatedImage = pygame.transform.rotate(image, 0)
    elif segment[0] == "left":
        rotatedImage = pygame.transform.rotate(image, 180)
    elif segment[0] == "up":
        rotatedImage = pygame.transform.rotate(image, 90)    
    elif segment[0] == "down":
        rotatedImage = pygame.transform.rotate(image, 270)       
    return rotatedImage        
        
def draw_text(text, color, size, x, y):
    font = pygame.font.Font('flup.ttf', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)
    
def button(text, x, y, width, height, inactive, active, text_color=czarny, action=None):
    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if (x + width > cursor[0] > x and y + height > cursor[1] > y):
        gameDisplay.blit(ACTIVE_B, (x, y))
        
        if click[0] == 1 and action is not None:
            BUTTON_PLAY.play()  
            if action == 'play' or action == 'again':
                gameLoop()
            elif action == 'controls' or action == 'previous':
                show_controls()
            elif action == 'quit':
                pygame.quit()
                pygame.font.quit()
                quit()
            elif action == 'menu':
                show_game_intro()
            elif action == 'next':
                show_controls_next()
        
    else:
        gameDisplay.blit(INACTIVE_B, (x, y))
        
    draw_text(text, text_color, int(round(height / 2)), x + width / 2, y + height / 4)
        

     
def score(score):
    font = pygame.font.Font('flup.ttf', 55)
    text = font.render(str(score), True, czarny)
    gameDisplay.blit(text, [25,1])
    
def randLocationGen (bombsList, snakeList):
    randX = round((random.randrange(block_size, display_width - 2*block_size))/block_size)*block_size
    randY = round((random.randrange(block_size, display_height - 2*block_size))/block_size)*block_size
    

    for bomb in bombsList:
        for element in snakeList:
            if(randX == bomb[0] and randY == bomb[1]) or (randX == element[1] and randY == element[2]):
                print("!TEXT!" + str(randX)+str(element[1]) + str(randY)+str(element[2]))
                return randLocationGen(bombsList, snakeList)
    
    return randX, randY


def pause ():
    
    draw_text("PAUSE", czarny, 60, display_width/2, display_height/2 -130)
    draw_text("Press P to continue", czarny, 30, display_width/2, display_height/2)
    pygame.display.update()
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return
                    
def show_game_intro():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                quit()                
                    
        gameDisplay.blit(START, (0,0))

        button("PLAY", 350, 250, 200, 70, czerwony,100, action = 'play')
        button("CONTROLS", 350, 350, 200, 70, czerwony,100, action = 'controls')
        button("QUIT", 350, 450, 200, 70, czerwony,100, action = 'quit')
        
        pygame.display.update()
        
        clock.tick(15)
        
def show_controls():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                quit()
                
        gameDisplay.blit(CONTROLS, (0,0))
        
        draw_text("GREETINGS", czarny, 38, display_width/2, display_height/2 -220)
        draw_text("Use arrows to navigate your little friend on the board.", czarny, 28, display_width/2, display_height/2 -150)
        draw_text("Collect fruits       , to increase your score and grow.", czarny, 28, display_width/2, display_height/2 -100)
        draw_text("Be careful not to eat a bomb and sudenlly appearing", czarny, 28, display_width/2, display_height/2 -50)
        draw_text("bombs      and most importantly don't bite yourself!", czarny, 28, display_width/2, display_height/2 -0)
        draw_text("Use diamonds to unlock special powers.", czarny, 28, display_width/2, display_height/2 +50)
        
        gameDisplay.blit(BIG_FRUIT, (340, display_height/2 -135))
        gameDisplay.blit(BOMB, (290, display_height/2 -20))
        
        button("MENU", 50, 500, 200, 70, czerwony, LIGHT_RED, action = 'menu')
        button("NEXT", 350, 500, 200, 70, czerwony, LIGHT_RED, action = 'next')
        button("QUIT", 650, 500, 200, 70, czerwony, LIGHT_RED, action = 'quit')
        
        pygame.display.update()
        
        clock.tick(15)
        
def show_controls_next():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                quit()
              
        gameDisplay.blit(CONTROLS, (0,0))
        
        draw_text("     will allow you to go through the walls", czarny, 28, display_width/2, display_height/2 -220)
        draw_text("and crash those sneaky bombs.", czarny, 28, display_width/2, display_height/2 -170)
        draw_text("This effect will remain for 10 seconds.", czarny, 28, display_width/2, display_height/2 -120)
        draw_text("     will make snake shorter and easier to maneuver.", czarny, 28, display_width/2, display_height/2 -70)
        draw_text("Whenever you want,", czarny, 28, display_width/2, display_height/2 -20)
        draw_text("you can press P to pause the game."  , czarny, 28, display_width/2, display_height/2 +30)
        draw_text("GOOD LUCK!", czarny, 30, display_width/2, display_height/2 +80)
        
        gameDisplay.blit(BLACK_DIAMOND_BIG, (280, display_height/2 -225))
        gameDisplay.blit(WHITE_DIAMOND_BIG, (260, display_height/2 -75))        
        
        button("MENU", 50, 500, 200, 70, czerwony, LIGHT_RED, action = 'menu')
        button("PREVIOUS", 350, 500, 200, 70, czerwony, LIGHT_RED, action = 'previous')
        button("QUIT", 650, 500, 200, 70, czerwony, LIGHT_RED, action = 'quit')
        
        pygame.display.update()
        
        clock.tick(15)
                    
def gameLoop(): 
    
    gameExit = False
    gameOver = False
    
    points = 0
    speed = FPS

    lead_x = display_width/2 
    lead_y = display_height/2 
    lead_x_change = block_size 
    lead_y_change = 0 
    
    Snake = snake(lead_x, lead_y)
    Bombs = bombs()
    Fruit = fruit(Bombs, Snake)
    Diamond = diamond()
    Trimer = diamond()

    while not gameExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                gameExit = True
            
            
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT) and Snake.direction != "right":
                    Snake.direction = "left"
                elif (event.key == pygame.K_RIGHT) and Snake.direction != "left":
                    Snake.direction = "right"
                elif (event.key == pygame.K_UP) and Snake.direction != "down":
                    Snake.direction = "up"    
                elif (event.key == pygame.K_DOWN) and Snake.direction != "up":
                    Snake.direction = "down"

                if event.key == pygame.K_p:
                    pause()
                    
        if Snake.direction == "left":
            lead_x_change = -block_size
            lead_y_change = 0
        elif Snake.direction == "right":
            lead_x_change = block_size
            lead_y_change = 0
        elif Snake.direction == "up":
            lead_y_change = -block_size
            lead_x_change = 0
        elif Snake.direction == "down":
            lead_y_change = block_size
            lead_x_change = 0
            
        lead_x += lead_x_change
        lead_y += lead_y_change
                    
        if (lead_x == Fruit.x and lead_y == Fruit.y):
            
            Fruit.renew(Bombs, Snake)
            Snake.length += 1
            points += 10
            POINT.play()
            
            if (points)%40 == 0:
                Bombs.add(Snake)
                
            if (points)%70 == 0:
                speed += 1
                print(speed)
                
            if (points)%100 == 0:
                Diamond.renew(Bombs, Snake, speed)
                
            if (points)%300 == 0:
                Trimer.renew(Bombs, Snake, speed)
                
        if (lead_x == Diamond.x and lead_y == Diamond.y):
            
            points += 50
            Diamond.kill()
            Snake.superSnake(speed)
            EVOLUTION.play()
            
            if (points)%280 == 0:
                Trimer.renew(Bombs, Snake, speed)
            
        if (lead_x == Trimer.x and lead_y == Trimer.y):
            points += 50
            Trimer.kill()
            Snake.trim()
            
            if (points)%150 == 0:
                Diamond.renew(Bombs, Snake, speed)
            
        if Snake.superTimer > 0:
            if 15 <= Snake.superTimer:
                pygame.mixer.music.set_volume(0.05)
            if (15 > Snake.superTimer >= 10):
                pygame.mixer.music.set_volume(0.10)
            elif 10 > Snake.superTimer >= 5:
                pygame.mixer.music.set_volume(0.15)
            elif 5 > Snake.superTimer:
                pygame.mixer.music.set_volume(10)
            for bomb in Bombs.list:
                if bomb[0] == Snake.head[1] and bomb[1] == Snake.head[2]:
                    points += 20
                    Bombs.destroy(bomb)
                    BOMBDESTROY.play()
        
                
            if lead_x >= display_width-block_size:
                lead_x = block_size
            elif lead_x < block_size:
                lead_x = display_width-2*block_size
            elif lead_y >= display_height-block_size:
                lead_y = block_size
            elif lead_y < block_size:
                lead_y = display_height-2*block_size

        Snake.update(lead_x, lead_y)
        gameOver = Snake.isDead(Bombs)
                
        gameDisplay.blit(BACKGROUND, (0,0))  
        Fruit.show()
        Bombs.show()
        Diamond.show('black')
        Trimer.show('white')
        Snake.show(FPS)
        gameDisplay.blit(WALL, (0,0))
        score(points) 
           
        pygame.display.update()   
        clock.tick(speed)
        
        while gameOver == True:

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False 
                    if event.key == pygame.K_c:
                        gameLoop()
                        
            gameDisplay.blit(GAMEOVER, (10,10))
            draw_text("SCORE: " + str(points), czarny, 50, display_width/2,display_height/2-30)
                        
            button("MENU", 100, 450, 200, 70, czerwony, LIGHT_RED, action = 'menu')
            button("PLAY AGAIN", 350, 450, 200, 70, czerwony, LIGHT_RED, action = 'again')
            button("QUIT", 600, 450, 200, 70, czerwony, LIGHT_RED, action = 'quit')
        
            pygame.display.update()
        
            clock.tick(15)
            
    pygame.quit()
    pygame.font.quit()
    quit()

pygame.mixer.music.play(loops=-1)
show_game_intro()

