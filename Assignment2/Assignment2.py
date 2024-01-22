###########################
from random import random, randint
import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy import stats
import sys
import pylab

N = 7
K = 100

def knapsackBool(i, size):
    if size == 0:       #Tests if the knapsack is full
        return True
    if size < 0:        #Tests if the knapsack is overfull
        return False
    if i == 0:          #tests if there are any items left available
        return False
    return knapsackBool(i-1, size) or knapsackBool(i-1, size - S[i])
    
for _ in range(0,100):
    S = [randint(1,K/2) for _ in range(0,N + 1)]
    if knapsackBool(N, K):
        print("Solution exists")
    else:
        print("Solution does not exist")
        
    
    #some testing 
N = 5
K = 10
S = [None, 11,12,23,435,44,4,20]
print(knapsackBool(N, K))   #returns false since there is no way to fill
                            #sack of size 10 from the elements of S
print(knapsackBool(N,11))   #returns true because you can fill a sack of size
                            #11


######
#Part 2 of assignment: 2 knapsack problem returning floating value
def knapsackFloat(i, sizek1, sizek2):
    if sizek1 == 0 and sizek2 == 0:
        return 0.0
    if i==0:
        return 0.0
    fillSack1 = 0.0
    fillSack2 = 0.0
    if sizek1 >= S[i]:
        fillSack1 = knapsackFloat(i-1, sizek1-S[i], sizek2) + V[i]
    if sizek2 >= S[i]:
        fillSack2 = knapsackFloat(i-1, sizek1, sizek2-S[i])+V[i]
    return max(knapsackFloat(i-1, sizek1, sizek2), fillSack1, fillSack2)

K1 = 1
K2 = 2

S = [None, 1, 1, 1, 1]
V = [None, 1, 2, 3, 4]
"""

#temporary testing code for sanity check
print(knapsackFloat(4, K1, K2))#expect 9
print(knapsackFloat(3, K1, K2))
print(knapsackFloat(4, 0, 1))

"""

####
#Part 3 of the assignment: random problem generator!

def probGen(N, aveSize):
    S=[randint(1, 2*aveSize) for _ in range(0, N+1)]
    V=[np.random.randn() for _ in range(0, N+1)]
    return S,V


###
#given code for timing, note that one of the if statements wasn't working and has been commented out so
#that the code could function. was getting an error on line 120 related to line 105, so far inexplicable
def showTime(function, sizes, init = None, fit = 'exponential'):  
    # times a given function and displays the time as a function of problem size  
    #function takes a single integer argument  
    #runs the function with an input values taken from input array sizes  
    #generates a graph of run time as a function of problem size  
    # init, if provided, is a function that is called once before function is called 
    # fit may be 'exponential' then the time as a function of problem size is assumed  
    #     to of the form time = c * a^n and the function solves for c and a  
    #     where a is the base of the exponential function and c is a multiplicative factor  
    #     sizes should be arithmeticly increasing (such as [10, 11, 12, 13, 14, 15])  
    # fit my be 'polynomial' then the time as a function of problem size is assumed  
    #     to of the form time = c * n ^ b and the function solves for c and b   
    #     where b is the power of n (the degree of the polynomial) and c is a multiplicative factor  
    #     sizes should be geometrically increasing (such as [64, 128, 256, 512, 1024])    
    timeLine = []    
    validSizes = []    
    for n in sizes:
        startTime = datetime.datetime.now()
        if not init == None:
            init()
        function(n)
        endTime = datetime.datetime.now()
        time_diff = (endTime - startTime)
        elapsed = time_diff.total_seconds() #* 1000
        #if elapsed > 0: #sometimes the function is too fast and we get 0 time
        timeLine.append(elapsed)
        validSizes.append(n)
        ##Generating the plot between time taken by each function call with n as variable and n
        plt.plot(validSizes, timeLine, 'g')
        plt.xlabel("n")
        if fit == 'exponential':
            plt.yscale('log')
        if fit == 'polynomial':
            plt.yscale('log')
            plt.xscale('log')
        plt.ylabel("time in milliseconds")
        plt.rcParams["figure.figsize"] = [16,9]
        plt.show()
        if fit == 'exponential': #fit a straight line to n and log time
            slope, intercept, _, _, _ = stats.linregress([validSizes], [np.log(t) for t in timeLine])
            print("time = %.6f %.3f ^ n" % (np.exp(intercept), np.exp(slope)))
        elif fit == 'polynomial': # fit a straight line to log n and log time 
            slope, intercept, _, _, _ = stats.linregress([np.log(v) for v in validSizes], [np.log(t) for t in timeLine])
            print("time = %.6f n ^ %.3f" % (np.exp(intercept), slope))
                        
def timerFunction(N):
    return knapsackFloat(N, 100, 100)

"""maxN = 15
S, V = probGen(maxN, 20)
"""
###
#part 4
##showTime(timerFunction, range(1,maxN), fit = "exponential")

def knapsackMemo(i, sizek1, sizek2):
    if sizek1 == 0 and sizek2 == 0:
        return 0.0
    if i==0:
        return 0.0
    
    if (i, sizek1, sizek2) in Cache:
        return Cache[i, sizek1, sizek2]
    
    fillSack1 = 0.0
    fillSack2 = 0.0
    if sizek1 >= S[i]:
        fillSack1 = knapsackMemo(i-1, sizek1-S[i], sizek2) + V[i]
    if sizek2 >= S[i]:
        fillSack2 = knapsackMemo(i-1, sizek1, sizek2-S[i])+V[i]
    Cache[i, sizek1, sizek2] = max(knapsackMemo(i-1, sizek1, sizek2), fillSack1, fillSack2)
    return Cache[i, sizek1, sizek2]

def knapsackDP(i, sizek1, sizek2):
    AnswerMatrix = {}
    for j in range(0,sizek1+1):
        for k in range(0,sizek2+1):
            for l in range(0,i+1):
                if (j==0 and k==0) or l==0:
                    AnswerMatrix[(l,j,k)]=0.0
                else:
                    fillSack1 = 0.0
                    fillSack2 = 0.0
                    if j >= S[l]:
                        fillSack1 = AnswerMatrix[(l-1, j-S[l], k)] + V[l]
                    if k >= S[l]:
                        fillSack2 = AnswerMatrix[(l-1, j, k-S[l])]+V[l]
                    AnswerMatrix[(l,j,k)] = max(AnswerMatrix[(l-1, j, k)], fillSack1, fillSack2)
        
    return AnswerMatrix.get((i, sizek1, sizek2))
    
"""N=5
K1=10
K2=5

S=[None, 10, 4, 5, 4, 5]
V=[None, 12, 15, 1, 12, 41]

global Cache
Cache = {}

##print(knapsackMemo(N, K1, K2))
##print(knapsackDP(N,K1,K2))
"""
def RaceTimer(N, K1, K2):
    memoTime=[]
    DPTime=[]
    AveSizes=[]
    for i in range(1, N, round(N/10)):
        AveSizes.append(i)
        mt = 0.0
        dpt=0.0
        for _ in range(20):
            global S,V
            S,V = probGen(N, i)
            mStart = datetime.datetime.now()
            global Cache
            Cache = {}
            
            knapsackMemo(N,K1,K2)
            mStop = datetime.datetime.now()
            mt+=(mStop-mStart).total_seconds()
            
            dpStart = datetime.datetime.now()
            knapsackDP(N,K1,K2)
            dpStop = datetime.datetime.now()
            dpt+=(dpStop-dpStart).total_seconds()
        memoTime.append(mt)
        DPTime.append(dpt)
    figure = plt.figure()
    subplot = figure.add_subplot(1,1,1)
    
    line1 = subplot.plot(memoTime, color = 'red', lw = 1)
    line2 = subplot.plot(DPTime, color = 'blue', lw = 1)
    
    pylab.show

RaceTimer(45, 50, 50)
            