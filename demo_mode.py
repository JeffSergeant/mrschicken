import pygame, os
from HappyMrsChicken import AIChicken
from HappyMrsChicken import isnear
from pygame.locals import *

chicken = 'Res/chicken.png'
egg = 'Res/egg.jpg'
imgtitle = 'Res/title.png'

pygame.init()

#============VARIABLES==============
os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
screen_width=1280
screen_height=768
bgColor = (50,50, 255)
size=(screen_width, screen_height)
display = pygame.display.set_mode(size)
progress = True
pygame.display.set_caption('Happy Mrs. Chicken')

title = pygame.image.load(imgtitle).convert_alpha()

mrschicken = pygame.image.load(chicken).convert_alpha()
mrschicken = pygame.transform.scale(mrschicken, (200, 150))
mrschicken.set_colorkey((255,255,255))

eggSprite = pygame.image.load(egg).convert_alpha()
eggSprite = pygame.transform.scale(eggSprite, (100, 100))
eggSprite.set_colorkey((255,255,255))

eggs = []



x=325
y=250
speed = 20
left = False
right = False
up = False
down = False

display.fill(bgColor)
display.blit(title, (100, screen_height*.25))
display.blit(mrschicken, (screen_width/2+100, screen_height*.75))
display.blit(eggSprite, (screen_width/2-100, screen_height*.75))
pygame.display.flip()
pygame.time.wait(5000)

pygame.mixer.music.load('Res/cluck.wav')
pygame.mixer.music.play(-1)
player = AIChicken((x,y),eggSprite,mrschicken,screen_width,screen_height,1)
player.state = 1

#============MAIN LOOP==============
while progress:
        x,y = player.loc
        display.fill(bgColor)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        progress = False
                        pygame.quit()
                        quit()
                elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                                progress = False
                                pygame.quit()
                                quit()
                #Player Input KeyDown
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                                left = True
                        elif event.key == pygame.K_RIGHT:
                                right = True
                        elif event.key == pygame.K_UP:
                                up = True
                        elif event.key == pygame.K_DOWN:
                                down = True
                        elif event.key == pygame.K_SPACE:
                                eggs.append(AIChicken((x,y),eggSprite,mrschicken,screen_width,screen_height))
                        
                #Player Input KeyUP           
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                                left = False
                        elif event.key == pygame.K_RIGHT:
                                right = False
                        elif event.key == pygame.K_UP:
                                up = False
                        elif event.key == pygame.K_DOWN:
                                down = False
        #Sprite Started To Move
        if left:
                x-=speed
        elif right:
                x+=speed
        elif up:
                y-=speed
        elif down:
                y+=speed

        #Limit The Player Movement within the boundary
        if x > screen_width - mrschicken.get_width():
                x = screen_width - mrschicken.get_width()
        if x < 0:
                x = 0
        if y > screen_height - mrschicken.get_height():
                y = screen_height - mrschicken.get_height()
        if y < 0:
                y = 0

        for egg in eggs:
            if egg.update() and len(eggs)<25:
                eggs.append(AIChicken(egg.loc,eggSprite,mrschicken,screen_width,screen_height))
            display.blit(egg.current_sprite, egg.loc)

        egg_characters = [e for e in eggs if e.state == 0]
        chicken_characters = [e for e in eggs if e.state == 1]

        for egg_character in egg_characters:
                display.blit(egg_character.current_sprite, egg_character.loc)

        for chicken_character in chicken_characters:
                display.blit(chicken_character.current_sprite, chicken_character.loc)

        player.update()
        display.blit(player.current_sprite, player.loc)

        pygame.display.flip()

        #Framerate of the Game
        clock.tick(30)
