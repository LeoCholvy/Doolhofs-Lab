import random
walls = 'W'
paths = ' '
class Maze:
    def __init__(self, width=20, length=20):
        assert width>=1 and length>=1
        self.length, self. width = length, width
        
        self.cmaze = [[Cell(x,y) for x in range(length)] for y in range(width)]
        
        self.current = self.cmaze[0][0] 
        self.stack = []
        
        self.generate_maze()
        self.fmaze = self.make_maze()

    def remove_wall(self, choice):
        
        if choice.x > self.current.x:
            self.current.walls['right'] = False
            choice.walls['left'] = False
        
        elif choice.x < self.current.x:
            self.current.walls['left'] = False
            choice.walls['right'] = False
        
        elif choice.y > self.current.y:
            self.current.walls['bottom'] = False
            choice.walls['top'] = False
        
        elif choice.y < self.current.y:
            self.current.walls['top'] = False
            choice.walls['bottom'] = False

    def draw_walls(self, fmaze):
        for yindex, y in enumerate(self.cmaze):
            for xindex, x in enumerate(y):
                for i, e in enumerate(x.walls):
                    if i==3 and x.walls[e]:
                        fmaze[yindex*2+1][xindex*2] = walls
                    if i==2 and x.walls[e]:
                        fmaze[yindex*2+1][xindex*2+2] = walls
                    if i==0 and x.walls[e]:
                        fmaze[yindex*2][xindex*2+1] = walls
                    if i==1 and x.walls[e]:
                        fmaze[yindex*2+2][xindex*2+1] = walls
        return fmaze
    
    def draw_borders(self, fmaze):
        length = len(self.cmaze)
        for row in self.cmaze:
            row[0] = row[length-1] = walls
        
        self.cmaze[0] = self.cmaze[length-1] = walls * length
        return fmaze
                    
                        
    def generate_maze(self):
        while True:
                self.current.visited = True
                children = self.current.get_child(self.cmaze)
                if children:
                    choice = random.choice(children)
                    choice.visited = True
                    
                    self.stack.append(self.current)

                    self.remove_wall(choice)
                    
                    self.current = choice
                
                elif self.stack:
                    
                    self.current = self.stack.pop()
                
                else:
                
                    break

    
    def make_maze(self):
        fmaze = []
        length = len(self.cmaze)*2+1

        for x in range(length):
            if x%2 == 0:
                fmaze.append([paths if x%2 != 0 else walls for x in range(length)])
            else:
                fmaze.append([paths] * length)

        fmaze = self.draw_walls(fmaze)
        fmaze = self.draw_borders(fmaze)
        return self.assemble_maze(fmaze)

        
    def assemble_maze(self, fmaze):
        self.choose_entrance(fmaze)
        self.choose_exit(fmaze)

        for i in fmaze:
            fmaze[fmaze.index(i)] = ''.join(i)
        return fmaze
    
    def choose_entrance(self, fmaze):
        length = len(fmaze)
        width = len(fmaze[0])
        choicey = random.randint(1, length-1)
        choicex = random.randint(1, width-1)
        if fmaze[choicey][choicex] == ' ':
            fmaze[choicey][choicex] = 'S' 
        else: 
            self.choose_entrance(fmaze)



    def choose_exit(self, fmaze):
        length = len(fmaze)
        width = len(fmaze[0])
        choicey = random.randint(1, length-1)
        choicex = random.randint(1, width-1)
        if fmaze[choicey][choicex] == ' ':
            fmaze[choicey][choicex] = 'E'  
        else: 
            self.choose_exit(fmaze)

    def Get_fmaze(self):
        return self.fmaze

    

        
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x,y
        self.walls = {'top':True, 'bottom':True, 'right': True, 'left':True}
        self.visited = False
    
    def get_child(self, maze):
        neighbours = [(1, 0), (-1,0), (0, 1), (0, -1)]
        children = []
        for x, y in neighbours:
            if self.x+x in [len(maze), -1] or self.y+y in [-1, len(maze)]:
                continue
            child = maze[self.y+y][self.x+x]
            if child.visited:
                continue
            children.append(child)
        return children