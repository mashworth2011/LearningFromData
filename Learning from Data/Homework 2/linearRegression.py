#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 16:52:45 2019

@author: markashworth
"""

"""
Program to be used to answer the Linear Regression questions Q(5-7) in Homework
2 of the learning from Data course. 
"""
import random
import matplotlib.pyplot as plt
import numpy as np

class generateLabels(object):
    """
    Our output data (or labels) are generated by using the target function 
    (evalPoint) on each point. Target function is created by picking two 
    random points x1 and x2, and drawing the line that passes through them.
    """
    def __init__(self, N):
        """
        N is the sample size
        x1 is the first point 
        x2 is the second point
        """
        self.N = N
        self.x1 = [random.choice([-1,1])*random.random(), random.choice([-1,1])*random.random()]
        self.x2 = [random.choice([-1,1])*random.random(), random.choice([-1,1])*random.random()]
        self.m, self.b = self.linearEq()
        self.mappedVec = self.mapVector() # Dict of input data (keys) and labels (values)
        
    def linearEq(self):
        """
        Generate linear equation based on points
        """
        m = (self.x2[1] - self.x1[1])/(self.x2[0] - self.x1[0])
        b = self.x1[1] - m*self.x1[0]
        return m, b
    
    def visual(self):
        """
        Visualisation based used equation on x-coordinates -1, and 1. 
        """
        y1 = self.m*-1 + self.b
        y2 = self.m*1 + self.b
        plt.plot([-1, 1], [y1, y2], 'r-')
        plt.xlim(-1, 1); plt.ylim(-1, 1)
    
    def evalPoint(self, x): # TARGET FUNCTION
        """
        Evaluate a single data point, x, given the linear equation splitting up
        the domain. This evalutaion is what constitutes the TARGET FUNCTION. 
        """
        if  x[1] < self.m*x[0] + self.b:
            return -1
        else:
            return 1
    
    def mapVector(self):
        """
        Evalutaion of N vector of input data points based on the target function. That is, 
        given some input data we want to map outputs (or labels) to them. The mapping
        is expressed as a dictionary with keys of input points and values of outputs.
        """
        return {i:self.evalPoint(i) for i in \
               [(random.choice([-1,1])*random.random(), random.choice([-1,1])*random.random())\
               for i in range(self.N)]}
               
               
class linearRegression(object):
    """
    Perform linear regression to find the target function. This amounts to 
    finding the optimal weights that minimise the in sample square error. This
    can be done exactly for the case of linear regression. 
    """
    def __init__(self, N):
        """
        X is the input data with the addition of x0 = 1
        y is the output data or labels
        w are the weights generated by the linear regression algorithm
        """
        self.N = N
        self.data = generateLabels(self.N) # generate input/output data 
        self.X = np.array([[1]+list(i) for i in self.data.mappedVec.keys()])
        self.y = np.array(list(self.data.mappedVec.values()))
        self.w = self.calcWeights()
        self.Ein = self.calcEin()
        
    def calcWeights(self):
        """
        Calculate the weights using the algorithm based on minimising the least
        squared error (involves calculating the psuedo-inverse matrix of X)
        """
        self.pinvX = np.linalg.pinv(self.X)
        return np.dot(self.pinvX, self.y)
        
    def calcEin(self):
        """
        Calculate the in sample error.
        """
        return (1/self.N)*np.linalg.norm(np.dot(self.X, self.w) - self.y, 2)
        

# Question 5    
def simulateLinReg(N, I):
    """
    Simulate the linear regression problem. Want to generate a dictionary of 
    g functions : Ein.
    N is the sample size
    I is the number of experiments 
    """
    lRdict = {}
    for i in range(I):
        lR = linearRegression(N)
        lRdict.update({tuple(lR.w):lR.Ein})
    return lRdict   


# Question 6
def EoutOfSample(N, lRdict):
    """
    Using the output from the simulateLinReg function test your collection of
    approximated target functions, g, to get the out of sample error for 1000
    new points of data. 
    """
    newDat = generateLabels(1000)
    X = np.array([[1]+list(i) for i in newDat.mappedVec.keys()])
    y = np.array([v for v in newDat.mappedVec.values()])
    Eout = []
    for w in lRdict.keys():
        Eout.append((1/N)*np.linalg.norm(np.dot(X, np.array(w)) - y, 2))
    return Eout
        

        