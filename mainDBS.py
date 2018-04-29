""""
Programmer: Briton A. Powe              Program Homework Assignment #3
Date: 4/29/18                           Class: Data Mining
Filename: mainDBS.py                    Version: 1.1.3
------------------------------------------------------------------------
Program Description:
Generates cluster using the DBScan algorithm. Generates points using a set seed.
**This Program uses Python 3.6.4***

"""
import random
import math
import matplotlib.pyplot as pl
from copy import deepcopy

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

#Function to calculate all Euclidean distances in a cluster
def calculate_distances_euclidean(main_point, points):
    euclidean_distances = []
 
    #Finding each distance
    for point in points:
        euclidean_distances.append(calculate_euclidean(main_point, point))

    return euclidean_distances

#Function for finding eps and min_pts
def calculate_k_nearest(list1): 
    #Lists for k nearest neighbor from 3-7
    dist_3_neighbor = []
    dist_4_neighbor = []
    dist_5_neighbor = []
    dist_6_neighbor = []
    dist_7_neighbor = []

    #Loop for calculating k nearest distances for each k
    for point in list1:
        point_list = deepcopy(list1)
        point_list.remove(point)
        distances = calculate_distances_euclidean(point, point_list)
        distances.sort()
        dist_3_neighbor.append(distances[2])
        dist_4_neighbor.append(distances[3])
        dist_5_neighbor.append(distances[4])
        dist_6_neighbor.append(distances[5])
        dist_7_neighbor.append(distances[6])

    #Sorting the k nearest distances
    dist_3_neighbor.sort()
    dist_4_neighbor.sort()
    dist_5_neighbor.sort()
    dist_6_neighbor.sort()
    dist_7_neighbor.sort()

    #Grouping all distances together
    dist_k_list = [dist_3_neighbor,
                dist_4_neighbor,
                dist_5_neighbor,
                dist_6_neighbor,
                dist_7_neighbor]

    #Adding a label for each distance in each k list
    count = 0
    for k in range(len(dist_k_list)):
        for x in range(len(dist_k_list[0])):
            dist_k_list[k][x] = (count, dist_k_list[k][x])
            count += 1
        count = 0

    #Outputting graph for all k lists
    print_points(dist_k_list)

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
    
    #List to keep track of which points were border points
    used_points = []

    for point in remaining_pts:
        #Getting neighboring points that are center points
        for index in range(len(clusters)):
            neighbors = get_neighbors(point,deepcopy(center_points), efs)
            
            #Adding border point to cluster with neighboring center point
            if list(set(clusters[index]).intersection(set(neighbors))) != []:
                clusters[index].append(point)
                used_points.append(point)
                break

    return clusters, used_points

#Main DBScan function
def DBScan(data_pts, efs, min_pts):
    #List for points
    global center_points, other_points

    #Ordering points
    order_points(data_pts, efs, min_pts)

    #Combining Neighboring clusters and outputing them
    clusters = merge_centers(center_points, efs)
    print_points(clusters)

    #Combining border points from other_points list
    clusters, points_to_remove = merge_borders(clusters, other_points, efs)
    
    #Removing border points from noise points
    other_points = list(set(other_points).difference(set(points_to_remove)))

    #Adding noise points as seperate cluster
    clusters.append(other_points)

    #Output final clustering result
    print_points(clusters)

#Start of 100 pts with 1.0 <= x,y <= 100.0
seed = 50
center_points = []
other_points = []
list1 = generate_points(seed, 1.0, 100.0, 100)

efs = 9
min_pts = 4

print_points([list1])
DBScan(list1, efs, min_pts)

#Start of 10 pts with 1.0 <= x,y <= 30.0 and 10 pts with 70.0 <= x,y <= 99.0
center_points = []
other_points = []
list1 = generate_points(seed, 1.0, 30.0, 10)
list2 = generate_points(seed, 70.0, 99.0, 10)
list1 = list(set(list1).union(set(list2)))

efs = 11
min_pts = 3

print_points([list1])
DBScan(list1, efs, min_pts)

#Start of 10 pts with 1.0 <= x,y <= 30.0 and 50 pts with 70.0 <= x,y <= 99.0
center_points = []
other_points = []
list1 = generate_points(seed, 1.0, 30.0, 10)
list2 = generate_points(seed, 70.0, 99.0, 50)
list1 = list(set(list1).union(set(list2)))

efs = 11
min_pts = 7

print_points([list1])
DBScan(list1, efs, min_pts)






