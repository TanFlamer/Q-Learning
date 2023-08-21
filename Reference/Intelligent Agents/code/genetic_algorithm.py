import math
import random
from operator import itemgetter


def get_rand_val(val):
    # Generate random value
    return random.randint(0, val) / (10000 / val)


def single_crossover(first_parent, second_parent):
    # Get crossover point
    crossover_point = random.randint(1, 7)
    # Perform crossover
    first_chromosome = first_parent[:crossover_point] + second_parent[crossover_point:]
    second_chromosome = second_parent[:crossover_point] + first_parent[crossover_point:]
    # Return chromosomes
    return [first_chromosome, second_chromosome]


def double_crossover(first_parent, second_parent):
    # Get crossover points
    first_point = random.randint(1, 3)
    second_point = random.randint(5, 7)
    # Perform crossover
    first_chromosome = first_parent[:first_point] + second_parent[first_point:second_point] + first_parent[
                                                                                              second_point:]
    second_chromosome = second_parent[:first_point] + first_parent[first_point:second_point] + second_parent[
                                                                                               second_point:]
    # Return chromosomes
    return [first_chromosome, second_chromosome]


class GeneticAlgorithm:
    def __init__(self, tuning_settings, fitness_function, fitness_settings):
        # Unpack tuning settings
        [self.crossover_rate, self.mutation_rate, self.single_double, self.roulette_tournament,
         self.population_size, self.elite, self.generation_size, self.best] = tuning_settings

        # Get fitness data
        self.fitness_function = fitness_function
        self.fitness_settings = fitness_settings

        # Fittest chromosomes
        self.fittest_chromosomes = []

    def run_algorithm(self):
        # Generate initial population
        population = self.generate_initial_population()

        # Run for 100 generations
        for generation in range(self.generation_size):
            # Evaluate population
            evaluated_population = self.evaluate_population(population)

            # Reevaluate fittest chromosome
            self.fittest_chromosomes = self.evaluate_fittest(evaluated_population)

            # Print fittest chromosomes
            print("Generation " + str(generation + 1) + ": " + str(self.fittest_chromosomes))

            # Add elite children to new population
            new_population = [x[0] for x in evaluated_population[:self.elite]]

            # Select new parents
            new_parents = self.selection(evaluated_population)

            # Generate new population
            for x in range(0, len(new_parents), 2):
                # Get new parents
                first_parent, second_parent = new_parents[x], new_parents[x + 1]

                # Crossover new chromosomes
                for chromosome in self.crossover(first_parent, second_parent):
                    # Mutate chromosome
                    self.mutate_chromosome(chromosome)

                    # Append new chromosome
                    new_population.append(chromosome)

            # Replace old population
            population = new_population

        # Return fittest chromosomes
        return [chromosome[0] for chromosome in self.fittest_chromosomes]

    def generate_initial_population(self):
        initial_population = []
        # Generate chromosome of population size
        for x in range(self.population_size):
            new_chromosome = []
            # Generate chromosome with 9 genes
            for y in range(3):
                new_chromosome.append(get_rand_val(100))
                new_chromosome.append(get_rand_val(100))
                new_chromosome.append(get_rand_val(10))
            initial_population.append(new_chromosome)
        # Return initial population
        return initial_population

    def evaluate_fittest(self, new_list):
        # Make and sort new list from old list
        temp_list = list(self.fittest_chromosomes)
        temp_list = temp_list + new_list
        temp_list.sort(key=lambda x: x[1], reverse=True)

        # Make and sort improved list
        improved_list = []
        [improved_list.append(x) for x in temp_list if x[0] not in [y[0] for y in improved_list]]
        improved_list.sort(key=lambda x: x[1])

        # Return fittest chromosomes
        return improved_list[:self.best]

    def evaluate_population(self, population):
        evaluated_population = []
        # Loop through chromosome in population
        for chromosome in population:
            # Evaluate chromosome fitness
            fitness = self.fitness_function(*self.fitness_settings, chromosome)[0]
            # Append chromosome with fitness
            evaluated_population.append((chromosome, fitness))
        # Sort evaluated population
        evaluated_population.sort(key=lambda x: x[1])
        # Return evaluated population
        return evaluated_population

    def selection(self, evaluated_population):
        if random.random() < self.roulette_tournament:
            new_parents = self.tournament_selection(evaluated_population)
        else:
            new_parents = self.roulette_selection(evaluated_population)
        return new_parents

    def tournament_selection(self, evaluated_population):
        new_parents = []
        # Tournament size is ceiling of 25% population size
        tournament_size = math.ceil(self.population_size / 4)
        for x in range(self.population_size - self.elite):
            # Randomly sample chromosome
            random_sample = random.sample(evaluated_population, tournament_size)
            # Choose chromosome with the lowest episode
            new_parent = min(random_sample, key=itemgetter(1))[0]
            new_parents.append(new_parent)
        return new_parents

    def roulette_selection(self, evaluated_population):
        new_parents = []
        total_fitness = sum(x[1] for x in evaluated_population)
        # Get probability of chromosome to be chosen
        probability = [1 - (x[1] / total_fitness) for x in evaluated_population]
        for x in range(self.population_size - self.elite):
            # Randomly choose chromosome by probability
            new_parent = random.choices(evaluated_population, weights=probability)[0][0]
            new_parents.append(new_parent)
        return new_parents

    def crossover(self, first_parent, second_parent):
        if random.random() < self.crossover_rate:
            # No crossover occurs
            chromosomes = [first_parent.copy(), second_parent.copy()]
        else:
            # Single or double crossover
            func = single_crossover if random.random() < self.single_double else double_crossover
            chromosomes = func(first_parent, second_parent)
        return chromosomes

    def mutate_chromosome(self, chromosome):
        # Loop through all 9 genes
        for x in range(9):
            if random.random() < self.mutation_rate:
                # Random value depends on gene position
                gene_position = x % 3
                max_val = 10 if gene_position == 2 else 100
                chromosome[x] = get_rand_val(max_val)
