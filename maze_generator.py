import random
width = 20
length = 20
mark = '@'
maze = {}
f_maze = []
for y in range(0, width):
    for x in range(0, length):
        maze[(x,y)] = 'W'

def p_maze(maze, MX=None, MY=None):
    for y in range(width):
        for x in range(length):
            if MX == x and MY == y:
                print(mark, end='')
            else:
                print(maze[(x,y)], end='')
            print()
def m_maze(x,y):
    while True:
        unvisitedNeighbors = []
        if y > 1 and (x, y - 2) not in hasVisited:
            unvisitedNeighbors.append('n')

        if y < length - 2 and (x, y + 2) not in hasVisited:
            unvisitedNeighbors.append('s')

        if x > 1 and (x - 2, y) not in hasVisited:
            unvisitedNeighbors.append('o')

        if x < length - 2 and (x + 2, y) not in hasVisited:
            unvisitedNeighbors.append('e')

        if len(unvisitedNeighbors) == 0:
            return
        else:
            nextIntersection = random.choice(unvisitedNeighbors)

            if nextIntersection == 'n':
                nextX = x
                nextY = y - 2
                maze[(x, y - 1)] = ' ' 
            elif nextIntersection == 's':
                nextX = x
                nextY = y + 2
                maze[(x, y + 1)] = ' ' 
            elif nextIntersection == 'o':
                nextX = x - 2
                nextY = y
                maze[(x - 1, y)] = ' ' 
            elif nextIntersection == 'e':
                nextX = x + 2
                nextY = y
                maze[(x + 1, y)] = ' '

            hasVisited.append((nextX, nextY))
            m_maze(nextX, nextY)

hasVisited = [(1,1)]
m_maze(1,1)
def m_fmaze():
    for y in range(length):
        temp_line = []
        for x in range(width):
            temp_line.append(maze[(x,y)])
        line = ''.join(temp_line)
        f_maze.append(line)
m_fmaze()
print(f_maze)
