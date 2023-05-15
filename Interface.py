import os
import sys
import pygame


# Class pour le carré orange
class Player(object):
    
    def __init__(self, walls):
        self.walls = walls
        self.rect = pygame.Rect(32, 32, 16, 16)
    
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

    def __init__(self, grille : list) -> None:
        # Initialise pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        # Set up the display
        pygame.display.set_caption("Get to the red square!")
        self.screen = pygame.display.set_mode((320, 240))
        
        self.clock = pygame.time.Clock()
        self.walls = [] # List to hold the walls

        self.level = grille

        # Parse the level string above. W = wall, E = exit
        self.x = self.y = 0
        for row in self.level:
            for col in row:
                if col == "W":
                    Wall((self.x, self.y), self.walls)
                if col == "E":
                    self.end_rect = pygame.Rect(self.x, self.y, 16, 16)
                self.x += 16
            self.y += 16
            self.x = 0

        self.player = Player(self.walls) # Create the player
        
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
            if key[pygame.K_LEFT]:
                self.player.move(-2, 0)
            if key[pygame.K_RIGHT]:
                self.player.move(2, 0)
            if key[pygame.K_UP]:
                self.player.move(0, -2)
            if key[pygame.K_DOWN]:
                self.player.move(0, 2)
            #FIXME: créer const speed
            
        
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
        "WWWWWWWWWWWWWWWWWWWWW",
        "W                  WW",
        "W         WWWWWW   WW",
        "W   WWWW       W   WW",
        "W   W        WWWW  WW",
        "W WWW  WWWW        WW",
        "W   W     W W      WW",
        "W   W     W   WWW WWW",
        "W   WWW WWW   W W  WW",
        "W     W   W   W W  WW",
        "WWW   W   WWWWW W  WW",
        "W W      WW        WW",
        "W W   WWWW   WWW   WW",
        "W     W    E   W   WW",
        "WWWWWWWWWWWWWWWWWWWWW",
    ]
    lab = Lab(level)
    lab.Run()