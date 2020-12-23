import random
import pygame


class AIChicken():
    def __init__(self, loc, egg_sprite, chick_sprite, chicken_sprite, screen_width, screen_height, state=0, player=False):

        # load parameters
        self.loc = loc
        self.state = state
        self.egg_sprite = egg_sprite
        self.chick_sprite= chick_sprite
        self.chicken_sprite = chicken_sprite
        self.player = player  #
        self.screen_width = screen_width
        self.screen_height = screen_height

        # set defaults
        self.current_sprite = self.egg_sprite
        self.x_direction = 0
        self.y_direction = 0
        self.speed = random.randrange(500, 1000) / 100

        # start movement
        self.changedirection()

    def update(self):

        if self.state == 0:
            if random.randrange(0, 100) == 1:
                self.state = 1
                return True

        if self.state in [1,2]:

            tempsprite = self.chick_sprite if self.state == 1 else self.chicken_sprite

            self.current_sprite = pygame.transform.flip(tempsprite, self.x_direction > 0, False)

            self.current_sprite.set_colorkey((255, 255, 255))

            # bounce off walls

            self.x_direction = self.horizontal_bounce()
            self.y_direction = self.vertical_bounce()

            self.loc = (self.loc[0] + self.x_direction * self.speed, self.loc[1] + self.y_direction * self.speed)

            if random.randrange(0, 25) == 1:
                self.changedirection()

            if random.randrange(0, 500) == 1:
                self.state = 2

        return False

    def vertical_bounce(self):
        bottom_edge = self.loc[1] + self.speed + self.current_sprite.get_height()

        if self.loc[1] < 0:
            return 1
        if bottom_edge>self.screen_height:
            return -1

        return self.y_direction

    def horizontal_bounce(self):
        right_edge = self.loc[0] + self.speed + self.current_sprite.get_width()

        if self.loc[0]<0:
            return 1
        if right_edge > self.speed + self.screen_width:
            return -1

        return self.x_direction

    def changedirection(self):
        self.x_direction, self.y_direction = random.choice([(-1, 0), (0, -1), (1, 0), (0, 1)])


def isnear(a, b, distance):
    print(a, b, distance, a[0] - b[0]), abs(a[1] - b[1])
    if abs(a[0] - b[0]) + abs(a[1] - b[1]) < distance:
        return True
    return False


def image_to_sprite(img, scale):
    sprite = pygame.image.load(img).convert_alpha()
    sprite = pygame.transform.scale(sprite, scale)
    sprite.set_colorkey((255, 255, 255))
    return sprite
