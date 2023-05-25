import pygame
from time import sleep

pygame.mixer.init()
start = pygame.mixer.Sound("assets/hunt.mp3")
win_sound = pygame.mixer.Sound("assets/hunter_win.mp3")


# Class pour le hunter (poursuit le joueur)
class Hunter(pygame.sprite.Sprite):
    
    def __init__(self, walls, pos, size, group, retard = 400):
        self.walls = walls
        self.size = size
        self.group = group
        self.pos = pos
        # self.dust = []
        self.collide = False
        #liste des mouvements du joueur
        self.mouvs = []
        self.spawned = False
        self.retard = retard

    
    def SetWalls(self, walls):
        self.walls = walls

    def pre_move(self, dx, dy):
        # if dx == 0 and dy == 0:
        #     return

        self.mouvs.append((dx,dy))

        if self.spawned:
            x, y = self.mouvs.pop(0)
            self.move(x, y)
            global start

        elif len(self.mouvs) >= self.retard:
            self.spawned = True
            self.Spawn()
            start.play()
    def Spawn(self):
        super().__init__(self.group)
        self.image = pygame.image.load('assets/joueur.png')
        self.image = pygame.transform.scale(self.image,(self.size,self.size))

        self.rect = self.image.get_rect()
        self.rect.move_ip(self.pos[0], self.pos[1])
        #self.rect = pygame.Rect(pos[0], pos[1], size, size)

    def move(self, dx, dy):
        
        # Bouge chaque axes séparéments. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
            # if dx > 0:
            #     self.dust.append(Dust(self.rect.midleft))
            # if dx < 0:
            #     self.dust.append(Dust(self.rect.midright))
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # if not self.collide:
        #     if dx > 0:
        #         self.dust.append(Dust(self.rect.midleft))
        #     if dx < 0:
        #         self.dust.append(Dust(self.rect.midright))
        #     if dy > 0:
        #         self.dust.append(Dust(self.rect.midtop))
        #     if dy < 0:
        #         self.dust.append(Dust(self.rect.midbottom))
 
        # If you collide with a wall, move out based on velocity
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.collide = True
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
            else:
                self.collide = False


def Sound_win():
    win_sound.play()
    sleep(1000)
    return