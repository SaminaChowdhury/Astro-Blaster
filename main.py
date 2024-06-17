import pygame
import sys
import random
import math
from pygame.locals import *

# Initialize Pygame and mixer for sound
pygame.mixer.pre_init()
pygame.init()

# Set up the game clock for FPS control
fps = pygame.time.Clock()

# Define color constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Define global variables for screen dimensions and game state
WIDTH = 1320
HEIGHT = 600
time = 0

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Asteroids (Space Game)')

# Load images
bg = pygame.image.load('Photos/background.jpg')
debris = pygame.image.load('Photos/debris2_brown.png')
ship = pygame.image.load('Photos/ship.png')
ship_thrusted = pygame.image.load('Photos/ship_thrusted.png')
asteroid = pygame.image.load('Photos/003-asteroid.png')
shot = pygame.image.load('Photos/shot2.png')

# Load sounds
missile_sound = pygame.mixer.Sound('Sound/missile.mp3')
missile_sound.set_volume(0.3)
thruster_sound = pygame.mixer.Sound('Sound/thrust.mp3')
thruster_sound.set_volume(1)
explosion_sound = pygame.mixer.Sound('Sound/sci-fi_explosion_1-42890.mp3')
explosion_sound.set_volume(10)

# Play background music
pygame.mixer.music.load('Sound/game-music-loop-6-144641.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Initialize ship variables
ship_x = WIDTH / 2 - 50
ship_y = HEIGHT / 2 - 50
ship_angle = 0
ship_is_rotating = False
ship_is_forward = False
ship_direction = 0
ship_speed = 0

# Initialize asteroid variables
asteroid_x = []
asteroid_y = []
asteroid_angle = []
asteroid_speed = 2
no_of_asteroids = 10

# Initialize bullet variables
bullet_x = []
bullet_y = []
bullet_angle = []
no_of_bullets = 0

# Initialize game state variables
score = 0
game_over = False
playing = True

# Set up initial positions for asteroids
for i in range(0, no_of_asteroids):
    asteroid_x.append(random.randint(0, WIDTH))
    asteroid_y.append(random.randint(0, HEIGHT))
    asteroid_angle.append(random.randint(0, 365))

# Function to rotate images around their center
def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

# Function to draw game elements on the canvas
def draw(canvas):
    global time, bullet_x, bullet_y
    global ship_is_forward, score
    canvas.fill(BLACK)
    canvas.blit(bg, (0, 0))
    canvas.blit(debris, (time * .3, 0))
    canvas.blit(debris, (time * .3 - WIDTH, 0))    
    time = time + 1

    for i in range(0, no_of_bullets):
        canvas.blit(shot, (bullet_x[i], bullet_y[i]))

    for i in range(0, no_of_asteroids):
        canvas.blit(rot_center(asteroid, time), (asteroid_x[i], asteroid_y[i]))

    if ship_is_forward:
        canvas.blit(rot_center(ship_thrusted, ship_angle), (ship_x, ship_y))
    else:
        canvas.blit(rot_center(ship, ship_angle), (ship_x, ship_y))

    # Draw score
    myfont1 = pygame.font.SysFont("Comic Sans MS", 40)
    label1 = myfont1.render("Score : " + str(score), 1, (255, 255, 0))
    canvas.blit(label1, (50, 20))

    # Draw pause button
    if game_over == False and playing == True:
        pause_button = myfont1.render('P : Pause', 1, (255, 255, 0))
        canvas.blit(pause_button, (1130, 20))

    # Draw game over screen
    if game_over:
        myfont2 = pygame.font.SysFont("Comic Sans MS", 80)
        label2 = myfont2.render("GAME OVER ", 1, (255, 0, 40))
        canvas.blit(label2, (WIDTH / 2 - 230, HEIGHT / 2 - 60))

        myfont3 = pygame.font.SysFont('Comic Sans MS', 40)
        label13 = myfont3.render('Total Score: ' + str(score), 1, (250, 0, 0))
        canvas.blit(label13, (520, 348))

        label17 = myfont3.render('R : Restart!', 1, (250, 0, 0))
        label117 = myfont3.render('Q : Quit', 1, (250, 0, 0))
        canvas.blit(label17, (522, 388))
        canvas.blit(label117, (514, 426))
        pygame.mixer.music.stop()
    
    # Draw pause screen
    if playing == False:
        myfont4 = pygame.font.SysFont("Comic Sans MS", 80)
        label4 = myfont4.render("PAUSED", 1, (112, 209, 240))
        canvas.blit(label4, (WIDTH / 2 - 290, HEIGHT / 2 - 90))

        myfont5 = pygame.font.SysFont("Comic Sans MS", 40)
        label5 = myfont5.render('P : Resume', 1, (112, 209, 240))    
        canvas.blit(label5, (WIDTH / 2 - 260, HEIGHT / 2))
        label100 = myfont5.render('Q : Quit', 1, (112, 209, 240))
        canvas.blit(label100, (WIDTH / 2 - 269, HEIGHT / 2 + 50))

# Function to handle player input
def handle_input():
    global ship_angle, ship_is_rotating, ship_direction
    global ship_x, ship_y, ship_speed, ship_is_forward
    global bullet_x, bullet_y, bullet_angle, no_of_bullets
    global missile_sound, thruster_sound, playing, score, game_over

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT and game_over == False and playing == True:
                ship_is_rotating = True
                ship_direction = 1
            elif event.key == K_RIGHT and game_over == False and playing == True:
                ship_is_rotating = True
                ship_direction = 0
            elif event.key == K_UP and game_over == False and playing == True:
                ship_is_forward = True
                ship_speed = 10
                thruster_sound.play()
            elif event.key == K_DOWN:
                ship_is_forward = False
                ship_speed = 0
            elif event.key == K_SPACE and game_over == False and playing == True:
                bullet_x.append(ship_x + 50)
                bullet_y.append(ship_y + 50)
                bullet_angle.append(ship_angle)
                no_of_bullets = no_of_bullets + 1
                missile_sound.play()
            elif event.key == K_LCTRL and game_over == False and playing == True:
                ship_is_forward = True
                ship_speed = 20                
                thruster_sound.play()
            elif event.key == K_p and game_over == False:
                if playing == True:
                    playing = False
                    pygame.mixer.music.stop()
                    ship_speed = 0
                else:
                    playing = True
                    pygame.mixer.music.play()
            elif game_over == True:
                if event.key == K_r:
                    game_over = False
                    score = 0
                    pygame.mixer.music.play()
                elif event.key == K_q:
                    sys.exit()
            elif event.key == K_q:
                sys.exit()
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                ship_is_rotating = False
            else:
                ship_is_forward = False
                thruster_sound.stop()
            if event.key == K_SPACE and game_over == False and playing == True:
                ship_is_forward = True

    if ship_is_rotating:
        if ship_direction == 0:
            ship_angle = ship_angle - 10
        else:
            ship_angle = ship_angle + 10

    if ship_is_forward or ship_speed > 0:
        ship_x = (ship_x + math.cos(math.radians(ship_angle)) * ship_speed)
        ship_y = (ship_y + -math.sin(math.radians(ship_angle)) * ship_speed)
        if ship_is_forward == False:
            ship_speed = ship_speed - 0.1

# Function to update the screen
def update_screen():
    pygame.display.update()
    fps.tick(60)

# Function to check collision between two objects
def isCollision(enemyX, enemyY, bulletX, bulletY, dist):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < dist:
        return True
    else:
        return False

# Game logic for updating positions and checking collisions
def game_logic():
    global asteroid_y, bullet_x, bullet_y, no_of_bullets
    global game_over, score
    for i in range(0, no_of_bullets):
        bullet_x[i] = (bullet_x[i] + math.cos(math.radians(bullet_angle[i])) * 10)
        bullet_y[i] = (bullet_y[i] + -math.sin(math.radians(bullet_angle[i])) * 10)
   
    for i in range(0, no_of_asteroids):
        asteroid_x[i] = (asteroid_x[i] + math.cos(math.radians(asteroid_angle[i])) * asteroid_speed)
        asteroid_y[i] = (asteroid_y[i] + -math.sin(math.radians(asteroid_angle[i])) * asteroid_speed)

        if asteroid_y[i] < 0:
            asteroid_y[i] = HEIGHT
        
        if asteroid_y[i] > HEIGHT:
            asteroid_y[i] = 0

        if asteroid_x[i] < 0:
            asteroid_x[i] = WIDTH
        
        if asteroid_x[i] > WIDTH:
            asteroid_x[i] = 0

        if isCollision(ship_x, ship_y, asteroid_x[i], asteroid_y[i], 27):
            game_over = True
            print('\nGame Over\n')
    
    for i in range(0, no_of_bullets):
        for j in range(0, no_of_asteroids):
            if isCollision(bullet_x[i], bullet_y[i], asteroid_x[j], asteroid_y[j], 50):
                asteroid_x[j] = random.randint(0, WIDTH)
                asteroid_y[j] = random.randint(0, HEIGHT)
                asteroid_angle[j] = random.randint(0, 365)
                explosion_sound.play()
                score = score + 1

# Main game loop
while True:
    draw(window)
    handle_input()
    update_screen()
    if not game_over:
        if playing:
            game_logic()
    update_screen()
