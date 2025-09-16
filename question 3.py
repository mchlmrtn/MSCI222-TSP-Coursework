import sys
import math
import numpy as np
import random


def read_tsp_file(file_name):
    file1 = open(file_name, 'r')
    lines = file1.readlines()
    file1.close()

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

# Local search algorithm 1: 2-opt
def local_search1(tsp_solution, distance_matrix):
    def local_search1(tsp_solution, distance_matrix):
        best_cost = tsp_solution[0]
        best_route = tsp_solution[1].copy()
        improved = False

        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route)):
                new_route = best_route[:]
                new_route[i:j] = best_route[j - 1:i - 1:-1]
                new_cost = sum(distance_matrix[new_route[k]][new_route[k + 1]] for k in range(len(new_route) - 1))
                new_cost += distance_matrix[new_route[-1]][new_route[0]]

                if new_cost < best_cost:
                    best_cost = new_cost
                    best_route = new_route
                    improved = True
                    break
            if improved:
                break

        return best_cost, best_route


# Local search algorithm 2: Swap cities
def local_search2(tsp_solution, distance_matrix):
    best_cost = tsp_solution[0]
    best_route = tsp_solution[1].copy()

    for i in range(len(best_route) - 1):
        for j in range(i + 1, len(best_route)):
            new_route = best_route.copy()
            new_route[i], new_route[j] = new_route[j], new_route[i]
            new_cost = sum(distance_matrix[new_route[k]][new_route[k + 1]] for k in range(len(new_route) - 1))
            new_cost += distance_matrix[new_route[-1]][new_route[0]]

            if new_cost < best_cost:
                best_cost = new_cost
                best_route = new_route

    return best_cost, best_route



# Local search algorithm 3: Simple city move
def local_search3(tsp_solution, distance_matrix):
    best_cost = tsp_solution[0]
    best_route = tsp_solution[1].copy()

    for i in range(len(best_route)):
        for j in range(len(best_route)):
            if i != j:
                new_route = best_route.copy()
                city = new_route.pop(i)
                new_route.insert(j, city)
                new_cost = sum(distance_matrix[new_route[k]][new_route[k + 1]] for k in range(len(new_route) - 1))
                new_cost += distance_matrix[new_route[-1]][new_route[0]]

                if new_cost < best_cost:
                    best_cost = new_cost
                    best_route = new_route

    return best_cost, best_route



# Variable Neighbourhood Search
def variable_neighbourhood_search(file_name, max_iter, max_iter2):
    city_locations = read_tsp_file(file_name)
    distance_table = create_distance_matrix(city_locations)
    best_solution = nearest_neighbour_algorithm(distance_table)

    # Initialize the probabilities for selecting each local search algorithm
    probabilities = [1 / 3, 1 / 3, 1 / 3]
    local_search_functions = [local_search1, local_search2, local_search3]

    for i in range(max_iter):
        rnd = random.random()
        cumulative_probability = 0
        for index, prob in enumerate(probabilities):
            cumulative_probability += prob
            if rnd < cumulative_probability:
                current_solution = local_search_functions[index](best_solution, distance_table)
                if current_solution and current_solution[0] < best_solution[0]:
                    best_solution = current_solution
                    # Update probabilities
                    improvement = 0.1 * (1 - probabilities[index])
                    probabilities = [(p - improvement / 2 if i != index else p + improvement) for i, p in enumerate(probabilities)]
                    # Normalize the probabilities to sum to 1
                    total = sum(probabilities)
                    probabilities = [p / total for p in probabilities]
                break  # Break as we have selected an algorithm

        print(f"Iteration {i + 1}: Best Cost = {best_solution[0]}, Probabilities = {probabilities}")

    return best_solution

# Run VNS for TSP
best_tsp_solution = variable_neighbourhood_search("ex5.txt", 10, 50)
print(f"Best solution found: {best_tsp_solution}")