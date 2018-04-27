""""
Programmer: Briton A. Powe              Program Homework Assignment #2
Date: 4/18/18                           Class: Data Mining
Filename: bisectingKMeansEuclidean.py   Version: 1.7.3
------------------------------------------------------------------------
Program Description:
Generates k number of clusters in a Euclidean space and outputs cluster analysis.
**This Program uses Python 3.6.4***

"""


import random
import math
import matplotlib.pyplot as pl
import copy

#Function to create 20 points with a defined seed
def generate_points(seed, lower, upper, amount):
    points = []
    
    #Setting the seed
    random.seed(seed)

    #Creating points
    for _ in range(amount):
        x = round(random.uniform(lower, upper), 2)
        y = round(random.uniform(lower, upper), 2)

        points.append((x,y))
    
    return points

#Function to calculate Euclidean distance
def calculate_euclidean(point1, point2):
    distance = round(math.sqrt(((point1[0]-point2[0])**2)+((point1[1]-point2[1])**2)), 2)
    return distance

#Function to split x and y coordinates for screen output
def split_coordinates(points):
    x_values = []
    y_values = []

    for point in points:
        x_values.append(point[0])
        y_values.append(point[1])
    
    return x_values, y_values

#Function to output clusters in coordinate plane
def print_points(clusters):
    count = 0
    marker = ''
    
    #Plotting points of each cluster with defined color
    for cluster in clusters:
        x_values, y_values = split_coordinates(cluster)
        if count == 0:
            marker = 'bo'
        elif count == 1:
            marker = 'go'
        elif count == 2:
            marker = 'ro'
        elif count == 3:
            marker = 'ko'
        elif count == 4:
            marker = 'yo'
        pl.ylabel('Y', {'color': 'y', 'fontsize': 16})
        pl.xlabel('X', {'color': 'y', 'fontsize': 16})
        pl.plot(x_values, y_values, marker)
        count += 1
    
    pl.axis([0.0, 100.0, 0.0, 100.0])
    
    #Outputting graph
    pl.show()

