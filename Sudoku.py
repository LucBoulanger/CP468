from collections import deque

class SudokuCSP():
    '''
        domain = dictionary where Key = (x, y), Value = [domain]
        arcs   = dictionary where Key = (x, y), Value = [Neighbors...]
    '''
    def __init__(self, file):
        self.domain = {}
        self.arcs = {}
        x = 0
        y = 0
        for line in file:
            for char in line:
                if char != "\n":
                    self.arcs[(x,y)] = []
                    if char == "*":
                        self.domain[(x,y)] = [1,2,3,4,5,6,7,8,9]
                    else:
                        self.domain[(x,y)] = [int(char)]
                y += 1
            x += 1
            y = 0
        self.populateArcs()    
        return    
    
    '''
    Initial list of all possible arcs.
    Arcs are expressed as dictionary where Key = (x, y), Value = [Neighbors...]
        - thus all values in the sudoku puzzle are given arcs to their neighbors
        - this is used to gather all neighbors of a given value when needed.
    '''
    def populateArcs(self):
        for key in self.arcs:
            for i in range(0,9):
                for j in range(0,9):
                    if (i != key[0] or j != key[1]) and (i == key[0] or j == key[1] or (i in range((key[0]//3)*3,(key[0]//3)*3+3) and j in range((key[1]//3)*3,(key[1]//3)*3+3))):
                        # clears some unnecessary arcs that don't need to be checked as they are already established 
                        if not (len(self.domain[key]) == 1 and len(self.domain[(i,j)]) == 1):
                            self.arcs[key].append((i,j))
                        elif self.domain[key][0] == self.domain[(i,j)][0]:
                            print("Invalid sudoku puzzle, exiting program.")
                            exit()
        total = 0
        for key in self.arcs: 
            self.arcs[key] = list(set(self.arcs[key]))
        for key in self.arcs:
            total += len(self.arcs[key])
        
        print(total)
        return  
        
    '''
    Since all constraints are between two integers, 
    I think we can just define this function to 
    compare them.
    Anytime you need to check constraints on two 
    variables, just send the arc here.
    '''
    def constraintCheck(self, Xi, Xj):
        return Xi != Xj
      
    '''
    Prints domains, for debugging
    '''
    def printDomain(self):
        for key in self.domain:
            print("{} -> {}".format(key, self.domain[key]))
        return
      
    def isSolved(self):
        for key in self.domain:
            if len(self.domain[key]) != 1:
                return False
        return True
    
    '''
    Prints the current sudoku problem by the values
    in the familiar sudoku format.
    ''' 
    def __str__(self):
        s = ""
        count = 0
        rows = 0
        for key in self.domain:
            if (rows == 0 or rows == 3 or rows == 6) and count == 0:
                s += "-------------\n"
            if count == 0 or count == 3 or count == 6:
                s += "|"
            if len(self.domain[key]) == 1:
                s += str(self.domain[key][0])
            else:
                s += "*"
            count += 1
            if count == 9:
                s += "|\n"
                rows += 1
                count = 0
        return s + "-------------\n"

'''
Main AC-3 algorithm. 
Returns True or False dependent upon whether the algorithm failed or not.
'''        
def AC3_Main(csp):   
    #initiate a queue to store all current arcs
    queue = deque()
    for key in csp.arcs:
        for neighbor in csp.arcs[key]:
            queue.append((key, neighbor))
    
    #iterate through queue until it isnt empty
    while queue:
        #print("Queue length: {}".format(len(queue)))
        i,j = queue.popleft()
        if AC3_Revise(csp, i,j):
            if len(csp.domain[i]) == 0:
                return False
            for key in csp.arcs[i]:
                queue.append((key, i))
    return True
    
def AC3_Revise(csp, i, j):
    revised = False
    tbr = []         #to be removed
    for x in csp.domain[i]:
        valid = False
        for y in csp.domain[j]:
            if csp.constraintCheck(x,y):
                valid = True
        if not valid:
            tbr.append(x)
            revised = True
    if revised:
        for x in tbr:
            csp.domain[i].remove(x)
    return revised
        
        

fileName = input("Which sudoku file to open? ")
        
sudoku = SudokuCSP(open("data/"+fileName, "r"))
print("---------------------------\nCurrent Sudoku Problem: \n---------------------------")
print(sudoku)
print("Sudoku solved? {}\n".format(sudoku.isSolved()))
if not sudoku.isSolved():
    print("Attempting AC-3 Algorithm...")
    if not AC3_Main(sudoku):
        print("Could not solve sudoku, one or more domain became empty.\n")
    else:
        ("Sudoku solved? {}\n".format(sudoku.isSolved()))
        print(sudoku)
#print("---------------------------\nDomain for each Variable: \n---------------------------")
#sudoku.printDomain()
print()