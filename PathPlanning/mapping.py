import numpy as np

class Map():
    '''
        dimensions -> [x, y] as a list containing the width (x) and the height (y) of the map.
        robots     -> [[x,y], [x,y]] as a list of starting coordinate pairs [x, y] of all 
                      robots in the map.
        goal       -> [x, y] as a list containing the coordinate pair representing the goal 
                      location.
        map        -> [[]] as the two dimensional list containing map information. 
                      if map[x][y] == 1: map[x][y] contains an obstruction.
                      if map[x][y] == 0: map[x][y] is a free space. 
    '''
    def __init__(self, file):
        self.dimensions = [int(i) for i in file.readline().split(" ")]          
        self.robots = [[int(char) for char in file.readline().split(" ")] for i in range(int(file.readline()))]
        self.goal = [int(i) for i in file.readline().split(" ")]
        self.map = [[int(char) for char in line if char != '\n'] for line in file]
    
    def printDetails(self):
        print(self.dimensions)
        print(self.robots)
        print(self.goal)
        print(np.matrix(self.map))