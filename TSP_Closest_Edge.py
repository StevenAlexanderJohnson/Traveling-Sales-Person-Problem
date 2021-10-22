import os
import sys
import math
import random
import time
from math import sqrt

# Node structure to hold the cities
class Node:
    def __init__(self, index, x, y):
        # Holds the city number.
        self.index = index
        # Holds the city location.
        self.x = x
        self.y = y
        # Holds the next city in the path
        self.next = None


class Graph:
    def __init__(self, node):
        self.root = node
        self.path = [node]
    
    # Inserts the new node in the correct index of the path where each node is 
    # connected to the next node in the list.
    def AddEdge(self, nodeTo):
        # If the length of the list is two or less add the node in order. You require a line segment before
        # the rest of the algorithm is to work.
        if len(self.path) < 3:
            self.path.append(nodeTo)
            if(len(self.path) == 3):
                self.path.append(self.path[0])
            return True
        
        # Used to hold the end points of the line segment.
        closest1 = self.path[0]
        closest2 = self.path[1]
        # Calculate the distance between the new node and the line segment.
        pointDistance = CalculatePointDistance(closest1, closest2, nodeTo)

        # Loop over the path to check possible edges.
        for i in range(0, len(self.path)-1):
            # If the path being checked is already assigned to the closest variables continue.
            if(self.path[i] == closest1 and self.path[i+1] == closest2):
                continue
            # Calculate the distance between the edge and the new node
            testDistance = CalculatePointDistance(self.path[i], self.path[i+1], nodeTo)
            # If the distance between the new node and the line segment is less than the current shortest distance
            # then reassign the closest indexs and distance
            if(testDistance < pointDistance):
                closest1 = self.path[i]
                closest2 = self.path[i+1]
                pointDistance = testDistance
            # else if the distances are equal that means that the node is closest to an endpoint.
            elif pointDistance == testDistance:
                # Calcualte the distance between the new node and the midpoint of the current closest line segment
                test1 = CalculatePointTieBraker(closest1, closest2, nodeTo)
                # ditto for the new line segment
                test2 = CalculatePointTieBraker(self.path[i], self.path[i+1], nodeTo)
                # If the distance between the node and the current shortest is shorter than the new node and
                # the new line segment continue
                if test1 < test2:
                    continue
                # else set the closest nodes. The distances are equal so I don't have to reassign.
                elif test2 < test1:
                    closest1 = self.path[i]
                    closest2 = self.path[i+1]

        # Edgecase, if the closest node is between last city and first city in cityList
        if closest2 == self.path[0]:
            self.path.insert(-1, nodeTo)
        # insert the node between closest1 and closest2
        else:
            index = self.path.index(closest2)
            self.path.insert(index, nodeTo)
        return True


# Calcualte the distance between the node and the line segment
def CalculatePointDistance(segStart, segEnd, point):
    # Math is from GeeksForGeeks
    segmentVector = [segEnd.x - segStart.x, segEnd.y - segStart.y]
    endToPoint = [point.x - segEnd.x, point.y - segEnd.y]
    startToPoint = [point.x - segStart.x, point.y - segStart.y]

    segDotETP = segmentVector[0] * endToPoint[0] + segmentVector[1] * endToPoint[1]
    segDotSTP = segmentVector[0] * startToPoint[0] + segmentVector[1] * startToPoint[1]

    if segDotETP > 0:
        return sqrt(endToPoint[0] ** 2 + endToPoint[1] ** 2)
    elif segDotSTP < 0:
        return sqrt(startToPoint[0] ** 2 + startToPoint[1] ** 2)
    else:
        return abs(segmentVector[0] * startToPoint[1] - segmentVector[1] * startToPoint[0]) / sqrt(segmentVector[0] ** 2 + segmentVector[1] ** 2)

# Calculate distance between point and line segment midpoint.
def CalculatePointTieBraker(segStart, segEnd, point):
    # Get midpoint
    segmentMiddle = [(segStart.x + segEnd.x)/2, (segStart.y + segEnd.y)/2]
    # Distance formula
    return sqrt((segmentMiddle[0] - point.x)**2 + (segmentMiddle[1] - point.y)**2)


# Calculates the distance between two given cities.
def CalculateDistance(nodeFrom, nodeTo):
    return math.sqrt((float(nodeTo.x)-float(nodeFrom.x))**2 + (float(nodeTo.y)-float(nodeFrom.y))**2)


# Global Variables
cityList = []
graph = None

# Build the tour path
def BuildTour(node, index):
    global graph, pause
    # initialize the graph if it is not already 
    if graph == None:
        graph = Graph(node)
    # if the node indes is not equal the start index add the edge
    if(node.index != index + 1):
        graph.AddEdge(cityList[index])
    # If the index is equal the the length length of the city list all cities were inserted
    if(index == len(cityList)-1):
        # Pause the animation
        pause = True
        # Print the city path in the terminal
        print([city.index for city in graph.path])
        # variable to hold the path distance sum
        sum = 0
        # sum the distances 
        for i in range(0, len(graph.path)-1):
            sum += CalculateDistance(graph.path[i], graph.path[i+1])
        print("Distance of path is: " + str(sum))
        # delete the graph so that you get a fresh graph on the next run
        del graph
        graph = None


# Reads the input file and buidls the citymap
def Driver(fileNumber):
    # Get location of the file. Should be placed in the same file as python script.
    location = os.path.join(sys.path[0], "Random" + str(fileNumber) + ".tsp")
    read = False

    # Open file
    with open(location, 'r') as inputFile:
        # Loop over each line in input file
        for line in inputFile:
            # If you have reached the section to read run
            if(read == True):
                # split the line into the index, x, and y values
                lineContent = line.split(' ')
                # Add cities to the citylist
                cityList.append(Node(int(lineContent[0]), float(lineContent[1]), float(lineContent[2])))
                # Continue so it doesn't have to do the next if statement.
                continue

            # Else check if the current line is the section header. If true set read to true
            if('NODE_COORD_SECTION' == line.strip('\n')):
                read = True
    # Map to hold the connections between cities


running = True
pause = False
def main():
    global running, pause, cityList
    # Select the file to read
    fileNumber = 30
    Driver(fileNumber)
    # Select a random start position
    randomIndex = random.randint(0, len(cityList)-1)
    # Set iterator to 0
    iterator = 0
    # Pygame best practice to handle inputs
    while running:
        # If the GUI is not paused then run
        if not pause:
            BuildTour(cityList[randomIndex], iterator)
            iterator += 1
        # Else swap what input file is being read and start over
        elif pause:
            iterator = 0
            cityList = []
            # Swap input file being read
            fileNumber = 40 if fileNumber == 30 else 30
            Driver(fileNumber)
            # If the input file is back to 30 select new starting point.
            if fileNumber == 30:
                running = False
            pause = False

startTime = time.time()
if __name__ == '__main__':
    main()
print("Execution took: " + str(time.time() - startTime))