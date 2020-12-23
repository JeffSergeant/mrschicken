import pygame, os
from HappyMrsChicken import AIChicken
from HappyMrsChicken import isnear
from HappyMrsChicken import image_to_sprite
from pygame.locals import *
import random

from IScene import IScene


class GameScene(IScene):
    def __init__(self):

        def setup_pygame():
            pygame.init()
            os.environ['SDL_VIDEO_CENTERED'] = '1'
            self.clock = pygame.time.Clock()
            flags = pygame.FULLSCREEN
            self.display = pygame.display.set_mode(self.size, flags)
            pygame.display.set_caption('Happy Mrs. Chicken')

        def setup_sprites():

            img_chicken = 'Res/chicken.png'
            self.mrschicken = image_to_sprite(img_chicken,(200,150))
            self.chick = image_to_sprite(img_chicken,(100,75))

            img_egg = 'Res/egg.jpg'
            self.egg = image_to_sprite(img_egg, (100, 100))

            img_nest = 'Res/nest.png'
            self.nest = image_to_sprite(img_nest, (200, 150))

            img_nest_front = 'Res/nestFront.png'
            self.nest_front = image_to_sprite(img_nest_front, (200, 150))



        self.screen_width=1280
        self.screen_height=768
        self.background_colour = (125, 200, 255)
        self.size=(self.screen_width, self.screen_height)

        # TODO Make these part of a Player Class
        self.x = 325
        self.y = 250
        self.speed = 20
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.eggs = []
        self.nests = []
        self.nest_location=(0,0)

        setup_pygame()
        setup_sprites()

    def set_nest_location(self):
        self.nest_location = (random.randrange(50, self.screen_width - 50), random.randrange(50, self.screen_height - 100))

    def lay_egg(self):

        if isnear(self.nest_location, (self.x + 40, self.y + 50), 200):
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Res\lay.wav'))

            self.eggs.append(
                AIChicken((self.nest_location[0] + 40, self.nest_location[1]), self.egg, self.chick, self.mrschicken,
                          self.screen_width, self.screen_height))

            self.nests.append(self.nest_location)

            self.set_nest_location()

    def initialise(self):

        pygame.mixer.music.load('Res/cluck.wav')
        pygame.mixer.music.play(-1)
        print("INIT")
        return True

    def update(self):

        self.display.fill(self.background_colour)

        # Handle  Events
        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return False #Stop Updating

                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                        return False #Stop Updating

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.lay_egg()

        self.do_player_movement()

        self.update_sprites() # redraw sprites AND update states on eggs + chickens

        pygame.display.flip()

        self.clock.tick(30)
        return True

    def update_sprites(self):
        # sequence here used to determine Z value,  TODO find a way to do this properly

        self.draw_nests()

        egg_characters = [e for e in self.eggs if e.state == 0]
        chicken_characters = [e for e in self.eggs if e.state in [1, 2]]

        self.update_eggs(egg_characters)

        self.draw_nest_fronts()

        self.update_chickens(chicken_characters)

        self.display.blit(self.mrschicken, (self.x, self.y)) # update player sprite

    def update_chickens(self, chicken_characters):
        for chicken_character in chicken_characters:
            if chicken_character.update() and len(chicken_characters) < 2:
                self.eggs.append(AIChicken(chicken_character.loc, self.egg, self.chick, self.mrschicken,
                                           self.screen_width, self.screen_height))

            self.display.blit(chicken_character.current_sprite, chicken_character.loc)

    def update_eggs(self, egg_characters):
        for egg_character in egg_characters:
            if egg_character.update():
                for used_nest in self.nests:
                    if used_nest == (egg_character.loc[0] - 40, egg_character.loc[1]):
                        self.nests.remove(used_nest)
                        break

            self.display.blit(egg_character.current_sprite, egg_character.loc)

    def draw_nest_fronts(self):
        for old_nest in self.nests:
            self.display.blit(self.nest_front, old_nest)

        self.display.blit(self.nest_front, self.nest_location)

    def draw_nests(self):
        self.display.blit(self.nest, self.nest_location)
        for old_nest in self.nests:
            self.display.blit(self.nest, old_nest)

    def do_player_movement(self):
        keys = pygame.key.get_pressed()
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]
        up = keys[pygame.K_UP]
        down = keys[pygame.K_DOWN]

        # Move x,y based on keys
        self.x += self.speed * (right - left)
        self.y += self.speed * (down - up)
        # Limit The Player Movement within the boundary
        max_x = self.screen_width - self.mrschicken.get_width()
        max_y = self.screen_height - self.mrschicken.get_height()
        self.x = max(min(self.x, max_x), 0)
        self.y = max(min(self.y, max_y), 0)


