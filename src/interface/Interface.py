import os
import sys
import pygame


# Class pour le carré orange
class Player(object):
    
    def __init__(self, walls, pos, size):
        self.walls = walls

        self.rect = pygame.Rect(pos[0], pos[1], size, size)
    
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
    
    def __init__(self, pos, walls, size):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], size, size)

class Lab(object):


    def __init__(self, grille : list, speed = 2) -> None:
        self.player_pos = None # si la grille ne contient pas "S"
        self.moving = False
        # Initialisation de pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        # const vistesse
        self.speed = speed

        #calcule de la taille de la fenetre et des blocs
        self.level = grille
        self.Calc_sizes()

        # Création de la fenetre
        pygame.display.set_caption("Trouve la sortie !")
        self.screen = pygame.display.set_mode(self.fn_size)
        
        self.clock = pygame.time.Clock()
        self.walls = [] # Liste des murs


        # Ajout des murs depuis la grille
        lg = self.block_size
        x = y = 0
        for row in self.level:
            for col in row:
                if col == "W":
                    Wall((x, y), self.walls, self.block_size)
                elif col == "E":
                    self.end_rect = pygame.Rect(x, y, lg, lg)
                elif col == "S":
                    self.player_pos = (x,y)
                x += lg
            y += lg
            x = 0
        
        #pos par défaut du joueur
        if self.player_pos == None:
            x = y = 0
            for row in self.level:
                for col in row:
                    if col == " ":
                        self.player_pos = (x,y)
                        break
                    x += lg
                if self.player_pos != None:
                    break
                y += lg
                x = 0

        self.player = Player(self.walls, self.player_pos, self.player_size) # Create the player
        
    def Calc_sizes(self):
        """Prend en paramètre une grille
        et calcule la taille de la fenètre (pixel)
        et la taille des block (mur)"""
        l = len(self.level[0])
        h = len(self.level)

        #TODO: condition si trop grand (réduire taille des block)
        if l > 100 or h > 50:
            self.block_size = 8
            self.fn_size = (l*8, h*8)
            self.player_size = 8
            self.speed /= 2
        else:
            self.block_size = 16
            self.fn_size = (l*16, h*16)
            self.player_size = 16

        self.mode_deplacement_par_bloc = self.block_size == self.speed
        
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
            
            #Deplacements
            self.Move()
            
            # Draw the scene
            self.screen.fill((0, 0, 0))
            for wall in self.walls:
                pygame.draw.rect(self.screen, (255, 255, 255), wall.rect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.end_rect)
            pygame.draw.rect(self.screen, (255, 200, 0), self.player.rect)
            # gfxdraw.filled_circle(self.screen, 255, 200, 5, (0,128,0))
            pygame.display.flip()
            self.clock.tick(360)


            # lorsque le joueur trouve la fin
            if self.player.rect.colliderect(self.end_rect):
                pygame.quit()
                #TODO: fin du lab
        pygame.quit()

    def Move(self):
        s = self.speed
        key = pygame.key.get_pressed()
        if not self.mode_deplacement_par_bloc:
            if key[pygame.K_LEFT]:
                self.player.move(-s, 0)
            if key[pygame.K_RIGHT]:
                self.player.move(s, 0)
            if key[pygame.K_UP]:
                self.player.move(0, -s)
            if key[pygame.K_DOWN]:
                self.player.move(0, s)
        else:
            if self.moving == True:
                if key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_UP] or key[pygame.K_DOWN]:
                    return
                self.moving = False
                return

            if key[pygame.K_LEFT]:
                self.player.move(-s, 0)
            elif key[pygame.K_RIGHT]:
                self.player.move(s, 0)
            elif key[pygame.K_UP]:
                self.player.move(0, -s)
            elif key[pygame.K_DOWN]:
                self.player.move(0, s)
            if key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_UP] or key[pygame.K_DOWN]:
                self.moving = True


    
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
    # level = ["W"*100] + ["W"+"S"+" "*97+"W"] + ["W"+" "*98+"W"]*46 + ["W" + "E" + " "*97 + "W"] + ["W"*100]
    # level = ["W"*120] + ["W"+"S"+" "*117+"W"] + ["W"+" "*118+"W"]*46 + ["W" + "E" + " "*117 + "W"] + ["W"*120]
    lab = Lab(level, 1)
    lab.Run()