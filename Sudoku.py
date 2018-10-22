class Sudoku():
    '''
        - self.domain -> 3d list with [row][col][domain for variable[row][col]]
        - self.values -> 2d array of current sudoku values. 
                         if [row][col] == "*", then no number placed there, 
                         if [row][col] == (some int), then domain[row][col] = [(some int)] 
        - self.constraints -> tbd
    '''
    def __init__(self, file):
        self.domain = []
        self.values = []
        row = 0
        for line in file:
            self.domain.append([])
            self.values.append([])
            for char in line:
                if char != "\n":
                    self.values[row].append(char)
                    if char == "*":
                        self.domain[row].append([1,2,3,4,5,6,7,8,9])
                    else:
                        self.domain[row].append([int(char)])
            row += 1
            
    def printDomain(self):
        for i in range (0,9):
            for j in range (0,9):
                print(self.domain[i][j], end="")
            print()
            
    def __str__(self):
        s = ""
        for i in range (0,9):
            s += "|"
            for j in range(0,9):
                s+= self.values[i][j] + "|"
            s += "\n"
        return s
sudoku = Sudoku(open("data\Testing1.txt", "r"))
print("---------------------------\nCurrent Sudoku Problem: \n---------------------------")
print(sudoku)
print("---------------------------\nDomain for each Variable: \n---------------------------")
sudoku.printDomain()
