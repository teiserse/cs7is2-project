
import numpy as np
from numpy import random
import time
import pycross

class Solution:
    def __init__(self, score, puzzleContraints):
        self.score  = score
        self.fitness = fitness(score, puzzleContraints)

class Game:
    def __init__(self, rows, columns, score):
        self.rows   = rows
        self.columns = columns
        self.board = []
        self.difficulty = 1
        self.colour = 1

        for row in range(rows):
            line = []
            for column in range(columns):
                line = line + [False]
            # effetively appends the new line to the puzzle
            self.board = self.board + line

class Contraints:
    
    def __init__(self, rows, columns):
        self.rows   = rows
        self.columns = columns

def geneticAlgo(puzzleContraints):

# in this function we carry out the main genetic algorithm function. 
# The operations mutate and crossOver are undertaken while the population has not
# converged on a solution.
#    
    contraints, rows, columns, fitnessScore, populationSize = puzzleContraints
    iterations = 0
    maxIter = 1000
    #initialise a population of agents which random configurations for the Picross puzzle.
    
    RandomAgents = []
    for n in range(populationSize):
        agent = []
        for score in range(fitnessScore):
            x = random.uniform(0, 1)
            #after experimenting with this threshhold for setting filled values, it was determined that 40% is optimal.
            threshhold = 0.4
            if (x < threshhold):
                agent = agent + [True]
            else:
                agent = agent + [False]
        RandomAgents = RandomAgents + [Solution(agent, puzzleContraints)]
    
    for _ in range (maxIter):
        # parents are selected from population and crossedover to produce offspirng.
        ParentsChildren  = crossOver(RandomAgents, puzzleContraints)
        # the  generation of children undergo mutations.
        MutatedChildren = mutate(ParentsChildren, puzzleContraints)
        # the next generation is selected based on a fitness function.
        RandomAgents = select(RandomAgents, MutatedChildren, puzzleContraints)
        
        iterations += 1
        # print("Iteration count: ", iterations)
        # print("Contraints unmet: ", abs(RandomAgents[0].fitness))

        #the current generation is checked against the known solution.
        #if the solution has been reached, the loop terminates early.
        if (converge(RandomAgents, puzzleContraints)):
            break
    return finalIter(RandomAgents, puzzleContraints)




def crossOver(RandomAgents, puzzleContraints):
    
    contraints, rows, columns, fitnessScore, populationSize = puzzleContraints
    ParentsChildren = []

    RandomAgents = sorted(RandomAgents, key = lambda x : (x.fitness, random.random()))
    
    prob = [None] * 200
    for i in range(200):
        prob[i] = 1/(2*(i+1))

    n = (populationSize*(populationSize+1))/2
    prob=[i/n for i in range(1, populationSize+1)]

    for i in range(populationSize):
        
        newOffspring1 = []
        newOffspring2 = []
        newParent1 = random.choice(RandomAgents, p=prob)
        newParent2 = random.choice(RandomAgents, p=prob)
        #newOffspring1 = newOffspring1 + [newParent1.score[i]]
        #newOffspring2 = newOffspring2 + [newParent2.score[i]]
        
        for i in range(fitnessScore):
            x = random.uniform(0, 1)

            if x < 0.5:
                newOffspring1 = newOffspring1 + [newParent1.score[i]]
                newOffspring2 = newOffspring2 + [newParent2.score[i]]
            else:
                newOffspring1 = newOffspring1 + [newParent1.score[i]]
                newOffspring2 = newOffspring2 + [newParent1.score[i]]
        
        ParentsChildren = ParentsChildren + [Solution(newOffspring1, puzzleContraints), Solution(newOffspring2, puzzleContraints)]

    return ParentsChildren


def mutate(RandomAgents, puzzleContraints):
    contraints, rows, columns, fitnessScore, populationSize = puzzleContraints
    #this is the operation of flipping filled or unfilled boxes in the nonogram.

    # this is the new generation of solutions
    ParentsChildren = []
    for agent in RandomAgents:
        # this probability was derived from experimentation.
        # Higher probabilities of mutation produce more volatile results, i.e. the solution may converge very quickly
        # or may not converge at all depending on the initial random solutions.
        
        prob = 0.01
        square = []
        for score in agent.score:
            x = random.uniform(0, 1)

            if x > prob:
                square += [square]
            else:
                square += [not square]

        ParentsChildren += [Solution(square, puzzleContraints)]

    return ParentsChildren



def select(randomAgents, MutatedChildren, puzzleContraints):
    
    contraints, rows, columns, fitnessScore, populationSize = puzzleContraints

    randomAgents = sorted(randomAgents, key = lambda s : (s.fitness, random.random()), reverse = True)
    MutatedChildren = sorted(MutatedChildren, key = lambda s : (s.fitness, random.random()), reverse = True)

    nParents  = int(0.25*populationSize)+1
    nChildren = int(0.5*populationSize)+1
    nRandom = populationSize - nChildren - nParents

    bestOnes = randomAgents[:nParents] + MutatedChildren[:nChildren]
    others   = randomAgents[nParents:] + MutatedChildren[nChildren:]

    nextGeneration = bestOnes + np.ndarray.tolist(random.choice(others, size=nRandom, replace=False))

    return nextGeneration


def converge(RandomAgents, puzzleContraints):
    contraints, rows, columns, fitnessScore, populationSize = puzzleContraints
    # if we have converged on an optimal solution, we have converged, else we still continue the iterations.

    for agent in RandomAgents:
        if (agent.fitness == 0):
            return True   
    return False

def finalIter(RandomAgents, puzzleContraints):
    contraints, rows, columns, fitnessScore, populationSize = puzzleContraints

    bestAgent = RandomAgents[0]
    for agent in RandomAgents:
        if (agent.fitness == 0):
            return agent
        if (agent.fitness < bestAgent.fitness):
            bestAgent = agent
    
    return bestAgent


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

        if ruleIndex < contraintsQtt:
            return False

        while(row < rows):
            if(board[row][column]):
                return False
            row += 1

    return True



def fitness(sol, puzzleContraints):
    
    contraints, rows, columns, fitnessScore, populationSize = puzzleContraints
    count = 0
    game  = Game(rows, columns, sol)
    board = sol
    #generic fitness function for nonograms sourced from github/rlegendi/griddler-solver

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


    def split_to_lines(gen_list, width):
        for i in range(0, len(gen_list), width):
            yield gen_list[i:i + width]

    def map_to_colour(marked):
        if marked:
            return list(puzzle.colours.keys())[0]
        else:
            return 0


    row_rules = [[rule[1] for rule in row] for row in puzzle.rows]
    column_rules = [[rule[1] for rule in column] for column in puzzle.columns]
    contraints = Contraints(rows=row_rules, columns=column_rules)
    rows = puzzle.height
    columns = puzzle.width
    populationSize = 200

    puzzleContraints = contraints, rows, columns, rows * columns, populationSize

    pre = time.perf_counter()
    solution = geneticAlgo(puzzleContraints)
    post = time.perf_counter()
    
    row = 0
    for line in split_to_lines(solution.score, puzzle.width):
        puzzle[row] = [map_to_colour(x) for x in line]
        row += 1

    return puzzle

