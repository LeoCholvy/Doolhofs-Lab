import os
import sys
import pygame


# Class pour le carré orange
class Player(object):
    
    def __init__(self, walls, pos):
        self.walls = walls
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
    
    def SetWalls(self, walls):
        self.walls = walls

    def move(self, dx, dy):
        
        # Bouge chaque axes séparéments. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy
 
        # If you collide with a wall, move out based on velocity
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos, walls):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

class Lab(object):

    def Calc_sizes(self):
        """Prend en paramètre une grille
        et calcule la taille de la fenètre (pixel)
        et la taille des block (mur)"""
        l = len(self.level[0])
        h = len(self.level)

        #TODO: condition si trop grand (réduire taille des block)
        self.block_size = 16
        self.fn_size = (l*16, h*16)

    def __init__(self, grille : list, speed = 2) -> None:
        # Initialisation de pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        # const vistesse
        self.speed = speed

        #calcule de la taille de la fenetre et des blocs
        self.level = grille
        self.Calc_sizes()

        # Création de la fenetre
        pygame.display.set_caption("Get to the red square!")
        self.screen = pygame.display.set_mode(self.fn_size)
        
        self.clock = pygame.time.Clock()
        self.walls = [] # Liste des murs


        # Ajout des murs depuis la grille
        lg = self.block_size
        x = y = 0
        for row in self.level:
            for col in row:
                if col == "W":
                    Wall((x, y), self.walls)
                elif col == "E":
                    self.end_rect = pygame.Rect(x, y, lg, lg)
                elif col == "S":
                    self.player_pos = (x,y)
                x += lg
            y += lg
            x = 0

        self.player = Player(self.walls, self.player_pos) # Create the player
        
    def Stop(self):
        self.running = False
    
    def Start(self):
        #TODO : threat avec Lab.Run()
        pass
    
    def Run(self):
        self.running = True
        while self.running:
            
            self.clock.tick(60)
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
        
            # Move the player if an arrow key is pressed
            key = pygame.key.get_pressed()
            # self.player.SetWalls(self.walls)
            s = self.speed
            #TODO: mode de déplacement par bloc (speed = block_size + realese key pour faire un autre mouv)
            if key[pygame.K_LEFT]:
                self.player.move(-s, 0)
            if key[pygame.K_RIGHT]:
                self.player.move(s, 0)
            if key[pygame.K_UP]:
                self.player.move(0, -s)
            if key[pygame.K_DOWN]:
                self.player.move(0, s)
            
        
            # Just added this to make it slightly fun ;)
            if self.player.rect.colliderect(self.end_rect):
                pygame.quit()
                sys.exit()
        
            # Draw the scene
            self.screen.fill((0, 0, 0))
            for wall in self.walls:
                pygame.draw.rect(self.screen, (255, 255, 255), wall.rect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.end_rect)
            pygame.draw.rect(self.screen, (255, 200, 0), self.player.rect)
            # gfxdraw.filled_circle(self.screen, 255, 200, 5, (0,128,0))
            pygame.display.flip()
            self.clock.tick(360)
        pygame.quit()


    
if __name__ == '__main__':
    level = [
        "WWWWWWWWWWWWWWWWWWWW",
        "W                  W",
        "W S       WWWWWW   W",
        "W   WWWW       W   W",
        "W   W        WWWW  W",
        "W WWW  WWWW        W",
        "W   W     W W      W",
        "W   W     W   WWW WW",
        "W   WWW WWW   W W  W",
        "W     W   W   W W  W",
        "WWW   W   WWWWW W  W",
        "W W      WW        W",
        "W W   WWWW   WWW   W",
        "W     W    E   W   W",
        "WWWWWWWWWWWWWWWWWWWW",
    ]
    lab = Lab(level, 16)
    lab.Run()