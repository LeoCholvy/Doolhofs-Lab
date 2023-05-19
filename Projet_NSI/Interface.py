import os
import sys
import pygame
from maze_generator import Maze
from test_cam import CameraGroup

DEFAULT_CONFIG = {"speed": 2}

# Class pour le carré orange
class Player(pygame.sprite.Sprite):
    
    def __init__(self, walls, pos, size, group):
        super().__init__(group)
        self.walls = walls
        self.image = pygame.image.load('graphismes/joueur.png')
        self.image = pygame.transform.scale(self.image,(size,size))
        self.pos = pos

        self.rect = self.image.get_rect()
        self.rect.move_ip(pos[0], pos[1])
        #self.rect = pygame.Rect(pos[0], pos[1], size, size)
    
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
class Wall(pygame.sprite.Sprite):
    
    def __init__(self, pos, walls, size,group):
        super().__init__(group)
        self.pos = pos
        walls.append(self)
        self.image = pygame.image.load('graphismes/bloc_wall_maze.png')
        self.image = pygame.transform.scale(self.image, (size,size))
        self.rect = pygame.Rect(pos[0], pos[1], size, size)

class End(pygame.sprite.Sprite):

    def __init__(self, pos, size, group):
        super().__init__(group)
        self.pos = pos
        self.image = pygame.image.load('graphismes/arrivee.png')
        self.image = pygame.transform.scale(self.image,(size, size))
        self.rect = pygame.Rect(pos[0], pos[1], size, size)

class Lab(object):


    def __init__(self, grille : list) -> None:
        self.player_pos = None # si la grille ne contient pas "S"
        self.moving = False
        # Initialisation de pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        config = Get_config()
        # const vistesse
        self.speed = config["speed"]

        #calcule de la taille de la fenetre et des blocs
        self.level = grille
        self.Calc_sizes()

        # Création de la fenetre
        pygame.display.set_caption("Trouve la sortie !")
        self.screen = pygame.display.set_mode(self.fn_size)
        self.surface = pygame.display.get_surface()
        
        self.clock = pygame.time.Clock()
        self.walls = [] # Liste des murs


    def ajout_mur(self):
        # Ajout des murs depuis la grille
        lg = self.block_size
        x = y = 0
        for row in self.level:
            for col in row:
                if col == "W":
                    Wall((x, y), self.walls, self.block_size,camera_group)
                elif col == "E":
                    self.end = End([x,y], lg, camera_group)
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

        self.player = Player(self.walls, self.player_pos, self.player_size, camera_group) # Create the player
        
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
            self.screen.fill((50, 0, 255))
            #for wall in self.walls:
                #pygame.draw.rect(self.screen, (255, 255, 255), wall.rect)
                #self.screen.blit(wall.image, (wall.pos[0], wall.pos[1]))
                
            #pygame.draw.rect(self.screen, (255, 0, 0), self.end_rect)
            #self.screen.blit(self.player.image, self.player.rect)
            #pygame.draw.rect(self.screen, (255, 200, 0), self.player.rect)
            # gfxdraw.filled_circle(self.screen, 255, 200, 5, (0,128,0))
            camera_group.update()
            camera_group.custom_draw()
            pygame.display.flip()
            self.clock.tick(360)


            # lorsque le joueur trouve la fin
            if self.player.rect.colliderect(self.end.rect):
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
        camera_group.offset.x = camera_group.camera_rect.left - camera_group.camera_borders['left']
        camera_group.offset.y = camera_group.camera_rect.top - camera_group.camera_borders['top']

def Get_config():
    try:
        #lire fichier de config
        f = open('config.txt','r')
        texte = f.read()
        texte = [x.split("=") for x in texte.replace(" ", "").split("\n") if not x[0] == '#']
        config = {i:eval(j) for i,j in texte}
        f.close()

        #verification des valeurs
        if not(isinstance(config["speed"], int) or isinstance(config["speed"], float)):
            Write_config()
            return DEFAULT_CONFIG
        return config

    except:
        #sinon on créer un fichier de config
        Write_config()
        return DEFAULT_CONFIG
def Write_config():
    f = open("config.txt", 'w')
    f.write(
        "#Recommende: 2,4,8,16 (16=deplacement par case)\n"+
        "speed = 2"
    )
    f.close()
    
if __name__ == '__main__':
    maze = Maze(13,13)
    level = maze.fmaze
    # level = ["W"*100] + ["W"+"S"+" "*97+"W"] + ["W"+" "*98+"W"]*46 + ["W" + "E" + " "*97 + "W"] + ["W"*100]
    # level = ["W"*120] + ["W"+"S"+" "*117+"W"] + ["W"+" "*118+"W"]*46 + ["W" + "E" + " "*117 + "W"] + ["W"*120]
    lab = Lab(level)
    camera_group = CameraGroup()
    lab.ajout_mur()
    lab.Run()