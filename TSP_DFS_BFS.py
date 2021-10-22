import os
import sys
import math
from math import inf
from time import sleep

# Node structure to hold the cities
class Node:
    def __init__(self, index, x, y):
        # Holds the city number.
        self.index = index
        
        # Holds the city location.
        self.x = x
        self.y = y
        # Array to hold all the possible paths from this node.
        self.pathList = []


# Takes the list of city nodes and the map of connected cities. Replace the 'X' with the correct city
# then remove all 'None's from the list. This creates a map for the edges.
def BuildCityPath(nodeList, cityMap):
    for i in range(len(cityMap)):
        for j in range(len(cityMap[i])):
            if(cityMap[i][j] != None):
                cityMap[i][j] = nodeList[j]
        cityMap[i] = list(filter(lambda x: x != None, cityMap[i]))
    return cityMap


# DFS 
def DFS(node, cityMap):
    bestPath = []
    output = (inf, [])
    # Queue to hold the continuations
    queue = []
    # Append a tuple that has the current node, path taken, and distance traveled
    queue.append((node, [node], 0))
    # Loop while the path queue is not empty
    while queue:
        # Unpack the tuple
        tempNode, tempArray, distanceTraveled = queue.pop()
        # If the distance traveled in this path is longer than the final path
        # then continue to avoid this path in the future
        if(distanceTraveled > output[0]):
            continue
        # If the tempNode index is 11 the algorithm reached the end of the path.
        # If the  distance traveled is shorter than the recorded output reassign output.
        if(tempNode.index == 11 and distanceTraveled < output[0]):
            bestPath = tempArray
            output = (distanceTraveled, tempArray)
            continue
        if tempNode.pathList == []:
            tempNode.pathList = cityMap[tempNode.index-1]
        # Add every continuation to the path queue
        for path in tempNode.pathList:
            queue.append((path,tempArray + [path], distanceTraveled + CalculateDistance(path, tempNode)))
    # When the queue is empty we have the shortest path.
    return output


# BFS algorithm using iteration. I used iteration here because it is easier and my other code would have taken more
# time to change to do BFS than writing new code.
def BFS(node):
    bestPath = []
    output = (inf, [])
    # Queue to hold the continuations
    queue = []
    # Append a tuple that has the current node, path taken, and distance traveled
    queue.append((node, [node], 0))
    # Loop while the path queue is not empty
    while queue:
        # Unpack the tuple
        tempNode, tempArray, distanceTraveled = queue.pop(0)
        # If the distance traveled in this path is longer than the final path
        # then continue to avoid this path in the future
        if(distanceTraveled > output[0]):
            continue
        # If the tempNode index is 11 the algorithm reached the end of the path.
        # If the  distance traveled is shorter than the recorded output reassign output.
        if(tempNode.index == 11 and distanceTraveled < output[0]):
            bestPath = tempArray
            output = (distanceTraveled, tempArray)
            continue
        # Add every continuation to the path queue
        for path in tempNode.pathList:
            queue.append((path,tempArray + [path], distanceTraveled + CalculateDistance(path, tempNode)))

    # When the queue is empty we have the shortest path.
    return output


# Calculates the distance between two given cities.
def CalculateDistance(nodeFrom, nodeTo):
    return math.sqrt((float(nodeTo.x)-float(nodeFrom.x))**2 + (float(nodeTo.y)-float(nodeFrom.y))**2)

# Driver.
cityList = []
def Driver():
    # Get location of the file. Should be placed in the same file as python script.
    _location = os.path.join(sys.path[0], "11PointDFSBFS.tsp")
    read = False

    # Open file
    with open(_location, 'r') as inputFile:
        # Loop over each line in input file
        for line in inputFile:
            # If you have reached the section to read run
            if(read == True):
                # split the line into the index, x, and y values
                lineContent = line.split(' ')
                # Add cities to the citylist
                cityList.append(Node(int(lineContent[0]), float(lineContent[1]), float(lineContent[2])))
                # cityList.append(Node(int(lineContent[0]), lineContent[1], lineContent[2]))
                # Continue so it doesn't have to do the next if statement.
                continue

            # Else check if the current line is the section header. If true set read to true
            if('NODE_COORD_SECTION' == line.strip('\n')):
                read = True
    
    # Map to hold the connections between cities
    cityMap = [[None, 'X', 'X', 'X', None, None, None, None, None, None, None],
            [None, None, 'X', None, None, None, None, None, None, None, None],
            [None, None, None, 'X', 'X', None, None, None, None, None, None],
            [None, None, None, None, 'X', 'X', 'X', None, None, None, None],
            [None, None, None, None, None, None, 'X', 'X', None, None, None],
            [None, None, None, None, None, None, None, 'X', None, None, None],
            [None, None, None, None, None, None, None, None, 'X', 'X', None],
            [None, None, None, None, None, None, None, None, 'X', 'X', 'X'],
            [None, None, None, None, None, None, None, None, None, None, 'X'],
            [None, None, None, None, None, None, None, None, None, None, 'X']]
    # Build the map
    cityMap = BuildCityPath(cityList, cityMap)
    # Initialize the pathlist for DFS
    cityList[0].pathList = cityMap[0]

    # Run DFS
    output = DFS(cityList[0], cityMap)
    # Cast the city numbers to strings to that I can join them and concatenate them to a string.
    output = (output[0], [str(city.index) for city in output[1]])
    print("Shortest Path: " + '->'.join(output[1]) + " with a distance of " + str(round(output[0], 3)))

    output = BFS(cityList[0])
    output = (output[0], [str(city.index) for city in output[1]])
    print("Shortest Path: " + '->'.join(output[1]) + " with a distance of " + str(round(output[0], 3)))
            

def main():
    Driver()

if __name__ == '__main__':
    main()