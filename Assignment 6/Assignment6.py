# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 18:27:24 2021

@author: bdpac
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import datetime
import random
import multiprocessing
import time

#Fast Fourier Transforms! Utilizing mathematical witchcraft*, we prepare a polynomial of size 2^n
#to be multiplied with another polynomial of the same size. More witchcraft is needed to reverse the
#process after the multiplication, producing the actual answer.
#*-complex number multiplication.
def fft(polynomial, omega,n):
    #base case    
    if n == 1:
        return polynomial
    else :
    #split into even and odd
        Podd = np.array([polynomial[i] for i in range(1,n,2)])
        Peven = np.array([polynomial[i] for i in range(0,n,2)])
    #square values in X
    omega2 = np.array([omega[n]**2 for n in range(int(n/2))])
    #compute values for even/odd
    solEven = fft(Peven, omega2, int(n/2))
    solOdd = fft(Podd, omega2, int(n/2))
    #construct solution
    result1 = np.array([solEven[i] + omega[i]*solOdd[i] for i in range(int(n/2))])
    result2 = np.array([solEven[j] - omega[j]*solOdd[j] for j in range(int(n/2))])    
    return np.append(result1, result2)


#finds the nth root of unity, for use in the fft.

def unityRoots(n):
    omega = complex(math.cos(2*math.pi/n), math.sin(2*math.pi/n))
    return np.array([omega**i for i in range(n)])

#used for the inverse version of fft
def inverseUnityRoots(n):
    omega = complex(math.cos(2*math.pi/n), -1*math.sin(2*math.pi/n))
    return np.array([omega**i for i in range(n)])

def padder(poly, size):
    zeroArray = np.zeros(size, dtype = np.int16)
    return np.append(poly, zeroArray)
   
def multiplyFFT(poly1, poly2):
    size = len(poly1)
    N0 = padder(poly1, size)
    N1 = padder(poly2, size)
    size2 = size*2
    omega = unityRoots(size2)
    S0 = fft(N0, omega, size2)
    S1 = fft(N1, omega, size2)

    complexSol = np.array([S0[i]*S1[i] for i in range(size2)])
    invOmega = inverseUnityRoots(size2)
    sol = fft(complexSol, invOmega, size2)
    solution = np.array([i.real/(size2) for i in sol])
    return np.real(solution)
   
def randListSizeN(n):
    maxNum = (2**11)-1
    return np.array([random.randint(0,maxNum) for _ in range(n)])

def naivePolyMult (P, Q):
    resultSize = len(P) +len(Q)
    result = np.zeros(resultSize)
    for i in range(0, resultSize):
        for j in range(i+1):
            if len(P)>j and len(Q)>i-j:
                result[i]+=P[j]*Q[i-j]
    return result


def polyMult(P,Q):
    baseLength = P.size
    result = np.zeros(baseLength*2)
    if baseLength == 1:
        result[0]=P[0]*Q[0]
    else:
        splitP = np.split(P,2)
        splitQ = np.split(Q,2)
        spacer = np.zeros(baseLength)
        shortSpacer = np.zeros(int(baseLength/2))
        U = polyMult(splitP[0], splitQ[0])
        Y = polyMult(np.add(splitP[0], splitP[1]), np.add(splitQ[0], splitQ[1]))
        Z = polyMult(splitP[1], splitQ[1])
        YsubUZ = np.subtract(Y, np.add(U,Z))
        term1 = np.append(U , spacer)
        term2 = np.append(
            np.append(shortSpacer , YsubUZ) , shortSpacer)
        term3 = np.append(spacer , Z)
       
        result = np.add(result,
                        np.add(term1,
                               np.add(term2, term3)))
    return result

def verifier(n):
    for _ in range(5):
        poly1 = randListSizeN(n)
        poly2 = randListSizeN(n)
        naiveTest = naivePolyMult(poly1, poly2)
        quickerTest = polyMult(poly1, poly2)
        fftTest = multiplyFFT(poly1, poly2)
        print(naiveTest,"  ",quickerTest,"   ",fftTest)
       
verifier(4)

def timer(func, input1, input2, timeLimit):
    startTime = datetime.datetime.now()
    f = multiprocessing.Process(target = func, args = (input1, input2))
    f.start()
    f.join(timeLimit)
    
    if f.is_alive():
        f.terminate()
        return -1
    
    endTime = datetime.datetime.now()
    elapsed = endTime - startTime
    return elapsed.total_seconds()*1000

def triPlotter(sizes, timeLimit):
    naiveLine = []
    polyLine = []
    fftLine = []
    finishedNaive = []
    finishedPoly = []
    finishedFFT = []
    continueNaive = True
    continuePoly = True
    continueFFT = True
   
    for n in sizes:
        
        testArr1 = randListSizeN(n)
        testArr2 = randListSizeN(n)
        
        if continueNaive :
            naiveTime = timer(naivePolyMult, testArr1, testArr2, timeLimit)
            if naiveTime == -1:
                print("naive Algorithm failed at {}".format(n))
                continueNaive = False
            if naiveTime > 0 :
                naiveLine.append(naiveTime)
                finishedNaive.append(n)
        
        if continuePoly :
            polyTime = timer(polyMult, testArr1, testArr2, timeLimit)
            if polyTime == -1:
                print("less naive algorithm failed at {}".format(n))
                continuePoly = False
            if polyTime > 0:
                polyLine.append(polyTime)
                finishedPoly.append(n)
               
        if continueFFT :
            fftTime = timer(multiplyFFT, testArr1, testArr2, timeLimit)
            if fftTime == -1:
                print("FFT algorithm failed at {}".format(n))
                continueFFT = False
            if fftTime > 0:
                fftLine.append(fftTime)
                finishedFFT.append(n)
        if not (continueNaive or continuePoly or continueFFT):
            break;
            
    plt.plot(finishedNaive, naiveLine, label = "naive algorithm")
    plt.plot(finishedPoly, polyLine, label = "less naive algorithm")
    plt.plot(finishedFFT, fftLine, label = "FFT algorithm")
    
    plt.legend()
    plt.xlabel("Polynomial Degree")
    plt.ylabel("time in milliseconds")
       
    plt.xscale('log')
    plt.yscale('log')
    plt.rcParams["figure.figsize"] = [16,9]
    plt.show()
    
triPlotter([128*(2**i) for i in range(10)], 15)