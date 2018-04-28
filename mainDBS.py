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


def get_neighbors(point, points, efs):
    neighbors = []
    points.remove(point)

    for each in points:
        if calculate_euclidean(point, each) <= efs:
            #print("Point 1:", point)
            #print("Point 2:", each)
            #print("Distance:",calculate_euclidean(point, each),"\n\n")
            neighbors.append(each)
    #print("Point:", point)
    #print("Neighbors:",neighbors)
    #print("Number of Neighbors:",len(neighbors))
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
        found = False
        found_index = []
        neighbors = get_neighbors(point, deepcopy(center_pts), efs)
        neighbors.append(point)
        for index in range(len(clusters)):
            if list(set(clusters[index]).intersection(set(neighbors))) != []:
                clusters[index] = list(set(clusters[index]).union(set(neighbors)))
                found = True
                found_index.append(index)
        if found == False:
            clusters.append(neighbors)
        if len(found_index) > 1:
            print(found_index)
            for index in range(1,len(found_index)):
                clusters[found_index[0]] = list(set(clusters[found_index[0]]).union(set(clusters[found_index[index]])))
            found_index.pop(0)
            print(found_index)
            print(len(clusters))
            new_clusters = []
            for index in range(len(clusters)):
                if found_index.__contains__(index):
                    continue
                else:
                    new_clusters.append(clusters[index])
            clusters = new_clusters

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

  

efs = 5
min_pts = 4
seed = 50
list1 = generate_points(seed, 1.0, 100.0, 300)

print_points([list1])

center_points = []
noise_points = []
order_points(list1, efs, min_pts)


#print(noise_points)
print("Total Center Points:",len(center_points))
print("Total Other Points:",len(noise_points))
clusters = merge_centers(center_points, efs)

print("Total Center Points:",len(center_points))
print("Total Other Points:",len(noise_points))
print("Length of Clusters:",len(clusters))

# print("\n\nCluster List")
# for each in clusters:
#     print(each)
# print("Number of Clusters:", len(clusters))
print_points(clusters)
# clusters = merge_borders(clusters, noise_points, list1, 5)
total = 0
for each in clusters:
    total+=len(each)

print("Total:",total)
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









