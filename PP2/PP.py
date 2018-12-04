import mapping
import copy
import time
import pygame, os 

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,50"
          
def main():
    pygame.init()
    pygame.display.set_caption('Path Planning')

    
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
    
    #Display the PP window
    surface = pygame.display.set_mode((WIDTH,HEIGHT))    

    # draw the map
    map.draw(surface, square)
    pygame.display.flip()

    while True:
        time.sleep(1)
        #perform A* for each robot
        for i in range(len(map.robots)):  
            possibleMoves = []
            visited = []
            possibleMoves.append(map.robots[i])
            found = False
            #main A* while loop
            while len(possibleMoves) > 0:
                time.sleep(.01)
                #find the best looking node to expand
                currentNode = possibleMoves[0]
                currentNodeCost = currentNode.pathCost +  ((currentNode.position[0] - map.goal[0]) ** 2) + ((currentNode.position[1] - map.goal[1]) ** 2)
                currentIndex = 0
                for index, item in enumerate(possibleMoves):
                    itemCost = item.pathCost +  ((item.position[0] - map.goal[0]) ** 2) + ((item.position[1] - map.goal[1]) ** 2)
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
                        time.sleep(.01)
                        map.draw(surface, square)
                        pygame.display.flip()
                        break
                    print("appending: ", nodePosition)
                    if nodePosition not in visited:
                        possibleMoves.append(mapping.Node(nodePosition, currentNode))
                if found:
                    break
            if not found:
                print("queue emptied")
            found = False
        break
    while True:
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop
    pygame.quit()
    data.close()

if __name__ == "__main__": main()
