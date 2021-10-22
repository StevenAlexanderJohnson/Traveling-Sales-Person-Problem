import math
import random
import time

from Develop import Calculate_Population_Scores

populationList = []
cityList = []

class City:
    def __init__(self, index:int, x:float, y:float) -> None:
        self.index = index
        self.x = x
        self.y = y

    
class Chromosome:
    def __init__(self, path, score) -> None:
        self.path = path
        self.score = score


def Calculate_Distance(cityFrom, cityTo):
    return math.sqrt((cityFrom.x - cityTo.x)**2 + (cityFrom.y - cityTo.y)**2)


def Calculate_Score(pathList:list) -> int:
    sum = 0
    # Calculate the list in order
    for i in range(1, len(pathList)):
        sum += Calculate_Distance(pathList[i-1], pathList[i])
    # Calcualte the score from the last element to the first element
    # to complete the loop
    sum += Calculate_Distance(pathList[0], pathList[-1])
    return sum


def Calculate_Population_Scores(population:list[Chromosome]) -> None:
    for chromosome in population:
        chromosome.score = Calculate_Score(chromosome.path)


def Get_City_List(filename) -> None:
    global cityList
    read = False
    with open(filename, 'r') as inputFile:
        for line in inputFile:
            if read == True:
                lineContent = line.split(' ')
                cityList.append(City(int(lineContent[0]), float(lineContent[1]), float(lineContent[2])))
            elif 'NODE_COORD_SECTION' == line.strip('\n'):
                read = True


def Generate_Population(populationNumber:int, possibilities:list) -> list:
    global populationList
    populationList = []
    for _ in range(populationNumber):
        random.shuffle(possibilities)
        score = Calculate_Score(possibilities)
        populationList.append(Chromosome(possibilities.copy(), score))
    return populationList


def OrderCrossover(population:list[Chromosome]) -> tuple[list[Chromosome], bool]:
    # Get population max/min scores used later
    populationMax = 0
    populationMin = math.inf
    for i in range(len(population)):
        if population[i].score < populationMin:
            populationMin = population[i].score
        if population[i].score > populationMax:
            populationMax = population[i].score
    
    # Generate a probability distrobution for each
    try:
        distrobutions = []
        for path in population:
            distrobution = ((path.score - populationMax)/(populationMin - populationMax))**2
            distrobutions.append(distrobution)
    except ZeroDivisionError:
        return population, False
    
    # Generate two list for parents
    selectedParents1 = random.choices(population.copy(), weights=distrobutions, k=len(population))
    selectedParents2 = random.choices(population.copy(), weights=distrobutions, k=len(population))

    outputPopulation = []
    while(len(outputPopulation) <= len(population)//2):
        chromosome1 = selectedParents1.pop(0)
        chromosome2 = selectedParents2.pop(0)
        # Random indexes to split the list into three sections
        randomIndex1 = random.randint(1, len(chromosome1.path)//2)
        randomIndex2 = random.randint(randomIndex1+1, len(chromosome2.path)-2)

        # Get the middle section of the three sections.
        chromosome1Middle = chromosome1.path[randomIndex1:randomIndex2]
        chromosome2Middle = chromosome2.path[randomIndex1:randomIndex2]

        # Concatenate the other two sections
        otherSections1 = [i for i in chromosome1.path if not i in chromosome2Middle]
        otherSections2 = [i for i in chromosome2.path if not i in chromosome1Middle]

        # Insert at the end wrapping around to the beginning causing the middle section to stay at the same index.
        chromosome2Middle = chromosome2Middle + otherSections1
        chromosome1Middle = chromosome1Middle + otherSections2
        outputPopulation.append(Chromosome(chromosome1Middle, math.inf))
        outputPopulation.append(Chromosome(chromosome2Middle, math.inf))
    return (population[:len(population)//2] + outputPopulation, True)


def ScoredCrossover(population:list[Chromosome]) -> tuple[list[Chromosome], bool]:
    # Get population max/min scores used later
    populationMax = 0
    populationMin = math.inf
    for i in range(len(population)):
        if population[i].score < populationMin:
            populationMin = population[i].score
        if population[i].score > populationMax:
            populationMax = population[i].score
    
    # Generate a probability distrobution for each
    try:
        distrobutions = []
        for path in population:
            distrobution = ((path.score - populationMax)/(populationMin - populationMax))**2
            distrobutions.append(distrobution)
    except ZeroDivisionError:
        return population, False
    
    # Generate two list for parents
    selectedParents1 = random.choices(population.copy(), weights=distrobutions, k=len(population[:len(population)//2+1]))
    selectedParents2 = random.choices(population.copy(), weights=distrobutions, k=len(population))

    outputPopulation = []
    while(len(outputPopulation) <= len(population)//2):
        chromosome1 = selectedParents1.pop(0)
        chromosome2 = selectedParents2.pop(0)
        # Random indexes to split the list into three sections
        randomIndex1 = random.randint(1, len(chromosome1.path)//2)
        randomIndex2 = random.randint(randomIndex1+1, len(chromosome2.path)-2)

        # Get the middle section of the three sections.
        chromosome1Middle = chromosome1.path[randomIndex1:randomIndex2]
        chromosome2Middle = chromosome2.path[randomIndex1:randomIndex2]

        # Concatenate the other two sections
        otherSections1 = [i for i in chromosome1.path if not i in chromosome2Middle]
        otherSections2 = [i for i in chromosome2.path if not i in chromosome1Middle]

        # Insert at the end wrapping around to the beginning causing the middle section to stay at the same index.
        chromosome2Middle = chromosome2Middle + otherSections1
        chromosome1Middle = chromosome1Middle + otherSections2
        child1 = Calculate_Score(chromosome1Middle)
        child2 = Calculate_Score(chromosome2Middle)
        if(child1 < child2):
            outputPopulation.append(Chromosome(chromosome1Middle, math.inf))
        else:
            outputPopulation.append(Chromosome(chromosome2Middle, math.inf))
    return (population[:len(population)//2] + outputPopulation, True)


def Mutation(population: list[Chromosome]) -> None:
    numberOfMutations = int(.05 * len(population))
    # At least one mutation
    if(numberOfMutations < 1):
        numberOfMutations = 1
    mutatedIndex = []
    for _ in range(numberOfMutations):
        randomIndex = random.randint(1, len(population)-1)
        while(randomIndex in mutatedIndex):
            randomIndex = random.randint(1, len(population)-1)
        mutatedIndex.append(randomIndex)

        randomSwapIndex1 = random.randint(0, len(population[randomIndex].path)//2)
        randomSwapIndex2 = random.randint(randomSwapIndex1+1, len(population[randomIndex].path)-1)
        population[randomIndex].path[randomSwapIndex1],population[randomIndex].path[randomSwapIndex2] = population[randomIndex].path[randomSwapIndex2],population[randomIndex].path[randomSwapIndex1]


def MajorMutation(population: list[Chromosome]) -> None:
    numberOfMutations = int(.10 * len(population))
    # At least one mutation
    if(numberOfMutations < 1):
        numberOfMutations = 1
    mutatedIndex = []
    for _ in range(numberOfMutations):
        randomIndex = random.randint(1, len(population)-1)
        while(randomIndex in mutatedIndex):
            randomIndex = random.randint(1, len(population)-1)
        mutatedIndex.append(randomIndex)

        randomSwapIndex1 = random.randint(0, int((len(population[randomIndex].path)-1)*.25))
        randomSwapIndex2 = random.randint(randomSwapIndex1 + 1, int((len(population[randomIndex].path)-1)*.5))
        randomSwapIndex3 = random.randint(randomSwapIndex2 + 1, int((len(population[randomIndex].path)-1)*.75))
        randomSwapIndex4 = random.randint(randomSwapIndex3 + 1, (len(population[randomIndex].path)-1))        
        population[randomIndex].path[randomSwapIndex1],population[randomIndex].path[randomSwapIndex3] = population[randomIndex].path[randomSwapIndex3],population[randomIndex].path[randomSwapIndex1]
        population[randomIndex].path[randomSwapIndex2],population[randomIndex].path[randomSwapIndex4] = population[randomIndex].path[randomSwapIndex4],population[randomIndex].path[randomSwapIndex2]
        population[randomIndex].path = population[randomIndex].path[0:randomSwapIndex1] + population[randomIndex].path[randomSwapIndex1:randomSwapIndex2] + population[randomIndex].path[randomSwapIndex2:randomSwapIndex3] + population[randomIndex].path[randomSwapIndex3:randomSwapIndex4] + population[randomIndex].path[randomSwapIndex4: len(population[randomIndex].path)]
    

def main():
    global cityList

    Get_City_List("Random100.tsp")
    initialPopulation = Generate_Population(1000, cityList)
    population = sorted(initialPopulation, key=lambda x: x.score)
    print("Best Initial Score: ")
    print(population[0].score)

    continueValue = True
    generation = 0
    bestGenerationScore = math.inf
    bestScorePath = 0
    while(continueValue):
        if(generation == 1000):
            print("-----Generation Cap Hit-----")
            break
        # Update population with one of the following crossovers
        # population, continueValue = OrderCrossover(population)
        population, continueValue = ScoredCrossover(population)
        # Mutate certain percent of population using one of the following mutations.
        Mutation(population)
        # MajorMutation(population)

        Calculate_Population_Scores(population)
        population.sort(key=lambda x: x.score)
        
        if(bestScorePath == 10000):
            print("-----Decent Path Found-----")
            print("Generation {}: {}".format(generation, population[0].score))
            break
        generation += 1

    # Print the best score and path
    print(str(population[0].score) + "\n" + str([i.index for i in population[0].path]))


if __name__ == '__main__':
    startTime = time.time()
    main()
    print("Execution took: {}".format(time.time() - startTime))