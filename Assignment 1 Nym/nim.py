# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"""import NumPy"""
import pylab
import matplotlib.pyplot as mpl
import time

def better_win(n):
    winArray = [True, False]
    for num in range(2,n+1):
        winArray.append(not(winArray[num-1] and winArray[num-2]))
    return winArray[n]
    

def win(n):
    if n==0:
        return True
    if n==1:
        return False
    return not(win(n-1) and win(n-2))

def move(n):
    if win(n-2)==False:
        return 2;
    if win(n-1)==False:
        return 1;
    return 0

def timer(n):
    tic = time.perf_counter()
    win(n)
    toc = time.perf_counter()
    return toc-tic

def timePlotter(n):
    data = []
    for i in range(0, n+1):
        data.append(timer(i))
    figure = mpl.figure()
    subplot = figure.add_subplot(1, 1, 1)
    
    line, = subplot.plot(data, color = 'red', lw=2)
    
    subplot.set_yscale('log')
    
    pylab.show()

"""
print("with 5 stones left you should remove: ")
print( move(5))
for x in range(0,10):
    if win(x)==better_win(x):
        print("match on ", x)
    else:
        print("error at " + str(x))
"""

timePlotter(48)