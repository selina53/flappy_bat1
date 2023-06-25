# Import module
import random
import sys
import pygame
from pygame.locals import *
from os import path
import time

# All the Game Variables
window_width = 600
window_height = 499

snd_dir = path.join(path.dirname(__file__), 'snd')


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# set height and width of window
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8

game_images = {}
framepersecond = 32

obst1_image = 'Obst1.png'
obst2_image = 'Obst2.png'
obst3_image = 'Obst3.png'
obst4_image = 'Obst4.png'
background_image = 'background.jpg'
bird_down_image = 'Bat right1.png'
bird_up_image = 'Bat right2.png'
echo_image = 'Echo.png'
web_image = 'Obst web.png'

transColor = (255, 0, 255)

player_img = pygame.image.load("Bat right1.png").convert()

web_img = pygame.image.load("Obst web.png").convert()
echo_img = pygame.image.load("Echo.png").convert()
live_img_tmp = pygame.image.load("heart.png").convert()
live_img1 = pygame.transform.scale(live_img_tmp, (50, 40))
live_img2 = pygame.transform.scale(live_img_tmp, (50, 40))
live_img3 = pygame.transform.scale(live_img_tmp, (50, 40))



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100, 75))
        self.image.set_colorkey(BLACK)
        #self.image = pygame.Surface((100, 75))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = window_width / 5
        self.rect.y = window_height / 2 
        self.bird_velocity_y = -9
        self.bird_Max_Vel_Y = 10
        self.bird_Min_Vel_Y = -10
        self.birdAccY = 0.75
        self.bird_flap_velocity = -10
        self.bird_flapped = False
        self.lives = 3
        
    def flap(self):
        self.bird_velocity_y = self.bird_flap_velocity
        self.bird_flapped = True

    def update(self):
        if self.bird_velocity_y < self.bird_Max_Vel_Y and not self.bird_flapped:
            self.bird_velocity_y += self.birdAccY

        if self.bird_flapped:
            self.bird_flapped = False
        
        playerHeight = game_images['flappybird'][0].get_height()    
        self.rect.y = self.rect.y + min(self.bird_velocity_y, playerHeight)
            
        return self.bird_velocity_y

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()
        
    #def blink(self):
     #   print("blink")
        """player_img = pygame.image.load("Bat right1.png").convert()
        player_img.set_alpha(150)
        self.image = pygame.transform.scale(player_img, (100, 75))
        self.image.set_colorkey((0,0,0))
        self.image.set_colorkey(BLACK)
        self.image.set_colorkey((0,0,0))
        self.image.set_colorkey(BLACK)"""

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image =  pygame.transform.scale(echo_img, (55, 18))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        #print(x, y)

    def update(self):
        self.rect.x -= self.speedy
        # kill if it moves off the top of the screen
        if self.rect.right < 0:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(web_img, (60, 60))
        self.image.set_colorkey(BLACK)
        #self.image = pygame.Surface((60, 60))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.rect.width+250, window_width-20)
        self.rect.y = random.randrange(20, window_height-20)
        self.speedx = -4

        
    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < -10 or self.rect.right > window_width+10:
            self.rect.x = random.randrange(self.rect.width+20, window_width-20, random.randrange(10, 50))
            self.rect.y = random.randrange(0, window_height, random.randrange(10,50))
            

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(3):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    #print("mob created", m.rect)

def flappygame():

    your_score = 0
    horizontal = int(window_width/5)
    #print(horizontal)
    vertical = int(window_width/2)

    ground = 0
    mytempheight = 100

    # Generating two pipes for blitting on window
    first_pipe = createObst()
    second_pipe = createObst()

    # List containing lower pipes
    down_pipes = [
        {'x': window_width+300-mytempheight,
        'y': first_pipe[1]['y']},
        {'x': window_width+300-mytempheight+(window_width/2),
        'y': second_pipe[1]['y']},
    ]

    # List Containing upper pipes
    up_pipes = [
        {'x': window_width+300-mytempheight,
        'y': first_pipe[0]['y']},
        {'x': window_width+200-mytempheight+(window_width/2),
        'y': second_pipe[0]['y']},
    ]

    # pipe velocity along x
    pipeVelX = -4

    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    player.flap()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    player.shoot()
        
        all_sprites.update()
        

        # This function will return true
        # if the flappybird is crashed
        game_over = isGameOver(horizontal,
                            vertical,
                            up_pipes,
                            down_pipes)
                            
        hits = pygame.sprite.spritecollide(player, mobs, True)
       
        if game_over or hits:
            #print(player.lives)
            player_die_sound.play()
            player.lives -= 1
            if player.lives < 0:
                game_over_sound.play()
                time.sleep(3)
                pygame.quit()
                sys.exit()
            #player.blink()
            if player.lives == 2:
                live_img3.fill((0,0,0,0))
            if player.lives == 1:
                live_img2.fill((0,0,0,0))
            if player.lives == 0:
                live_img1.fill((0,0,0,0))
            
      
        # check for your_score
        playerMidPos = horizontal + game_images['flappybird'][0].get_width()
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['obstacle'][1].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1
                print(f"Your your_score is {your_score}")

        bird_velocity_y = player.update()
        

        
        #vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)
        #vertical = vertical + min(bird_velocity_y, playerHeight)
        vertical = player.rect.y
        
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        
        for hit in hits:
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

    # check to see if a mob hit the player
        """ 
        for m in mobs:
        
            hits = pygame.sprite.spritecollide(player, m, True)
            #print(hits)       
            print("Player", player.rect)
            print("MOB", m.rect)
            if hits:
                print("HIT")
                return
        """

       # hits = pygame.sprite.spritecollide(player, mobs, True)
        
       # if hits:
        #    return

        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is
        # about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createObst()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['obstacle'][1].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['obstacle'][1],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['obstacle'][1],
                        (lowerPipe['x'], lowerPipe['y']))
               

        #window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'][0], (horizontal, vertical))
        

        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width)/1.1

        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num],
                        (Xoffset, window_width*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()
            
        window.blit(live_img1, (20, 20))
        window.blit(live_img2, (55, 20))
        window.blit(live_img3, (90, 20))

        # Refreshing the game window and displaying the score.
    

                    
        all_sprites.draw(window)
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)
    pygaem.quit()


def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    #if vertical > elevation - 25 or vertical < 0:
    if vertical > window_height or vertical < 0:    
        return True

    for pipe in up_pipes:
        pipeHeight = game_images['obstacle'][0].get_height()
        if(vertical < pipeHeight + pipe['y'] and abs(horizontal - pipe['x']) < game_images['obstacle'][1].get_width()):
            return True

    for pipe in down_pipes:
        if (vertical + game_images['flappybird'][0].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['obstacle'][0].get_width():
            return True
    return False


def createObst():

    offset = window_height/3
    pipeHeight = game_images['obstacle'][1].get_height()
    y2 = offset + random.randrange(0, int(window_height - 1.2 * offset))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    # upper and lover pipe
    pipe = [{'x': pipeX, 'y': -y1}, {'x': pipeX, 'y': y2}]
    return pipe




# program where the game starts
if __name__ == "__main__":

    # For initializing modules of pygame library
    pygame.init()
    pygame.mixer.init()
    framepersecond_clock = pygame.time.Clock()

    # Sets the title on top of game window
    pygame.display.set_caption('Flappy Bird Game')

    # Load all the images which we will use in the game

    # images for displaying score
    
    shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'click.mp3'))
    game_over_sound = pygame.mixer.Sound(path.join(snd_dir, 'gameover.wav'))

    player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
    pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
    pygame.mixer.music.set_volume(0.4)
    
    game_images['scoreimages'] = (
        pygame.image.load('0.png').convert_alpha(),
        pygame.image.load('1.png').convert_alpha(),
        pygame.image.load('2.png').convert_alpha(),
        pygame.image.load('3.png').convert_alpha(),
        pygame.image.load('4.png').convert_alpha(),
        pygame.image.load('5.png').convert_alpha(),
        pygame.image.load('6.png').convert_alpha(),
        pygame.image.load('7.png').convert_alpha(),
        pygame.image.load('8.png').convert_alpha(),
        pygame.image.load('9.png').convert_alpha()
    )
    
    img1 = pygame.image.load(bird_up_image)
    tr1 = pygame.transform.scale(img1, (100, 75))
    img2 = pygame.image.load(bird_down_image)
    tr2= pygame.transform.scale(img2, (100, 75))
    game_images['flappybird'] = (tr1.convert_alpha(), tr2.convert_alpha())
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    
    img1 = pygame.image.load(obst2_image)
    tr1 = pygame.transform.scale(img1, (50, 320))
    img2 = pygame.image.load(obst3_image)
    tr2= pygame.transform.scale(img2, (50, 320))
    
    game_images['obstacle'] = (tr1.convert_alpha(),tr2.convert_alpha())
    
    img1 = pygame.image.load(echo_image)
    tr1 = pygame.transform.scale(img1, (45, 45))


    game_images['echo'] = tr1.convert_alpha()

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    # Here starts the main game

    while True:

        # sets the coordinates of flappy bird
        #self.rect.x = window_width / 2
        #self.rect.y = window_height - 10
        horizontal = window_width / 5
        vertical = window_height / 2
        ground = 0
        while True:
            for event in pygame.event.get():

                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # If the user presses space or
                # up key, start the game for them
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    flappygame()

                # if user doesn't press anykey Nothing happen
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['flappybird'][0], (horizontal, vertical))
                    #window.blit(game_images['sea_level'], (ground, elevation))
                    pygame.display.update()
                    framepersecond_clock.tick(framepersecond)

