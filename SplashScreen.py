import pygame, os
from HappyMrsChicken import AIChicken
from HappyMrsChicken import image_to_sprite
from pygame.locals import *
import random

from IScene import IScene

from GameScene import GameScene


class SplashScreen(IScene):
    def __init__(self):

        self.size, self.display, self.clock = self.setup_pygame()
        screen_width,screen_height = self.size

        self.setup_sprites()

        background_colour = (125, 200, 255)

        self.display.fill(background_colour)
        self.display.blit(self.title, (100, screen_height * .25))
        self.display.blit(self.mrschicken, (screen_width / 2 + 100, screen_height * .75))
        self.display.blit(self.nest, (screen_width / 2 - 100, screen_height * .75))
        self.display.blit(self.egg, (screen_width / 2 - 60, screen_height * .75))
        self.display.blit(self.nest_front, (screen_width / 2 - 100, screen_height * .75))

        pygame.display.flip()
        pygame.time.wait(2500)

    def setup_sprites(self):
        self.img_title = 'Res/title.png'
        self.title = pygame.image.load(self.img_title).convert_alpha()

        img_chicken = 'Res/chicken.png'
        self.mrschicken = image_to_sprite(img_chicken, (200, 150))
        self.chick = image_to_sprite(img_chicken, (100, 75))

        img_egg = 'Res/egg.jpg'
        self.egg = image_to_sprite(img_egg, (100, 100))

        img_nest = 'Res/nest.png'
        self.nest = image_to_sprite(img_nest, (200, 150))

        img_nest_front = 'Res/nestFront.png'
        self.nest_front = image_to_sprite(img_nest_front, (200, 150))

    def setup_pygame(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        size = (1280,768)
        clock = pygame.time.Clock()
        flags = pygame.NOFRAME
        display = pygame.display.set_mode(size, flags)
        return size,display,clock

    def update(self):

        pygame.time.wait(2500)
        pygame.mixer.music.load('Res/cluck.wav')
        pygame.mixer.music.play(-1)
        return False

    def close(self):
        pygame.quit()
        print("Quitting, returning GameScene")
        return GameScene()