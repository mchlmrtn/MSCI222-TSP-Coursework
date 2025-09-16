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

def move_one_city_to_best_location(tsp_solution, distance_matrix):
    city_list_current = tsp_solution[1]
    cost_current = tsp_solution[0]

    list_length = len(city_list_current)  # find the number of locations
    selected_city_location = random.randrange(0, list_length)  # randomly select a location
    selected_city = tsp_solution[1][selected_city_location]  # find the city that will be moved

    cost_dif = 0  # initialise

    city_before = city_list_current[selected_city_location-1] # even negative python handles
    city_after = city_list_current[(selected_city_location + 1) % list_length]  # new index within range
    cost_dif -= distance_matrix[city_before, selected_city]  # city_before -> selected_city
    cost_dif -= distance_matrix[selected_city, city_after]  # selected_city -> city_after
    cost_dif += distance_matrix[city_before, city_after]  # city_before -> city_after

    city_list_out = tsp_solution[1].copy()  # city list to return
    city_list_out.remove(selected_city)  # remove randomly selected city from this list

    best_location = -1
    best_cost_dif = sys.maxsize
    for i in range(0, list_length-1):  # iterate over all possible locations
        city_before2 = city_list_out[i - 1]  # if the city is inserted to location i, city before
        city_after2 = city_list_out[i]  # if the city is inserted to location i, city after

        current_cost_dif = 0  # this variable shows how much cost difference does inserting to current location makes
        current_cost_dif += distance_matrix[city_before2, selected_city]  # city_before2 -> selected_city
        current_cost_dif += distance_matrix[selected_city, city_after2]  # selected_city -> city_after2
        current_cost_dif -= distance_matrix[city_before2, city_after2]  # city_before2 -> city_after2

        if current_cost_dif < best_cost_dif:  # if current is better (smaller), update
            best_cost_dif = current_cost_dif
            best_location = i

    cost_out = cost_current + cost_dif + best_cost_dif  # use the best solution to update
    city_list_out.insert(best_location, selected_city)  # use the best location to update

    return cost_out, city_list_out

def nearest_neighbour_algorithm(distance_matrix):
    max_distance = np.max(distance_matrix)
    list_length = len(distance_matrix)
    city_list = list(range(0, list_length))
    city_list_out = []
    total_cost_out = 0
    modified_distance_matrix = np.copy(distance_matrix)

    first_city = random.randrange(0, list_length)
    city_list.remove(first_city)
    city_list_out.append(first_city)
    current_city = first_city
    modified_distance_matrix[:, current_city] = 2 * max_distance * np.ones(list_length)

    while len(city_list) != 0:
        nearest_next_city = np.argmin(modified_distance_matrix[current_city, :])
        total_cost_out += distance_matrix[current_city, nearest_next_city]
        city_list.remove(nearest_next_city)
        city_list_out.append(nearest_next_city)
        current_city = nearest_next_city
        modified_distance_matrix[:, current_city] = 2 * max_distance * np.ones(list_length)

    total_cost_out += distance_matrix[current_city, first_city]

    return total_cost_out, city_list_out

def solve_tsp2(file_name, max_iter, max_iter2):
    random.seed(5)

    city_locations = read_tsp_file(file_name)
    distance_table = create_distance_matrix(city_locations)

    file1 = open("output.txt", 'w')

    previous_solution = nearest_neighbour_algorithm(distance_table)
    best_solution = previous_solution

    for i in range(0, max_iter):
        current_solution = nearest_neighbour_algorithm(distance_table)

        if current_solution[0] < best_solution[0]:
            best_solution = current_solution

        percentage_change = ((current_solution[0] - previous_solution[0]) / previous_solution[0]) * 100
        if percentage_change < 0:
            percentage_change = 0

        file1.write(f"Iteration {i+1}: Cost = {current_solution[0]}, Improvement = {percentage_change:.5f}%\n")

        previous_solution = current_solution

        start_time = datetime.datetime.now()

        for j in range(0, max_iter2):
            new_solution = move_one_city_to_best_location(current_solution, distance_table)

            if new_solution[0] < current_solution[0]:
                current_solution = new_solution
                if new_solution[0] < best_solution[0]:
                    best_solution = new_solution

            file1.write(f"{new_solution[0]} {best_solution[0]}\n")

        end_time = datetime.datetime.now()

        running_time = (end_time - start_time).total_seconds()
        print(f"Iteration {i + 1}: Cost = {current_solution[0]}, "
              f"Improvement = {percentage_change:.5f}%, "
              f"Running Time = {running_time:.7f} seconds")

    file1.close()
    return best_solution

solve_tsp2("ex5.txt", 10, 50)

