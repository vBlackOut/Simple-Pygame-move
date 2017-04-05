import pygame, sys, math
from pygame.locals import *
from math import atan2, degrees, pi


# some simple vector helper functions, stolen from http://stackoverflow.com/a/4114962/142637
def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]    

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def normalize(v):
    vmag = magnitude(v)
    return [ v[i]/vmag  for i in range(len(v)) ]

class Ship(object):
    def __init__(self):
        self.x, self.y = (0, 0)
        self.set_target((0, 0))
        self.speed = 5
        self.rotation = 0
        self.positionViseurX = 0
        self.positionViseurY = 0

    @property
    def pos(self):
        return self.x, self.y

    # for drawing, we need the position as tuple of ints
    # so lets create a helper property
    @property
    def int_pos(self):
        return map(int, self.pos)

    @property
    def target(self):
        return self.t_x, self.t_y

    @property
    def int_target(self):
        return map(int, self.target)   

    def set_target(self, pos):
        self.t_x, self.t_y = pos

    def update(self):
        # if we won't move, don't calculate new vectors
        if self.int_pos == self.int_target:
            return 

        target_vector = sub(self.target, self.pos) 

        # a threshold to stop moving if the distance is to small.
        # it prevents a 'flickering' between two points
        if magnitude(target_vector) < 2: 
            return

        # apply the ship's speed to the vector
        move_vector = [c * self.speed for c in normalize(target_vector)]

        # update position
        self.x, self.y = add(self.pos, move_vector)

    def draw(self, s):
        positionCanonX = 200
        positionCanonY = 150
        positionViseurX = 100
        positionViseurY = 100

        pygame.draw.circle(s, (255, 0 ,0), self.int_pos, 2)
        player = pygame.image.load("player.png")
        w,h = player.get_size()
        player = pygame.transform.scale(player, (int(w/2), int(h/2)))
        pygame.draw.line(screen, black, [self.int_pos[0], self.int_pos[1]], [self.int_pos[0]+10, self.int_pos[1]+10], 5)

        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    positionCanonY += 3
                     
                elif event.key == K_UP:
                    positionCanonY -= 3
                elif event.key == K_RIGHT:
                    positionCanonX += 3
                elif event.key == K_LEFT:
                    positionCanonX -= 3
            if event.type == MOUSEMOTION:
                self.positionViseurX = event.pos[0]-19
                self.positionViseurY = event.pos[1]-19
                self.rotation += 2

        dx = self.positionViseurX - self.int_pos[0]
        dy = self.positionViseurY - self.int_pos[1]
        rads = atan2(-dy,dx)
        rads %= 2*pi
        degs = degrees(rads)

        print self.rotation
        Rotate = pygame.transform.rotate(player, degs+90)
        screen.fill((255,255,255,128))
        pygame.draw.rect(s,-1,s.blit(Rotate, self.int_pos),1)

 
pygame.init()
quit = False
ship = Ship()

size = width, height = 1600, 848
speed = [2, 2]
black = (0, 0, 0)
rotation = 0

pygame.mouse.set_cursor(*pygame.cursors.broken_x)

screen = pygame.display.set_mode(size)
clock=pygame.time.Clock()


while not quit:
    quit = pygame.event.get(pygame.QUIT)
    if pygame.event.get(pygame.MOUSEBUTTONDOWN):
        ship.set_target(pygame.mouse.get_pos())
    pygame.event.poll()
    ship.update()
    screen.fill((0, 0, 255))
    ship.draw(screen)
    pygame.display.flip()
    clock.tick(60)

