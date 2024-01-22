# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 20:47:06 2021

@author: User
"""

import random
import matplotlib.pyplot as plt
from scipy import stats
import datetime

# switches for whether or not to use short circuits in different places in the code,
# for testing purposes.
evalExpShort = False
solveExpShort = False

def makeExp(n):
    # n variables (use 0 ... n-1 for variables, and n .. 2n-1 for their negation
    # we always generate 4.3 * n clauses because for some reason, this ratio
    # generates the hardest problems!
    return [[random.randint(0, 2 * n - 1) for _ in range(3)] for _ in 
range(int(4.3*n))]
def printSolution(exp, values, solution):
    variableValues = values + [not values[i] for i in range(len(values))]
    print("Solution is " + (" True " if solution else "False"))
    if solution:
        print("Variables = " + ''.join(["T " if values[i] else "F " for i in 
range(len(values))]))
        print("Clauses ")
        for clause in exp:
            print('(' + ''.join(["T " if variableValues[var] else "F " for var in 
clause]) + ')')
            
            
def evalExp(exp, values):
    # append the negated variables at the end
    variableValues = values + [not values[i] for i in range(len(values))]
    solution = True
    for j in range(len(exp)):
        solution = solution and evalClause(exp[j], variableValues)
        if evalExpShort and not solution: #short circuit evaluation
            break
    return solution

def evalClause(clause, variableValues):
    return variableValues[clause[0]] or variableValues[clause[1]] or variableValues[clause[2]]

"""
The given version of solve expression,
reffered to as Algorithm0 in graphs given
hereafter
"""

def solveExp(exp, n, values=[]):
    # modified to return both the solution (true or false) and the variable 
#assignments
    if n == 0:
        return (evalExp(exp, values), values)
    # Early termination strategy
    # check if the partial assignment leads to any false clauses
    (solT, valuesT) = solveExp(exp, n - 1, [True] + values)
    if solveExpShort and solT: #short circuit evaluation
        return (solT, valuesT)
    (solF, valuesF) = solveExp(exp, n - 1, [False] + values)
    if solT:
        return (solT, valuesT)
    else:
        return (solF, valuesF)
    
def solveExp1(exp, n, values = []):
    evalExpShort = True
    return solveExp(exp, n, values=[])
    
def solveExp2(exp,n,values=[]):
    evalExpShort = True
    solveExpShort = True
    return solveExp(exp,n,values=[])

def lastVarAssigned(clause, n):
    #get's the last variable assigned in clause for expDict below
    return n - max(i if i<n else i - n for i in clause)
    
def expDict(exp, n):
    #fills a dictionary with empty lists
    myDict = {i: [] for i in range(n+1)}
    for clause in exp :
        lastVar = lastVarAssigned(clause, n)
        #appends each clause to the key that corresponds to the point
        # in solveEXP where that clause is checkable
        myDict[lastVar].append(clause)
    return myDict

def solveExp3(exp, n, values=[], myDict = "none"):
    # build expDict in the first recursion, then pass it on.
    evalExpShort = True
    if myDict == "none":
        myDict = expDict(exp, n)
    if n == 0:
        return (evalExp(exp, values), values)
    # Early termination strategy
    # check if the partial assignment leads to any false clauses
    
    if myDict[n] : #if any clauses are checkable at this point
        if not (evalExp(myDict[n], values + [False]*n)): #check those clauses and
            return (False, values)      #terminate early
        
    (solT, valuesT) = solveExp(exp, n - 1, [True] + values)
    if solT: #short circuit evaluation
        return (solT, valuesT)
    (solF, valuesF) = solveExp(exp, n - 1, [False] + values)
    if solT:
        return (solT, valuesT)
    else:
        return (solF, valuesF)
# def walkSat(exp, n, p, maxFlips):
#     # exp is the expression, n is how many variables, p is a probability usually 
#set to 0.5,
#     # maxFlips is an int
#     values = randomValues(n) #generate a list of random Boolean values
#     for i in range(0, maxFlips): #number of attempts at finding a solution
#         if evalExp(exp, values): #found a solution
#             return (True, values)
#         clause = selectRandomClause(exp, values) #randomly select unsatisfied 
#clause
#         if random.random() < p: #with probability p
#             values = # flip the value of a randomly chosen variable in clause
#         else:
#             values = #for each variable in clause, flip it and count the number 
#of unsatisfied clauses
#                      #select the variable flip that leads to the minimum number 
#of unsatisfied clauses
#     return (False, [])
"""n = 22 #always make the number of clauses 4.5* the number of variables
for i in range(100):
    exp = makeExp(n)
    (solution, values) = solveExp(exp, n, values=[])
    printSolution(exp, values, solution)
    """
    
def comparisonPlotter(functions, sizes) :
    #create a seperate line for each function passed in functions.
    timeLines = [[] for _ in range(len(functions))]
    #only graph those sizes which have measurable results for the given function.
    validSizes = [[] for _ in range(len(functions))]
    for i in sizes:
        #create 5 random problems of with i variables to test
        problems = [makeExp(i) for _ in range(5)]
        for f in range(len(functions)) :
            startTime = datetime.datetime.now()
            for p in problems:
                functions[f](p, i)
            endTime = datetime.datetime.now()
            timeDiff = endTime-startTime
            elapsedAve = timeDiff.total_seconds()*200 #average time in milliseconds (*1000/5)
            if elapsedAve > 0:
                timeLines[f].append(elapsedAve)
                validSizes[f].append(i)
            
            plt.plot(validSizes[f], timeLines[f], label = "Algorithm{}".format(f))
            
            plt.legend()
            plt.xlabel("Problem size")
            plt.ylabel("time in milliseconds")
       
        
        plt.yscale('log')
        plt.rcParams["figure.figsize"] = [16,9]
        plt.show()

n = 10
for i in range(100):
    exp = makeExp(n)
    (solution, values) = solveExp(exp, n, values=[])
    (sol3, val3) = solveExp3(exp, n, values=[])
    if sol3 == solution :
        print("algorithm 3 match!")    
    else :
        print("algorithm 3 innaccuracy found!")


comparisonPlotter([solveExp, solveExp1, solveExp2, solveExp3], [i for i in range(3,22)])

                