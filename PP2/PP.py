import mapping
import copy
import pygame
import math
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,50"
          
def main():
    #pygame initialization stuff
    pygame.init()
    pygame.display.set_caption('Path Planning')

    WHITE = ( 255, 255, 255)
    
    
    HEIGHT = pygame.display.Info().current_h - 100
    WIDTH  = pygame.display.Info().current_w - 100
    SQ_SIZE = 0

    #retrieve map information from file
    filename = input("Enter filename: ")
    data  = open("data/"+filename, "r")
    paths = open("paths/"+filename, "w")
    map = mapping.Map(data)
    map.printDetails()
    DRAW_DURING = False
    inputting = input("Draw path during algorithm? ")
    if inputting[0] == 'y' or inputting[0] == "Y":
        DRAW_DURING = True
    QUIT = False

    #more pygame initialization
    square = HEIGHT // len(map.map)
    WIDTH = square * len(map.map[0])
    HEIGHT = square * len(map.map)
    
    if square < 5:
        square = 5
        HEIGHT = pygame.display.Info().current_h - 100
        WIDTH  = pygame.display.Info().current_w - 100 
    
    #Display the PP window
    surface = pygame.display.set_mode((WIDTH,HEIGHT))    
    
    # draw the map
    map.draw(surface, square)
    pygame.display.flip()

    #perform A* for each robot
    for i in range(len(map.robots)):  
        #intialization of A star variables
        print("Working on robot ", i)
        print("Working on robot ", i, file=paths)
        beginning = copy.deepcopy(map.robots[i])
        possibleMoves = []
        visited = []
        found = False
        
        #initialize array of visited locations (2D array for fast lookup)
        for j in range(map.dimensions[0]):
            visited.append([])
            for k in range(map.dimensions[1]):
                visited[j].append(0)
        #insert robot starting position into queue
        possibleMoves.append(map.robots[i])
        
        #main A* while loop
        while len(possibleMoves) > 0:
            #quit the program if the user wants to
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QUIT = True
                    break
            if QUIT:
                break
            
            #find the best looking node to expand
            currentNode = possibleMoves[0]
            #current node cost = current path cost (g(n)) + 1.001* manhatten distance (h(n))
            currentNodeCost = currentNode.pathCost + 1.001*(abs(currentNode.position[0] - map.goal[0]) + abs(currentNode.position[1] - map.goal[1]))
            currentIndex = 0
            #iterate through queue and find lowest cost
            for index, item in enumerate(possibleMoves):
                itemCost = item.pathCost +  1.001*(abs(item.position[0] - map.goal[0]) + abs(item.position[1] - map.goal[1]))
                if itemCost < currentNodeCost:
                    currentNode = item
                    currentNodeCost = itemCost
                    currentIndex = index
            #retrieve the lowest cost Node, this is where we move the robot to
            currentNode = possibleMoves.pop(currentIndex)
            #set the chosen node as visited 
            visited[currentNode.position[0]][currentNode.position[1]] = 1
            #update the robots position
            map.robots[i] = currentNode
            #if set up, draw to screen
            if DRAW_DURING:
                map.draw(surface, square)
                pygame.display.flip()
            #expand the nodes neighbors
            for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nodePosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])
                #don't include if out of range
                if nodePosition[0] < 0 or nodePosition[0] >= len(map.map[0]):                   
                    continue
                if nodePosition[1] < 0 or nodePosition[1] >= len(map.map):
                    continue
                #also dont include if path is an obstacle
                if map.map[nodePosition[1]][nodePosition[0]] == 1:
                    continue
                #check if goal node
                if nodePosition[0] == map.goal[0] and nodePosition[1] == map.goal[1]:
                    #if goal node, update robot position again and exit A star
                    map.robots[i] = mapping.Node(nodePosition, currentNode)
                    found = True
                    break
                #if square not already visited, set square to visited.
                if visited[nodePosition[0]][nodePosition[1]] == 0:
                    visited[nodePosition[0]][nodePosition[1]] = 1
                    if i == 0:
                        map.visited.append(nodePosition)
                    #add new node to  queue
                    possibleMoves.append(mapping.Node(nodePosition, currentNode))
            if found:
                break
        if QUIT:
            break
        if not found:
            # if the queue is empty but no solution has been found, reset the robot as the goal node is unreachable
            map.robots[i] = beginning
            print("queue emptied")
            print("queue emptied", file=paths)
        # print out path of robot
        path = []
        pos = map.robots[i]
        while pos is not None:
            yCorrected = (pos.position[0],map.dimensions[1] - 1 - pos.position[1])
            path.append(yCorrected)
            pos = pos.child
            
        for i in range(len(path) - 1, 0, -1):
            print(path[i], end=" -> ")
            print(path[i], end=" -> ",file=paths)
        print(path[0])
        print(path[0],file = paths)
        
    #draw map when done
    while not QUIT:
        surface.fill(WHITE)
        map.draw(surface, square)
        pygame.display.flip()
        
        for ev in pygame.event.get():   # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                QUIT = True             #   ... leave game loop
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT:
                    map.offsetX -= 1
                if ev.key == pygame.K_RIGHT:
                    map.offsetX += 1
                if ev.key == pygame.K_UP:
                    map.offsetY -= 1
                if ev.key == pygame.K_DOWN:
                    map.offsetY += 1
    
    #save rendered map as a .PNG in the /img folder
    newWidth = square*map.dimensions[0]
    newHeight = square*map.dimensions[1]
    newsurface = pygame.display.set_mode((newWidth,newHeight))    
    map.draw(newsurface, square)
    pygame.image.save(newsurface, "img/"+filename+".PNG")
    pygame.quit()
    data.close()
    paths.close()

if __name__ == "__main__": main()
