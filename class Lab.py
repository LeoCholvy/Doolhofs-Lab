from random import randint

class Genere_Labyrinthe:
    def __init__(self, width, length):
        self.length = length
        self.width = width
    
    def create_blank_maze(self):
        return [[0 for i in range(0,self.width)] for j in range(0,self.length)]
    
    def create_wall_maze(self, maze):
        for i in range(1,self.length-1, 2):
            for j in range(1,self.width-1, 2):
                maze[j][i] = 1
        for i in range(1,self.length-1, 2):
            for j in range(1,self.width-1, 2):
                pass
    
    def infect_1(self,i,j, maze):
        forbid_y, forbid_x = [1, len(maze)-1], [1, len(maze[0])-1]
        if i in forbid_x:
            pass
        elif j in forbid_y:
            pass
        else:
            pxy = [randint(-1,1), randint(-1,1)]
            try:
                maze[j+pxy[1]][i+pxy[0]]
            except maze[j+pxy[1]][i+pxy[0]]==1:
                self.infect_1(i,j,maze)




    def place_spawn(self):
        return 0
    def place_end(self):
        return 0
    
maze_creator = Genere_Labyrinthe(17,17)
maze = maze_creator.create_blank_maze()
maze_creator.create_wall_maze(maze)
maze_creator.infect_1(16,14,maze)
