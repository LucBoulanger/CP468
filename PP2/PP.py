import mapping
import copy
import pygame
import math
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,50"
          
def main():
    pygame.init()
    pygame.display.set_caption('Path Planning')

    WHITE = ( 255, 255, 255)
    
    HEIGHT = pygame.display.Info().current_h - 100
    WIDTH  = pygame.display.Info().current_w - 100
    SQ_SIZE = 0

    filename = input("Enter filename: ")
    data = open("data/"+filename, "r")
    map = mapping.Map(data)
    map.printDetails()

    square = HEIGHT // len(map.map)
    WIDTH = square * len(map.map[0])
    HEIGHT = square * len(map.map)
    
    if square < 10:
        square = 5
        HEIGHT = pygame.display.Info().current_h - 100
        WIDTH  = pygame.display.Info().current_w - 100 
    
    #Display the PP window
    surface = pygame.display.set_mode((WIDTH,HEIGHT))    
    
    # draw the map
    map.draw(surface, square)
    pygame.display.flip()

    while True:
        #perform A* for each robot
        for i in range(len(map.robots)):  
            print("Working on robot ", i)
            beginning = copy.deepcopy(map.robots[i])
            possibleMoves = []
            visited = []
            possibleMoves.append(map.robots[i])
            found = False
            #main A* while loop
            while len(possibleMoves) > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            pygame.quit()
                #find the best looking node to expand
                currentNode = possibleMoves[0]
                currentNodeCost = currentNode.pathCost + 1.1*(abs(currentNode.position[0] - map.goal[0]) + abs(currentNode.position[1] - map.goal[1]))
                currentIndex = 0
                for index, item in enumerate(possibleMoves):
                    itemCost = item.pathCost +  1.001*(abs(item.position[0] - map.goal[0]) + abs(item.position[1] - map.goal[1]))
                    if itemCost < currentNodeCost:
                        currentNode = item
                        currentNodeCost = itemCost
                        currentIndex = index
                #retrieve the current Node, this is where the robot is now
                currentNode = possibleMoves.pop(currentIndex)
                visited.append(currentNode.position)
                map.robots[i] = currentNode
                map.draw(surface, square)
                pygame.display.flip()
                #expand the node
                for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nodePosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])
                    #don't include if out of range
                    if nodePosition[0] < 0 or nodePosition[0] >= len(map.map[0]):                   
                        continue
                    if nodePosition[1] < 0 or nodePosition[1] >= len(map.map):
                        continue
                    if map.map[nodePosition[1]][nodePosition[0]] == 1:
                        continue
                    if nodePosition[0] == map.goal[0] and nodePosition[1] == map.goal[1]:
                        map.robots[i] = mapping.Node(nodePosition, currentNode)
                        found = True
                        #map.draw(surface, square)
                        #pygame.display.flip()
                        break
                    if nodePosition not in visited:
                        visited.append(nodePosition)
                        if i == 0:
                            map.visited.append(nodePosition)
                        possibleMoves.append(mapping.Node(nodePosition, currentNode))
                if found:
                    break
            if not found:
                map.robots[i] = beginning
                print("queue emptied")
            map.draw(surface, square)
            pygame.display.flip()
            found = False
        break
    while True:
        surface.fill(WHITE)
        map.draw(surface, square)
        pygame.display.flip()
        
        for ev in pygame.event.get():   # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                pygame.quit()           #   ... leave game loop
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT:
                    map.offsetX -= 1
                if ev.key == pygame.K_RIGHT:
                    map.offsetX += 1
                if ev.key == pygame.K_UP:
                    map.offsetY -= 1
                if ev.key == pygame.K_DOWN:
                    map.offsetY += 1
    pygame.quit()
    data.close()

if __name__ == "__main__": main()
