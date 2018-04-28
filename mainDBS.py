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


seed = 50
list1 = generate_points(seed, 1.0, 50.0, 100)

print_points([list1])

center_points = []
noise_points = []

def get_neighbors(point, points, efs):
    neighbors = []
    points.remove(point)

    for each in points:
        if calculate_euclidean(point, each) <= efs:
            neighbors.append(each)

    return neighbors



def order_points(points, efs, min_pts):
    global center_points, noise_points, noise_points
    for point in points:
        if len(get_neighbors(point, deepcopy(points), efs)) >= min_pts:
            center_points.append(point)
        else:
            noise_points.append(point)

    print("Total Points:",len(center_points)+len(noise_points))

def merge_centers(center_pts, efs):
    clusters =[]

    for point in center_pts:
        contain = False
        neighbors = get_neighbors(point, deepcopy(center_pts), efs)
        neighbors.append(point)

        if len(clusters) != 0:
            for index in range(len(clusters)):
                if list(set(clusters[index]).intersection(set(neighbors))) != []:
                    clusters[index] = list(set(clusters[index]).union(set(neighbors)))
                    contain = True
                    break
            if contain == False:
                clusters.append(neighbors)
        else:
            clusters.append(neighbors)

    return clusters

def merge_borders(clusters, remaining_pts, starting_list, efs):
    
    for point in remaining_pts:
        #print("Point:",point)
        for index in range(len(clusters)):
            neighbors = get_neighbors(point,deepcopy(starting_list), efs)
            #print("Neighbors:",neighbors)
            if list(set(clusters[index]).intersection(set(neighbors))) != []:
                #print(True)
                #print("Cluster Before:",clusters[index])
                clusters[index].append(point)
                #print("Cluster After:",clusters[index])
                break

    return clusters

    



order_points(list1, 10, 4)


#print(noise_points)
print("Total Center Points:",len(center_points))
clusters = merge_centers(center_points, 10)
print("Total Other Points:",len(noise_points))

total = 0
for each in clusters:
    total+= len(each)
print("Total in Cluster(Centers Only):", total)

# clusters = merge_borders(clusters, noise_points, list1, 5)
# total = 0
# total_cluster_pts = []
# for each in clusters:
#     total += len(each)
#     for point in each:
#         total_cluster_pts.append(point)
# print(total)
# print(len(total_cluster_pts))
# noise_points = list(set(noise_points).difference(total_cluster_pts))
# print("cluster and noise total:")
# print(len(total_cluster_pts)+len(noise_points))

# clusters.append(noise_points)
# print_points(clusters)









