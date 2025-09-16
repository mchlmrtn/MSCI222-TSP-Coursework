###QUESTION 2###
import sys
import datetime
import math
import numpy as np
import random

def read_tsp_file(file_name):
    file1 = open(file_name, 'r')  # open the file to [r]ead
    lines = file1.readlines()  # add file line by line to lines list
    file1.close()  # close the file

    location_count = int(lines[0])
    counter = 1
    locations = []

    while counter < len(lines) and lines[counter] is not None:
        current_line = lines[counter]
        parts = current_line.split(",")
        coordinate_x = float(parts[1])
        coordinate_y = float(parts[2])
        new_tuple = (coordinate_x, coordinate_y)
        locations.append(new_tuple)
        counter += 1

    return locations

def calculate_distance(loc1, loc2):
    return math.sqrt(math.pow(loc1[0] - loc2[0], 2) + math.pow(loc1[1] - loc2[1], 2))

def create_distance_matrix(locations):
    table = np.zeros((len(locations), len(locations)))
    for i in range(0, len(locations)):
        for j in range(0, len(locations)):
            table[i, j] = calculate_distance(locations[i], locations[j])
    return table

def tsp_local_search_1(tsp_solution, distance_matrix): #2opt method
    best_cost = tsp_solution[0]
    best_route = tsp_solution[1]
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route)):
                if j - i == 1: continue  # Skip adjacent edges
                new_route = best_route[:]
                new_route[i:j] = best_route[j - 1:i - 1:-1]  # Reverse the segment between i and j
                new_cost = 0
                for k in range(len(new_route) - 1):
                    new_cost += distance_matrix[new_route[k]][new_route[k + 1]]
                new_cost += distance_matrix[new_route[-1]][new_route[0]]
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_route = new_route
                    improved = True
                    break  # Improvement found, go to the outer loop
            if improved:
                break

    tsp_solution = [best_cost, best_route]
    return tsp_solution  # return the solution found (it returns what it receives, current_solution, right now)


def tsp_local_search_2(tsp_solution, distance_matrix): #city swap
    best_cost = tsp_solution[0]
    best_route = tsp_solution[1].copy()

    for i in range(len(best_route)):
        for j in range(i + 1, len(best_route)):
            new_route = best_route[:]
            new_route[i], new_route[j] = new_route[j], new_route[i]  # Swap two cities
            new_cost = 0
            for k in range(len(new_route) - 1):
                new_cost += distance_matrix[new_route[k]][new_route[k + 1]]
            new_cost += distance_matrix[new_route[-1]][new_route[0]]
            if new_cost < best_cost:
                best_cost = new_cost
                best_route = new_route

    tsp_solution = [best_cost, best_route]
    return tsp_solution  # return the solution found (it returns what it receives, current_solution, right now)


def nearest_neighbour_algorithm(distance_matrix):

    max_distance = np.max(distance_matrix)  # find maximum distance between any two locations

    list_length = len(distance_matrix)  # find the number of locations
    city_list = list(range(0, list_length))
    print(city_list)
    city_list_out = []  # list of cities the algorithm will return
    total_cost_out = 0
    modified_distance_matrix = np.copy(distance_matrix)  # copy of the distance matrix we will modify

    first_city = random.randrange(0, list_length)  # randomly select the first city
    city_list.remove(first_city)  # remove it from the cities not visited yet list
    city_list_out.append(first_city)  # add first city to the list of cities algorithm will return
    current_city = first_city  # set first city as the current city
    modified_distance_matrix[:, current_city] = 2 * max_distance * np.ones(list_length)  # modify the distance matrix

    while len(city_list) != 0:
        nearest_next_city = np.argmin(modified_distance_matrix[current_city, :])  # find the index of the next city
        total_cost_out += distance_matrix[current_city, nearest_next_city] # update the cost
        city_list.remove(nearest_next_city)  # update things (same as before)
        city_list_out.append(nearest_next_city)
        current_city = nearest_next_city
        modified_distance_matrix[:, current_city] = 2 * max_distance * np.ones(list_length)

    total_cost_out += distance_matrix[current_city, first_city]

    return total_cost_out, city_list_out  # this returns a tuple where item 0 is the cost and item 1 is the tour


def solve_tsp(file_name, max_iter): #solution for question 2
    city_locations = read_tsp_file(file_name)
    distance_table = create_distance_matrix(city_locations)

    file1 = open("output.txt", 'w')  # open a file to write

    best_solution = nearest_neighbour_algorithm(distance_table)  # initialise best_solution (with a feasible solution)

    for i in range(0, max_iter):
        inital = nearest_neighbour_algorithm(distance_table) #our inital solution for lcl srchs to start with
        current_solution_1 = tsp_local_search_1(inital, distance_table)
        current_solution_2 = tsp_local_search_2(inital, distance_table)
        if current_solution_1[0] < best_solution[0]:
            best_solution = current_solution_1
        if current_solution_2[0] < best_solution[0]:
            best_solution = current_solution_2

    file1.write(str(best_solution))  # write the best solution and its objective function to the output file
    file1.close()  # close the output file
    return best_solution

print(solve_tsp("ex5.txt", 10))