import pygame
import cv2
import random
import time
import os

FPS = 20
run = True
ALL_WIDTH = 1920
ALL_HEIGHT =1080
screen = pygame.display.set_mode((ALL_WIDTH,ALL_HEIGHT))
r = 50
if not os.path.isdir('saved_videos/'):
    os.makedirs('saved_videos/')
pygame.init()
pygame.display.set_caption('nnControl4080')
LOGO_img = pygame.image.load(os.path.join("img", "CIRCLE.png")).convert()
LOGO_mini_img = pygame.transform.scale(LOGO_img, (25, 19))
LOGO_mini_img.set_colorkey((0,0,0))
pygame.display.set_icon(LOGO_mini_img)
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
clock = pygame.time.Clock()

def video_recorder(i,X=0,Y=0):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    if i == "all":
        video_writer = cv2.VideoWriter("saved_videos/output_"+str(i)+".avi", fourcc, FPS, size, True)
    else:
        video_writer = cv2.VideoWriter("saved_videos/output_"+str(i)+"_pos(x,y)=("+X+","+Y+").avi", fourcc, FPS, size, True)
    print("start recording new videos " +str(i) +"(" +str(X) + str(Y))
    return video_writer


# create objects


class letter_L(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load('img/letter_L.PNG').convert_alpha()
        self.radius = r
        self.image = pygame.transform.scale(self.raw_image, (self.radius-10, self.radius-10))
        self.rect = self.image.get_rect()
        self.rect.x = -500
        self.rect.y = -500
        self.showuptime = 0
        self.showornot = 0
    def showup(self,X,Y):
        self.image = pygame.transform.scale(self.raw_image, (self.radius-10, self.radius-10))
        self.rect.x = X+10
        self.rect.y = Y+10
        self.showuptime = self.showuptime + 1 
        pygame.display.update()
    def vanish(self):
        self.showuptime = 0
        self.image = pygame.transform.scale(self.raw_image, (0, 0))
        self.rect.x = -500
        self.rect.y = -500
        pygame.display.update()

class letter_R(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load('img/letter_R.PNG').convert_alpha()
        self.radius = r
        self.image = pygame.transform.scale(self.raw_image, (self.radius-10, self.radius-10))
        self.rect = self.image.get_rect()
        self.rect.x = -500
        self.rect.y = -500
        self.showuptime = 0
        self.showornot = 0
    def showup(self,X,Y):
        self.image = pygame.transform.scale(self.raw_image, (self.radius-10, self.radius-10))
        self.rect.x = X+10
        self.rect.y = Y+10
        self.showuptime = self.showuptime + 1 
        pygame.display.update()
    def vanish(self):
        self.showuptime = 0
        self.image = pygame.transform.scale(self.raw_image, (0, 0))
        self.rect.x = -300
        self.rect.y = -300
        pygame.display.update()

class BlackDot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load('img/CIRCLE.PNG').convert_alpha()
        self.radius = r  # 50 pixels
        # reshape
        self.image = pygame.transform.scale(self.raw_image, (self.radius, self.radius))
        #set position
        self.rect = self.image.get_rect()
        self.rect.x = -300
        self.rect.y = -300
        self.zoomornot = 0
        self.boundaryornot = 0
        self.zoomtime = 0
    def showup(self,X,Y):
        
        self.image = pygame.transform.scale(self.raw_image, (self.radius, self.radius))
        self.rect.x = self.rect.x + X + 300
        self.rect.y = self.rect.y + Y + 300
        print("showup!",X,Y)
        pygame.display.update()

class Dot(pygame.sprite.Sprite):
    def __init__(self,X,Y):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load('img/CIRCLE.PNG').convert_alpha()
        self.radius = r  # 50 pixels
        # reshape
        self.image = pygame.transform.scale(self.raw_image, (self.radius, self.radius))
        #set position
        self.rect = self.image.get_rect()
        self.rect.x = X
        self.rect.y = Y
        self.zoomornot = 0
        self.boundaryornot = 0
        self.zoomtime = 0
    def zoomin(self):
            self.radius = self.radius + 2
            self.rect.x = self.rect.x - 1
            self.rect.y = self.rect.y - 1
            self.image = pygame.transform.scale(self.raw_image, (self.radius, self.radius))
            if self.radius == 100:
                self.boundaryornot = 1
    def zoomout(self):
            self.radius = self.radius - 2
            self.rect.x = self.rect.x + 1
            self.rect.y = self.rect.y + 1
            self.image = pygame.transform.scale(self.raw_image, (self.radius, self.radius))
            #print(self.radius)
            if self.radius == 50:
                self.boundaryornot = 0
                self.zoomtime = self.zoomtime+1
    def changepos(self, X, Y):
        self.rect.x = X
        self.rect.y = Y
        pygame.display.update()


def draw_init():
    font_name = pygame.font.match_font('arial') 
    font = pygame.font.Font(font_name, 100)
    text_surface = font.render("right click to start",True,(255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = 800
    text_rect.y = 500
    screen.blit(text_surface,text_rect)
# add object to sprite

all_sprite = pygame.sprite.Group()

dot_x = random.randint(100,ALL_WIDTH -100 )
dot_y = random.randint(100,ALL_HEIGHT - 100)
dot = Dot(dot_x, dot_y)
black_dot = BlackDot()
all_sprite.add(dot)
all_sprite.add(black_dot)
L = letter_L()
R = letter_R()
all_sprite.add(L)  
all_sprite.add(R)    


start_record = 1

'''
for dd in all_sprite:
    print(dd)
    if dd == 'Dot Sprite(in 1 groups)':
        print("yes")
'''

Draw_init = True
one_point_flag = 0 # control only one point can blink
one_point_LR = 0 # control either L or R can show up
mouse_flag = 0 # when switch to 1, read the input of mouse
ii = 0
start_record = 0
TEST_TIME = 5

# body
# VW = video_recorder(ii)
if Draw_init == True:
        draw_init()
        pygame.display.update()
        while Draw_init:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    Draw_init = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()
                    if mouse_buttons[2]:
                            print("right mouse button")
                            Draw_init = False
                            screen = pygame.display.set_mode((ALL_WIDTH,ALL_HEIGHT))
                            break

if run:
    VW_all = video_recorder("all")

while run and not Draw_init:

    
    clock.tick(FPS)

    ret, frame = capture.read()
    pygame.display.update()
    # cv2.imshow('Video Stream', frame)
    VW_all.write(frame)
    if start_record == 1:
        VW.write(frame)
    black_dot.showup(-300,-300)
    all_sprite.draw(screen)
    pygame.display.update()
    if one_point_LR == 0:
        random_LR = random.randint(0,1)
        one_point_LR =1

    dot.zoomornot = 1
    if dot.zoomtime == 1:
        if start_record == 0:
            x_cm = (dot_x-840+25) / 32.1285
            y_cm = (0-dot_y-25) / 32.1285            
            VW = video_recorder(str(ii),str(round(x_cm,2)),str(round(y_cm,2)))
            start_record = 1
            VW.write(frame)

    if dot.zoomornot == 1 and dot.boundaryornot == 0 and dot.zoomtime != 3 :
        dot.zoomin()
    elif dot.zoomornot == 1 and dot.boundaryornot == 1 and dot.zoomtime != 3:
        dot.zoomout()
    
    elif dot.zoomtime == 3:
        if random_LR == 0:
            L.showup(dot_x, dot_y)
            print("show_L")
        elif random_LR == 1:
            R.showup(dot_x, dot_y)
            print("show_R")
        dot.zoomornot = 0
        dot.boundaryornot = 0
        dot.zoomtime = 0
        one_point_flag = 0
    
    if R.showuptime <= 2 and R.showuptime > 0 :
        R.showup(dot_x, dot_y)
        print("showing...")
    
    elif R.showuptime == 3:
        screen = pygame.display.set_mode((ALL_WIDTH,ALL_HEIGHT))
        R.vanish()
        black_dot.showup(dot_x,dot_y)
        all_sprite.draw(screen)
        # os.system("pause")
        one_point_LR = 0
        mouse_flag = 1



    if L.showuptime <= 2 and L.showuptime > 0 :
        L.showup(dot_x, dot_y)
        print("showing...")

    elif L.showuptime == 3:
        screen = pygame.display.set_mode((ALL_WIDTH,ALL_HEIGHT))
        L.vanish()
        black_dot.showup(dot_x,dot_y)
        all_sprite.draw(screen)
        # os.system("pause")
        one_point_LR = 0
        mouse_flag = 1

    if mouse_flag == 1:
        screen = pygame.display.set_mode((ALL_WIDTH,ALL_HEIGHT))
        L.vanish()
        R.vanish()
        black_dot.showup(dot_x,dot_y)
        dot.changepos(-300,-300)
        all_sprite.draw(screen)
        pygame.display.update()
        mouse_flag += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    
    end = time.time()
    while mouse_flag == 2:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_buttons = pygame.mouse.get_pressed()
                button_msg = ""
                if mouse_buttons[0]:
                    button_msg = "left mouse button"
                elif mouse_buttons[2]:
                    button_msg = "right mouse button"
            
                if button_msg == "":
                    print("no button pressed")

                elif random_LR == 0 and button_msg == "left mouse button":
                    need_time = str(time.time() - end ) 
                    print("correct!")
                    mouse_flag = 0
                    print(need_time)
                    start_record = 0
                    VW.release()
                    print("realease")
                    dot_x = random.randint(100,ALL_WIDTH -100)
                    dot_y = random.randint(100,ALL_HEIGHT -100)
                    dot.changepos(dot_x,dot_y)
                    pygame.display.update()
                    # os.system("pause")
                    screen = pygame.display.set_mode((ALL_WIDTH,ALL_HEIGHT))
                    ii = ii+1
                    black_dot.showup(-300,-300)
                    if float(need_time) > 1.0:
                        TEST_TIME  = TEST_TIME + 1

                elif random_LR == 1 and button_msg == "right mouse button":
                    print("correct!")
                    mouse_flag = 0
                    need_time = str(time.time() - end ) 
                    print(need_time)
                    start_record = 0
                    VW.release()
                    print("realease")
                    dot_x = random.randint(100,ALL_WIDTH -100)
                    dot_y = random.randint(100,ALL_HEIGHT -100)
                    dot.changepos(dot_x,dot_y)
                    screen = pygame.display.set_mode((ALL_WIDTH,ALL_HEIGHT))
                    ii = ii+1
                    black_dot.showup(-300,-300)
                    pygame.display.update()
                    # os.system("pause")
                    if float(need_time) > 1.0:
                        TEST_TIME  = TEST_TIME + 1

                elif random_LR == 1 and button_msg == "left mouse button":
                    mouse_flag = 0
                    start_record = 0
                    VW.release()
                    dot_x = random.randint(100,ALL_WIDTH -100)
                    dot_y = random.randint(100,ALL_HEIGHT -100)
                    dot.changepos(dot_x,dot_y)
                    screen = pygame.display.set_mode((ALL_WIDTH,ALL_HEIGHT))
                    black_dot.showup(-300,-300)
                    ii = ii+1
                    TEST_TIME  = TEST_TIME + 1

                elif random_LR == 0 and button_msg == "right mouse button":
                    mouse_flag = 0
                    start_record = 0
                    VW.release()
                    dot_x = random.randint(100,ALL_WIDTH -100)
                    dot_y = random.randint(100,ALL_HEIGHT -100)
                    dot.changepos(dot_x,dot_y)
                    screen = pygame.display.set_mode((ALL_WIDTH,ALL_HEIGHT))
                    black_dot.showup(-300,-300)
                    ii = ii+1
                    TEST_TIME  = TEST_TIME + 1

    if ii == TEST_TIME:
        break                
    


capture.release()


print("DONE")
cv2.destroyAllWindows()