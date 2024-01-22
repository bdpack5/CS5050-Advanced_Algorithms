# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 20:14:22 2021

@author: User
"""

import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy import stats
import random
import math

MAX_DISTANCE = 100
def xSort(point):
    return point[0]

def ySort(point):
    return point[1]

def distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
    
def xdistance(point1, point2):
    return abs(point1[0] - point2[0])


def minDistance(points):
    result = MAX_DISTANCE
    size = len(points)
    for i in range(size):
        for j in range(i+1, size):
            dist = distance(points[i], points[j])
            result = min(dist, result)
    return result

def minDistanceDC(points):
    n = len(points)
    if n <= 1:
        return MAX_DISTANCE
    if n == 2:
        return distance(points[0], points[1])
    
    result = min(minDistanceDC(points[n//2:]), minDistanceDC(points[:n//2]))
    midArray = points[n//2:n//2+1]
    for x in range(n//2+1, n):
        if xdistance(points[x], points[n//2-1])>result:
            break
        else :
            midArray.append(points[x])
    for x in range(n//2-1, 0, -1):
        if xdistance(points[x], points[n//2])>result:
            break
        else :
            midArray.append(points[x])
    midArray.sort(key = ySort)
    midLength = len(midArray)
    for i in range(midLength):
        limit = min(midLength, i+7)
        for j in range(i+1, limit):
            tempDist = distance(midArray[i], midArray[j])
            result = min(tempDist, result)
    return result    


def minDistanceHybrid(points):
    n = len(points)
    if n<= 32:
        return minDistance(points)
    if n <= 1:
        return MAX_DISTANCE
    if n == 2:
        return distance(points[0], points[1])
    
    result = min(minDistanceDC(points[n//2:]), minDistanceDC(points[:n//2]))
    midArray = points[n//2:n//2+1]
    for x in range(n//2+1, n):
        if xdistance(points[x], points[n//2-1])>result:
            break
        else :
            midArray.append(points[x])
    for x in range(n//2-1, 0, -1):
        if xdistance(points[x], points[n//2])>result:
            break
        else :
            midArray.append(points[x])
    midArray.sort(key = ySort)
    midLength = len(midArray)
    for i in range(midLength):
        limit = min(midLength, i+7)
        for j in range(i+1, limit):
            tempDist = distance(midArray[i], midArray[j])
            result = min(tempDist, result)
    return result  
        
def randProb(n):
    result = [(MAX_DISTANCE*random.random(), MAX_DISTANCE*random.random()) 
                       for _ in range(n)]
    return result

for i in range(10):
    
    prob = randProb(2**10)
    prob.sort(key = xSort)
    
    print (minDistance(prob) - minDistanceDC(prob))



def firstStudy(sizes):
    naiveLine = []
    DaCLine = []
    hybridLine = []

    finishedNaive = []
    finishedDaC = []
    finishedHybrid = []
   
    for n in sizes:
        naiveTotal = 0.0
        DaCTotal = 0.0
        hybridTotal = 0.0
        for _ in range(10):
            testProblem = randProb(n)
        
            startTime = datetime.datetime.now()
            minDistance(testProblem)
            endTime = datetime.datetime.now()
            elapsed = endTime - startTime
            naiveTotal += elapsed.total_seconds()*1000
        
        
            DaCStart = datetime.datetime.now()
            testProblem.sort(key = xSort)
            minDistanceDC(testProblem)
            DaCEnd = datetime.datetime.now()
            DaCelapsed = DaCEnd - DaCStart
            DaCTotal += DaCelapsed.total_seconds()*1000
        
            testProblem.sort(key = ySort)  
            hybridStart = datetime.datetime.now()
            testProblem.sort(key = xSort)
            minDistanceHybrid(testProblem)
            hybridEnd = datetime.datetime.now()
            hybridElapsed = hybridEnd - hybridStart
            hybridTotal += hybridElapsed.total_seconds()*1000
        
        naiveAverage = naiveTotal/10
        if naiveAverage > 0 :
            naiveLine.append(naiveAverage)
            finishedNaive.append(n)
            
        DaCAverage = DaCTotal/10
        if DaCAverage>0:
            DaCLine.append(DaCAverage)
            finishedDaC.append(n)
            
        hybridAverage = hybridTotal/10
        if hybridAverage>0:
            hybridLine.append(hybridAverage)
            finishedHybrid.append(n)
        plt.plot(finishedNaive, naiveLine, label = "naive algorithm")
        plt.plot(finishedDaC, DaCLine, label = "Divide and Conquer algorithm")
        plt.plot(finishedHybrid, hybridLine, label = "Hybrid algorithm")
        plt.legend()
        plt.xlabel("Polynomial Degree")
        plt.ylabel("time in milliseconds")
       
        plt.xscale('log')
        plt.yscale('log')
        plt.rcParams["figure.figsize"] = [16,9]
        plt.show()
    
    
    
firstStudy([2**n for n in range(1,25)])