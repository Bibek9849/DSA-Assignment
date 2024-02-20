import numpy as np
import random

class AntColony:
    def __init__(self, distance_matrix, num_ants, evaporation_rate, alpha, beta):
        self.distance_matrix = distance_matrix
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.num_cities = len(distance_matrix)
        self.pheromone_matrix = np.ones((self.num_cities, self.num_cities))
        self.probabilities = np.zeros((self.num_cities, self.num_cities))
        self.best_tour = []
        self.best_tour_length = float('inf')

    def solve(self, max_iterations):
        for iteration in range(max_iterations):
            for ant in range(self.num_ants):
                visited = [False] * self.num_cities
                tour = []
                current_city = random.randint(0, self.num_cities - 1)
                tour.append(current_city)
                visited[current_city] = True

                for _ in range(self.num_cities - 1):
                    self.calculate_probabilities(current_city, visited)
                    next_city = self.select_next_city(current_city)
                    tour.append(next_city)
                    visited[next_city] = True
                    current_city = next_city

                tour_length = self.calculate_tour_length(tour)
                if tour_length < self.best_tour_length:
                    self.best_tour_length = tour_length
                    self.best_tour = tour

            self.update_pheromones()

    def calculate_probabilities(self, city, visited):
        total = 0.0
        for i in range(self.num_cities):
            if not visited[i]:
                self.probabilities[city][i] = (self.pheromone_matrix[city][i] ** self.alpha) * \
                                              ((1.0 / self.distance_matrix[city][i]) ** self.beta)
                total += self.probabilities[city][i]
            else:
                self.probabilities[city][i] = 0.0

        for i in range(self.num_cities):
            self.probabilities[city][i] /= total

    def select_next_city(self, city):
        probabilities = self.probabilities[city]
        r = random.random()
        cumulative_probability = 0.0
        for i in range(self.num_cities):
            cumulative_probability += probabilities[i]
            if r <= cumulative_probability:
                return i

    def update_pheromones(self):
        # Evaporation
        self.pheromone_matrix *= (1.0 - self.evaporation_rate)
        # Add new pheromones
        for i in range(self.num_ants):
            for j in range(self.num_cities - 1):
                city1 = self.best_tour[j]
                city2 = self.best_tour[j + 1]
                self.pheromone_matrix[city1][city2] += (1.0 / self.best_tour_length)
                self.pheromone_matrix[city2][city1] += (1.0 / self.best_tour_length)

    def calculate_tour_length(self, tour):
        length = 0
        for i in range(len(tour) - 1):
            length += self.distance_matrix[tour[i]][tour[i + 1]]
        length += self.distance_matrix[tour[-1]][tour[0]]
        return length

if __name__ == "__main__":
    distance_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    num_ants = 5
    evaporation_rate = 0.5
    alpha = 1.0
    beta = 2.0

    colony = AntColony(distance_matrix, num_ants, evaporation_rate, alpha, beta)
    colony.solve(1000)

    best_tour = colony.best_tour
    best_tour_length = colony.best_tour_length

    print("Best tour:", best_tour)
    print("Best tour length:", best_tour_length)
