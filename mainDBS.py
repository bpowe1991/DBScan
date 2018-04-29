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
from copy import deepcopy
from itertools import chain

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
    
    #Plotting points of each cluster with defined color
    for cluster in clusters:
        x_values, y_values = split_coordinates(cluster)
        
        
        pl.ylabel('Y', {'color': 'y', 'fontsize': 16})
        pl.xlabel('X', {'color': 'y', 'fontsize': 16})
        if cluster != clusters[-1]:
            pl.plot(x_values, y_values, 'o')
        else:
            pl.plot(x_values, y_values, 'kx')

    
    pl.axis([0.0, 100.0, 0.0, 100.0])
    
    #Outputting graph
    pl.show()

#Function to find neighbor based on efs
def get_neighbors(point, points, efs):
    neighbors = []
    
    if points.__contains__(point):
        points.remove(point)

    #Add point to neighbors list if in range of efs
    for each in points:
        if calculate_euclidean(point, each) <= efs:
            neighbors.append(each)

    return neighbors

#Function to split points into center points and other points
def order_points(points, efs, min_pts):
    global center_points, other_points
    
    #Split points if number of neighbor meets threshold
    for point in points:
        if len(get_neighbors(point, deepcopy(points), efs)) >= min_pts:
            center_points.append(point)
        else:
            other_points.append(point)

#Function to combine center points if they are neighbors
def merge_centers(center_pts, efs):
    #List to hold clusters
    clusters =[]

    #Main loop for finding neighboring clusters
    for point in center_pts:
        found = False
        found_index = []
        neighbors = get_neighbors(point, deepcopy(center_pts), efs)
        neighbors.append(point)
        
        #Loop for combining intersecting center points
        for index in range(len(clusters)):
            
            #If center points have neighboring points, combine into a set
            if list(set(clusters[index]).intersection(set(neighbors))) != []:
                clusters[index] = list(set(clusters[index]).union(set(neighbors)))
                found = True
                found_index.append(index)
        
        #If no neighboring points intersect, append as new cluster
        if found == False:
            clusters.append(neighbors)
        
        #If more than one previous cluster overlaps, combine them together
        if len(found_index) > 1:
            for index in range(1,len(found_index)):
                clusters[found_index[0]] = list(set(clusters[found_index[0]]).union(set(clusters[found_index[index]])))
            found_index.pop(0)
            new_clusters = []
            
            #Create new list of clusters and replace old list
            for index in range(len(clusters)):
                if found_index.__contains__(index):
                    continue
                else:
                    new_clusters.append(clusters[index])
            clusters = new_clusters

    return clusters

#Function to combine potential border points to the clusters
def merge_borders(clusters, remaining_pts, efs):
    global center_points
    used_points = []

    for point in remaining_pts:

        for index in range(len(clusters)):
            neighbors = get_neighbors(point,deepcopy(center_points), efs)
            
            if list(set(clusters[index]).intersection(set(neighbors))) != []:
                clusters[index].append(point)
                used_points.append(point)
                break

    return clusters, used_points

  

efs = 2
min_pts = 0
seed = 50
list1 = generate_points(seed, 1.0, 100.0, 100)

print_points([list1])

center_points = []
other_points = []
order_points(list1, efs, min_pts)


print("Total Center Points:",len(center_points))
print("Total Other Points:",len(other_points))
clusters = merge_centers(center_points, efs)

print("Total Center Points:",len(center_points))
print("Total Other Points:",len(other_points))
print("Length of Clusters:",len(clusters))

print_points(clusters)
total = 0
for each in clusters:
    total+=len(each)

print("Total:",total)

clusters, points_to_remove = merge_borders(clusters, other_points, efs)

total = 0
for each in clusters:
    total+=len(each)

print("Total:", total)

other_points = list(set(other_points).difference(set(points_to_remove)))

print(len(other_points))
clusters.append(other_points)

print_points(clusters)





