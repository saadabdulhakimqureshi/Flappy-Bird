#Importing:
import pygame, sys, random
from tkinter import *
from PIL import Image, ImageTk

def game():
#Initialization and creating the screen:
# pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 2, buffer = 512)#To avoid delay in audio.
    
    pygame.init() #Initializing pygame.
    swidth = 576
    sheight = 1024
    game_win = pygame.display.set_mode((swidth,sheight)) #Creating game window.

    #Game clock:
    clock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird") #Game name.

    #Surfaces:

    #Display Surface:
    #Background:
    bg_surface = pygame.image.load('assets/background-day.png').convert()#Importing image.
    bg_surface = pygame.transform.scale2x(bg_surface)#Increasing image size by 2x.
    bg_surface_x_position = 0

    def draw_surface():
        game_win.blit(bg_surface, (bg_surface_x_position,0))
        game_win.blit(bg_surface, (bg_surface_x_position + swidth,0))

    #Floor:
    floor_surface = pygame.image.load("assets/base.png").convert()
    floor_surface = pygame.transform.scale2x(floor_surface)
    floor_surface_x_position = 0

    def draw_floor(floor_surface_x_position):
        game_win.blit(floor_surface, (floor_surface_x_position ,900))
        game_win.blit(floor_surface, (floor_surface_x_position + swidth,900))

    #Regular Surface:
    #Bird:
    # bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()#To make sure black box doesn't appear around rotated bird.
    # bird_surface = pygame.transform.scale2x(bird_surface)
    # bird_rect = bird_surface.get_rect(center = (100,512))#Creating a rectangle around bird to check for collisions.
    bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
    bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
    bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())


    #Animating Bird.
    bird_frames = [bird_downflap,bird_midflap,bird_upflap]
    bird_index = 0
    bird_surface = bird_frames[bird_index]
    bird_rect = bird_surface.get_rect(center = (100,512))

    BIRDFLAP = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRDFLAP, 200)


    def bird_animation():
        new_bird = bird_frames[bird_index]
        new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))#Getting centery of previous bird.
        return new_bird


    def rotate_bird(bird):
        new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)#Second argument is how much the bird will rotate.
        return new_bird
        
    #Game Over Surface:
    game_over = pygame.image.load("assets/gameover.png").convert_alpha()
    game_over = pygame.transform.scale2x(game_over)
    game_over_rect = game_over.get_rect(center = (288,500))

    #Pipes:
    pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
    pipe_surface = pygame.transform.scale2x(pipe_surface)
    pipe_list = []
    SPAWNPIPE = pygame.USEREVENT#An event that is triggered by timer. #Will be needed to draw pipes repeatidly.
    pygame.time.set_timer(SPAWNPIPE, 1200)#Time in miliseconds.
    pipe_height = [400, 600, 800]#All possible heights of list.

    def draw_pipes(pipes, score):
        for pipe in pipes:
            if pipe.bottom >= 1024: 
                game_win.blit(pipe_surface, pipe)
                if pipe.right == 62:
                    score += 1
                    score_sound.play()
            else:
                flip_pipe = pygame.transform.flip(pipe_surface, False, True)#Flipping top pipe.
                game_win.blit(flip_pipe, pipe)
            
        return score 

    def create_pipe():
        random_pipe_pos = random.choice(pipe_height)
        bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))#Creating pipe outside the screen.
        top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
        return (bottom_pipe, top_pipe)

    def move_pipes(pipes):
        for pipe in pipes:
            pipe.centerx -= 5
        return pipes

    #Collisions:
    def check_collision(pipes):
        for pipe in pipes:
            if bird_rect.colliderect(pipe):#If bird rectangle colides with pipe rectangle.
                return False

        if bird_rect.top <= -100 or bird_rect.bottom >= 900:#Checking if character collides with the floor or pipe outside screen.
            return False
        return True#Returns False by default.

    #Font:
    def score_display(game_status):
        if game_status == "First Run":
            score_surface = game_font.render(f"Score: {str(score)}", True, (255,255,255))#(String,Anti-Aliasing = True/False,(R,G,B))
            score_rect = score_surface.get_rect(center = (288, 100))
            game_win.blit(score_surface, score_rect)

        elif game_status == "Not First Run":#To display high score only after first run.
            score_surface = game_font.render(f"Score: {str(score)}", True, (255,255,255))#(String,Anti-Aliasing = True/False,(R,G,B))
            score_rect = score_surface.get_rect(center = (288, 100))
            game_win.blit(score_surface, score_rect)
            high_score_surface = game_font.render(f"High Score: {str(high_score)}", True, (255,255,255))#(String,Anti-Aliasing = True/False,(R,G,B))
            high_score_rect = score_surface.get_rect(center = (250, 850))
            game_win.blit(high_score_surface, high_score_rect)
        

    game_font = pygame.font.Font('04b_19.ttf', 40)#(Font Name, Size)

    #Game Variables: 
    #Bird Movement:
    gravity = 0.25 #To make sure bird goes down.
    bird_movement = 0

    #Game Over Logic:
    game_active = True

    #Score:
    score = 0
    high_score = 0
    game_status = "First Run"

    #Sound: 
    flap_sound =pygame.mixer.Sound('sound/sfx_wing.wav')#Importing sound file.
    death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
    death = True
    score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and game_active:
                bird_movement = 0#Stopping fall.
                bird_movement -= 10#Moving Up.
                #Flap Sound:
                flap_sound.play()
            if keys[pygame.K_SPACE] and game_active == False:#Restarting game after game is lost.
                game_active = True #Restarting Game.
                death = True
                #To avoid bugs:
                pipe_list = []  
                bird_rect.center = (100, 512)
                bird_movement = 0



            if event.type == SPAWNPIPE:#Every 1200 miliseconds. #Creating new pipe.
                pipe_list.extend(create_pipe())#Will create a new rectangle every 1.2 seconds.

            if event.type == BIRDFLAP:#Every 200 miliseconds. #Animating Bird.
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0

        #Drawing background
        bg_surface_x_position -= 1
        draw_surface()
        if bg_surface_x_position < (-1*swidth):#Indicating both surfaces have reached the end of window.
            bg_surface_x_position = 0

        #Drawing floor:
        floor_surface_x_position -= 1
        draw_floor(floor_surface_x_position)

        if floor_surface_x_position < (-1*swidth):
            floor_surface_x_position = 0

        #Checking for collisions:
        game_active = check_collision(pipe_list)

        if game_active:
            #Drawing bird:
            bird_surface = bird_animation()
            bird_movement += gravity
            bird_rect.centery += bird_movement#Moving bird up.
            rotated_bird = rotate_bird(bird_surface)
            game_win.blit(rotated_bird, bird_rect)#Bird rect corresponds to centerx and centery coordinates.

            #Drawing pipes:
            pipe_list = move_pipes(pipe_list)
            score = draw_pipes(pipe_list,score)
            score_display(game_status)
        else:
            #Checking score and changing game status.
            
            if score > 0:
                game_status = "Not First Run"
            if score > high_score:
                high_score = score
                score = 0
            if death == True:#To make sure death sound doesn't play repeatidly.
                death_sound.play()
                death = False
            game_win.blit(game_over,game_over_rect)


        pygame.display.update()#Updating display.
        clock.tick(120)
def gui():

    root = Tk()

    # canvas = Canvas(root, width = 576, height = 1024)

    # canvas.pack()

    img = Image.open("assets/background-day.png")
    img = img.resize((576,1024))
    img = ImageTk.PhotoImage(img)
    button = Button(root, padx = 0, pady = 0, text = "Play", command = game)

    label = Label(image = img)

    button.pack()
    label.pack()  

    root.mainloop()

gui()