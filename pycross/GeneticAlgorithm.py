import numpy as np
import pycross
from numpy import random
import time

class Solution:
    def __init__(self, points, puzzleContraints):
        self.points  = points
        self.fitness = fitness(points, puzzleContraints)

def getContraints(puzzle):
    contraints = []
    contraints = puzzle.rows
    contraints = contraints.append(puzzle.columns)
    return contraints

def main():
    
    #x = pycross.from_json(open("examples/5x5Monochrome/1.json").read())
    #puzzleName = "examples/5x5Monochrome/1.json"
    #contraints = getContraints(x)
    #print("contraints: ", contraints)
    #populationSize = 200
    

    puzzleName = '1'
    populationSize = 200

    contraints = readContraintsFile('examples/' + puzzleName + '.txt')
    puzzleContraints = createPuzzleContraints(contraints, populationSize)

    #print("Puzzel constraints: ", puzzleContraints)

    contraints, rows, columns, nPoints, populationSize = puzzleContraints
    puzzleContraints = contraints, rows, columns, rows*columns, populationSize
    
    
    pre = time.perf_counter()
    solution = geneticAlgo(puzzleContraints)
    print(checkSolution(Game(rows, columns, solution.points), contraints))

    post = time.perf_counter()
    print("Time: ", post - pre)
   

def geneticAlgo(puzzleContraints):
    contraints, rows, columns, nPoints, populationSize = puzzleContraints
    iterations = 0
    RandomAgents = randomInit(puzzleContraints)
    
    while not converge(RandomAgents, puzzleContraints):
        ParentsChildren  = crossover(RandomAgents, puzzleContraints)
        MutatedChildren = mutation(ParentsChildren, puzzleContraints)
        RandomAgents   = select(RandomAgents, MutatedChildren, puzzleContraints)
        iterations += 1

        # print("Iteration count: ", iterations)
        # print("Contraints unmet: ", abs(RandomAgents[0].fitness))
        if(iterations > 1000):
            break
    return finalIter(RandomAgents, puzzleContraints)

def randomInit(puzzleContraints):
    contraints, rows, columns, nPoints, populationSize = puzzleContraints

    S = []

    # print()
    for _ in range(populationSize):
        s = []
        for _ in range(nPoints):
            if random.random() <= 0.5:
                s += [True]
            else:
                s += [False]
        S += [Solution(s, puzzleContraints)]
    return S

def crossover(P, puzzleContraints):
    contraints, rows, columns, nPoints, populationSize = puzzleContraints

    PP    = []

    P = sorted(P, key = lambda s : (s.fitness, random.random()))
    n = (populationSize*(populationSize+1))/2
    prob=[i/n for i in range(1, populationSize+1)]

    for _ in range(populationSize):
        child1Points = []
        child2Points = []
        parent1, parent2 = random.choice(P, p=prob, replace=False, size=2)

        for i in range(nPoints):
            if random.random() <= 0.5:
                child1Points += [parent1.points[i]]
                child2Points += [parent2.points[i]]
            else:
                child1Points += [parent2.points[i]]
                child2Points += [parent1.points[i]]

        PP    += [Solution(child1Points, puzzleContraints), Solution(child2Points, puzzleContraints)]

    return PP

def mutation(P, puzzleContraints):
    contraints, rows, columns, nPoints, populationSize = puzzleContraints

    PP = []

    for s in P:

        prob = 0.01
        newPoints = []

        for p in s.points:
            if random.random() > prob:
                newPoints += [p]
            else:
                newPoints += [not p]

        PP += [Solution(newPoints, puzzleContraints)]

    return PP

def select(randomAgents, crossoverParents, puzzleContraints):
    contraints, rows, columns, nPoints, populationSize = puzzleContraints

    randomAgents = sorted(randomAgents, key = lambda s : (s.fitness, random.random()), reverse = True)
    PP = sorted(crossoverParents, key = lambda s : (s.fitness, random.random()), reverse = True)

    nParents  = int(0.2*populationSize)+1
    nChildren = int(0.5*populationSize)+1
    nRandom = populationSize - nChildren - nParents

    bestOnes = randomAgents[:nParents] + crossoverParents[:nChildren]
    others   = randomAgents[nParents:] + crossoverParents[nChildren:]

    nextGeneration = bestOnes + np.ndarray.tolist(random.choice(others, size=nRandom, replace=False))

    return nextGeneration

def converge(P, puzzleContraints):
    contraints, rows, columns, nPoints, populationSize = puzzleContraints

    for s in P:
        if s.fitness == 0:
            return True

    for i in range(len(P)-1):
        if P[i].points != P[i+1].points:
            return False

    return True

def finalIter(P, puzzleContraints):
    contraints, rows, columns, nPoints, populationSize = puzzleContraints

    for s in P:
        if s.fitness == 0:
            return s
    return P[0]

class Game:
    def __init__(self, rows, columns, points):
        self.rows   = rows
        self.columns = columns
        self.board = []

        for _ in range(self.rows):
            aux = []
            for _ in range(self.columns):
                aux += [False]
            self.board += [aux]

        self.fill(points, rows, columns)

    def fill(self, points, rows, columns):
        for i, v in enumerate(points):
            self.board[int(i/columns)][i%columns] = v

    def __str__(self):
        result = '=' * ((self.columns)*2+2) + '\n'

        for l in self.board:
            result += '|'
            for s in l:
                result += (chr(9608) if not s else ' ')*2
            result += '|\n'

        result += '=' * ((self.columns)*2+2)
        return result

class Contraints:
    # example: lines = [[1,2,3], [], [2], [9]]
    def __init__(self, rows, columns):
        self.rows   = rows
        self.columns = columns

    def __str__(self):
        result = 'rows:\n'
        for l in self.rows:
            for n in l:
                result += str(n)
                result += ' '
            result += '\n'

        result += 'columns:\n'
        for c in self.columns:
            for n in c:
                result += str(n)
                result += ' '
            result += '\n'
        return result[:-1]

def checkSolution(game, contraints):
    board    = game.board
    rows   = game.rows
    columns = game.columns

    for row in range(rows):
        contraintsQtt = len(contraints.rows[row])

        column = 0
        ruleIndex   = 0
        while column < columns and ruleIndex < contraintsQtt:
            countSegment = 0

            while(column < columns and not board[row][column]):
                column += 1

            while(column < columns and board[row][column]):
                countSegment += 1
                column  += 1

            currRule = contraints.rows[row][ruleIndex]
            if(countSegment != currRule):
                return False

            ruleIndex += 1

        if ruleIndex < contraintsQtt:
            return False

        while(column < columns):
            if(board[row][column]):
                return False
            column += 1

    for column in range(columns):
        contraintsQtt = len(contraints.columns[column])

        row = 0
        ruleIndex   = 0

        # Check if all contraints are being fulfilled
        while row < rows and ruleIndex < contraintsQtt:
            countSegment = 0

            while(row < rows and not board[row][column]):
                row += 1

            while(row < rows and board[row][column]):
                countSegment += 1
                row  += 1

            currRule = contraints.columns[column][ruleIndex]
            if(countSegment != currRule):
                return False

            ruleIndex += 1

        # Check if there isn't any remaining rule
        if ruleIndex < contraintsQtt:
            return False

        # Check if there isn't any additional square after last rule
        while(row < rows):
            if(board[row][column]):
                return False
            row += 1

    return True

def readContraintsFile(puzzleFile):
    
    with open(puzzleFile) as puzzleFile:
        readingLines = True
        rows   = []
        columns = []

        for rule in puzzleFile:
            if(rule == '-\n'):
                readingLines = False
                continue

            constraints = [[int(x) for x in rule.split()]]
            if(readingLines):
                rows   += constraints
            else:
                columns += constraints

    return Contraints(rows=rows, columns=columns)

def createPuzzleContraints(contraints, populationSize):
     
    rows   = len(contraints.rows)
    columns = len(contraints.columns)
    nPoints  = 0

    # Count total number of points
    for row in contraints.rows:
        for rule in row:
            nPoints += rule

    return (contraints, rows, columns, nPoints, populationSize)

def fitness(sol, puzzleContraints):
    contraints, rows, columns, nPoints, populationSize = puzzleContraints
    count = 0
    game  = Game(rows, columns, sol)
    board = sol

    for row in range(rows):
        contraintsQtt = len(contraints.rows[row])

        column = 0
        ruleIndex   = 0

        while column < columns or ruleIndex < contraintsQtt:
            countSegment = 0
            currRule     = contraints.rows[row][ruleIndex] if ruleIndex < contraintsQtt else 0

            while column < columns and not board[row*columns + column]:
                column += 1

            while column < columns and board[row*columns + column]:
                countSegment += 1
                column += 1

            count -= abs(countSegment - currRule)
            ruleIndex += 1

    for column in range(columns):
        contraintsQtt = len(contraints.columns[column])

        row = 0
        ruleIndex = 0

        while row < rows or ruleIndex < contraintsQtt:
            countSegment = 0
            currRule     = contraints.columns[column][ruleIndex] if ruleIndex < contraintsQtt else 0

            while row < rows and not board[row*columns + column]:
                row += 1

            while row < rows and board[row*columns + column]:
                countSegment += 1
                row    += 1

            count     -= abs(countSegment - currRule)
            ruleIndex += 1

    return count

import pycross

def solve_from_picross(puzzle : pycross.Picross):

    # contraints = readContraintsFile('examples/' + puzzleName + '.txt')
    # puzzleContraints = createPuzzleContraints(contraints, populationSize)
    # contraints, rows, columns, nPoints, populationSize = puzzleContraints

    row_rules = [[rule[1] for rule in row] for row in puzzle.rows]
    column_rules = [[rule[1] for rule in column] for column in puzzle.columns]
    contraints = Contraints(rows=row_rules, columns=column_rules)
    rows = puzzle.height
    columns = puzzle.width
    populationSize = 200

    puzzleContraints = contraints, rows, columns, rows * columns, populationSize

    pre = time.perf_counter()
    solution = geneticAlgo(puzzleContraints)
    # print(checkSolution(Game(rows, columns, solution.points), contraints))
    # print(Game(rows, columns, solution.points))
    # print(solution.points)
    post = time.perf_counter()
    # print("Time: ", post - pre)

    def split_to_lines(gen_list, width):
        for i in range(0, len(gen_list), width):
            yield gen_list[i:i + width]

    def map_to_colour(marked):
        if marked:
            return list(puzzle.colours.keys())[0]
        else:
            return 0

    row = 0
    for line in split_to_lines(solution.points, puzzle.width):
        puzzle[row] = [map_to_colour(x) for x in line]
        row += 1

    return puzzle

if __name__ == '__main__':
    
    main()

