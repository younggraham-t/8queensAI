# -*- coding: utf-8 -*-

"""

Created on Mon Oct  3 17:35:52 2022


@author: Graham Young

"""




from nQueensBoard import NQueensBoard
import math
from numpy.random import rand
import numpy
import random
import itertools
import time
import copy
import decimal


class __Algorithm():
    

    def __init__(self, board_size=8):
        self.board_size = board_size
        self.search_cost = 0
        self.solved = False
        self.board = NQueensBoard(board_size)
        self.visualize_list = []
        

    def run(self):
        pass


    def get_search_cost(self):
        return self.search_cost


    def is_solved(self):
        self.solved = self.board.get_heuristic() == 0
        return self.solved
    

    def get_board(self):
        return self.board
    

    def visualize(self):
        self.run()
        print("Visualization: ")
        for b in self.visualize_list:
            time.sleep(.1)
            print(b)
            

    def get_successor(self, board):
        self.search_cost += 1
        new_board = board.get_successor()
        return new_board


    def exit(self, current):
        self.board = current
        self.is_solved()
        self.visualize_list.append(copy.deepcopy(current))
        return self
    

    def __str__(self):
        string = self.board.__str__() + "\nheuristic " + str(self.board.get_heuristic())
        string += "\nis solved " + str(self.solved) + "\nsearch cost " + str(self.search_cost)
        return string
    
    
    
    
    
    
    

class GeneticAlgorithm(__Algorithm):
    

    def __init__(self, population=100, board_size=8):
        super().__init__(board_size)
        self.queen_positions = self.board.get_queen_positions()
        self.population = population
        self.boards = []
        #the highest number of non-attacking queens is defined by the sum of
        # 1 + 2 + 3 ... + n where n is the number of queens (the same as the size of
        # the board) in other words the nth triangle number which is given as (n(n+1))/2
        self.max_fitness = (self.board_size*(self.board_size+1))/2
        for i in range(self.population):
            self.boards.append(NQueensBoard(board_size))
        

        #print(self.board, "\nsearch_cost ", self.search_cost)

    

    #overrides abstract method

    def run(self):

        #find the fitnesses for each board

        board_fitness = self.find_fitness(self.boards)

        #a generation number to see which generation is being run

        generation = 0

        #print(board_fitness)

        #run until there is a board in the population that is solved 

        #i.e. the value (fitness) is equal to the max (the value for a solved board)

        while self.max_fitness not in board_fitness.values():

            generation += 1

            #replace the fitnesses with the probability of them being chosen

            fitness_percent = self.find_fitness_probability(board_fitness)

            #print(fitness_percent)
            

            #get as many children as the population i.e. if population is 10 then children

            #will have a length of 10

            children = self.get_children(fitness_percent)

            #print(children)
            

            #evaluate the children

            children_boards = self.convert_chromes_to_boards(children)

            new_board_fitness = self.find_fitness(children_boards)

            #print(new_board_fitness)
            

            #find the top [population size] # of boards

            board_fitness = self.find_survivors(board_fitness, new_board_fitness)

            #print(board_fitness)

            #the best is the first in the list because it is sorted in desc  order by fitness

            best = list(board_fitness.keys())[0]

            best_board = NQueensBoard(self.board_size, self.get_list_from_chrome(best))

            #add the best board to the visual

            self.visualize_list.append(best_board)
            

        self.board = best_board

        self.is_solved()
        return self
        

    def find_survivors(self, board_fitness, new_board_fitness):

        fitnesses = board_fitness.copy()

        fitnesses.update(new_board_fitness)

        fitnesses = self.sort_dict_by_values_desc(fitnesses)

        return dict(itertools.islice(fitnesses.items(), self.population))
    

    def convert_chromes_to_boards(self, chrome_list):

        boards = []

        for chrome in chrome_list:

            queen_positions = self.get_list_from_chrome(chrome)

            boards.append(NQueensBoard(self.board_size, queen_positions))
        return boards
        

    #find 2 parents and then breed them to get children equal to the size of the 

    #population

    def get_children(self, board_fitness):

        self.search_cost += self.population

        children = []

        #loop for half of pop size because children returns 2 values

        for n in range(math.floor(self.population/2)):

            parent1 = self.find_parent(board_fitness, 0)

            parent2 = self.find_parent(board_fitness, 1)

            children = self.breed(parent1, parent2, children)
        return children


    #choose a parent based on the probability of its fitness

    def find_parent(self, dictionary, start_ind):

        for i, key in enumerate(dictionary, start=start_ind):

            #initialize parent in case no value is found

            parent = key

            #check rand against the percentage

            curr_val = dictionary[key]

            if random.uniform(0, 0.25) < curr_val:

                return key
        return parent
    

    #breed 2 parents based on a random cross point and then randomly mutate the 

    #children

    def breed(self, parent1, parent2, children):

        #get lists for each parent (easier to edit)

        parent1 = self.get_list_from_chrome(parent1)

        parent2 = self.get_list_from_chrome(parent2)

        #print("p1", parent1, "p2", parent2)

        #cross the parents to get children

        cross_point = self.choose_cross_point()

        child1 = parent1[:cross_point] + parent2[cross_point:]

        child2 = parent1[cross_point:] + parent2[:cross_point]

        #print("c1", child1, "c2", child2)

        #mutate the children

        mutation_prob = 1/10

        self.mutate(child1, mutation_prob)

        self.mutate(child2, mutation_prob)

        #print("c1", child1, "c2", child2)

        #add the children to the list

        children.append(self.get_chromosome(child1))

        children.append(self.get_chromosome(child2))
        return children
    
        

    def mutate(self, child, mutation_prob):

        if rand() < mutation_prob:

            mutation = child[random.randint(0, self.board_size-1)] = random.randint(1, self.board_size)

            return mutation
        

    def choose_cross_point(self):

        #choose a point between 1 and board size

        return random.randint(1, self.board_size-1)
    

    def get_chromosome(self, queen_pos_list):

        string = ''.join([str(x) for x in queen_pos_list])

        return string
    

    def get_list_from_chrome(self, string):

        q_list = []

        for i in string:

            q_list.append(int(i))

        return q_list


    #finds the fitnesses for a list of boards and sorts it in descencding order

    def find_fitness(self, boards):

        board_fitness = {}

        for b in boards:

            board_q_p = self.get_chromosome(b.get_queen_positions())

            board_fitness[board_q_p] = self.__fitness__(board_q_p)

        #sort the board descending

        board_fitness = self.sort_dict_by_values_desc(board_fitness)
        return board_fitness
    

    def sort_dict_by_values_desc(self, dictionary):

        return {k: v for k, v in reversed(sorted(dictionary.items(), key=lambda item: item[1]))}
    

    #replaces the fitness value with its probability 

    def find_fitness_probability(self, board_fitness):

        sum_board_values = sum(board_fitness.values())

        fitness_percent = {}

        for f in board_fitness.keys():

            fitness_percent[f] = round((board_fitness[f]/sum_board_values), 2)
        return fitness_percent
    

    #fitness is based on the negative heuristic of the board + 28 to put it 

    #in the positive numbers

    #28 because that is the number of non attacking queen pairs in a solved board

    def __fitness__(self, chromosome):

        queen_pos_list = self.get_list_from_chrome(chromosome)

        board = NQueensBoard(len(queen_pos_list), queen_pos_list)

        #add 28 to put the numbers in the positive integers for easier use

        fitness = -board.get_heuristic() + self.max_fitness
        return fitness










class SimulatedAnnealing(__Algorithm):
    

    def __init__(self, max_time=50000, board_size=8):

        super().__init__(board_size)

        self.max_time = max_time

        self.initial_temp = 4000

        self.heuristic_list = []
        
    

    #overrides abstract method

    def run(self):

        current, curr_eval = self.set_curr_as_new(self.board, self.board.get_heuristic())

        temp = self.initial_temp

        for t in range(1, self.max_time):

            self.heuristic_list.append(curr_eval)

            temp *= 0.99

            #if temp is 0 end and return current 

            #this won't actually ever run with the current cooldown function

            if temp == 0:

                return self.exit(current)

            #get a succesor

            #new = self.get_successor(current)

            new = NQueensBoard(self.board_size)

            self.search_cost += 1

            new_eval = new.get_heuristic()

            #print("new eval ", new_eval, " curr eval ", curr_eval)

            #if the new eval is 0 then it is a solution so it should exit

            if new_eval == 0:

                current, curr_eval = self.set_curr_as_new(new, new_eval)

                return self.exit(current)
            

            #compute the change in value between new and current

            diff = new_eval - curr_eval

            #print("diff", diff, "temp",  temp)

            prob = self.check_prob(diff, temp)

            #print(prob)

            #save new if its better or based on probability

            if diff < 0 or prob:

                current, curr_eval = self.set_curr_as_new(new, new_eval)

                if t % 10 == 0:

                    self.visualize_list.append(copy.deepcopy(current))

                #print('>%d\n%s\n%d' % (t, current, curr_eval))

        return self.exit(current)

        #print("no")
    

    def check_prob(self, diff, temp):

        try:

            return random.uniform(0, 1) < math.e ** (-diff/temp) 

        except OverflowError:

            return False
    

    def set_curr_as_new(self, new, new_eval):

        current = new

        curr_eval = new_eval

        return current, curr_eval

    
    
    
    
    

class HillClimb(__Algorithm):    
    

    def __init__(self, board_size=8):

        super().__init__(board_size)

        self.num_successors = (self.board_size-1)*self.board_size
        
        

    #Overwrites abstract method

    def run(self):

        #get the cuurent and curr_eval

        current = self.board

        curr_eval = current.get_heuristic()

        best_successor, best_eval = self.get_best_successor(current)
        
        

        #run until theres a solution or a return statement is found

        while best_eval < curr_eval:

            current = best_successor

            curr_eval = best_eval

            self.visualize_list.append(copy.deepcopy(current))

            best_successor, best_eval = self.get_best_successor(current)
            

        self.board = current

        self.is_solved()
        return self
                
    

    def get_best_successor(self, current):

            successors = self.generate_successors(current)

            #[print(repr(x)) for x in successors]

            best_successor = successors[0]

            best_eval = best_successor.get_heuristic()

            for b in successors:
                

                candidate_eval = b.get_heuristic()

                #print(repr(b), best_eval, candidate_eval)

                if candidate_eval < best_eval:

                    best_successor = b

                    best_eval = candidate_eval
                
            

            #print("best", best_eval, "\n", best_successor)

            return best_successor, best_eval
                
                    
                    

    #gets the next successor of a board given the index of the column wanted

    #will generate a new board that has the same values except for the given column

    #having a value of n+1 that loops back to 1 if it exceeds the size of the board

    def generate_successors(self, board):

        successors = []

        board_q_p = board.get_queen_positions()
        

        for i in range(board.board_size):

            new_board_q_p = board_q_p[:]

            n_plus = new_board_q_p[i]
            

            for j in range(board.board_size-1):

                n_plus += 1 

                if n_plus > board.board_size:

                    n_plus = 1

                new_board_q_p[i] = n_plus

                #print(new_board_q_p)

                new_board = NQueensBoard(board.board_size, new_board_q_p)

                successors.append(copy.deepcopy(new_board))

                self.search_cost += 1
        return successors
    
    







 

class HillClimbRandomRestart(HillClimb):
    

    def __init__(self, board_size=8, num_restarts=25):

        super().__init__(board_size)

        self.num_restarts = num_restarts

        self.final_num_restarts = 0
    

    def run(self):

        current = HillClimb().run()

        #print("curr\n", current.visualize_list)
        

        self.visualize_list.append(copy.deepcopy(current.visualize_list))

        self.search_cost += current.search_cost

        current = current.board

        curr_eval = current.get_heuristic()
        

        if curr_eval == 0:

                return self.exit(current)

        for i in range(self.num_restarts):

            self.final_num_restarts += 1

            current = HillClimb().run()

            #print("curr\n", current.visualize_list)
            

            self.visualize_list.append(copy.deepcopy(current.visualize_list))

            self.search_cost += current.search_cost

            current = current.board

            curr_eval = current.get_heuristic()

            if curr_eval == 0:

                return self.exit(current)
                

        return self.exit(current)
    

    def visualize(self):
        self.run()

        print("Visualization: ")

        for i, b in enumerate(self.visualize_list):

            if i != len(self.visualize_list)-1 and i != 0:

                    print("Restarting:\n")

                    time.sleep(0.5)

            try:

                for j in b:

                    print(j)

                    time.sleep(0.25)


            except TypeError:
                continue

        print("Number of restarts: ", self.final_num_restarts)
    
    
    
    
    
    

class MinConflicts(__Algorithm):
    

    def __init__(self, board_size=8):
        super().__init__(board_size)
        self.num_restarts = 0
        
    
    def run(self):
        
        #run an iteration until it gets stuck
        current = self.run_one_iteration(self.board, self.board.get_heuristic())
        curr_eval = current.get_heuristic()
        #check if a solution was found
        if curr_eval == 0:
            return self.exit(current)
        #repaeat 25 times or until a solution is found
        for i in range(25):
            self.num_restarts += 1
            current = self.run_one_iteration(self.board, self.board.get_heuristic())
            curr_eval = current.get_heuristic()
            if curr_eval == 0:
                return self.exit(current)
            
        
        return self.exit(current)
    
    def run_one_iteration(self, current, curr_eval):
        random_queen = self.get_random_queen_in_conflict(current)
        best_successor, best_eval = self.get_best_successor(current, random_queen)
        
        while best_eval < curr_eval:
            current = best_successor
            curr_eval = best_eval
            #get the index of a random queen that has at least one conflict
            random_queen = self.get_random_queen_in_conflict(current)
            #find the board of the successors with the loswest number of conflicts at the random queen's column (index)
            best_successor, best_eval = self.get_best_successor(current, random_queen)
            self.visualize_list.append(copy.deepcopy(current))
        return current


            

    def get_best_successor(self, board, random_queen_in_conflict):
        successors = self.generate_successors(board, random_queen_in_conflict)
        #[print(repr(x)) for x in successors]
        best_successor = board
        best_eval = board.get_conflicts_for_each_queen()[random_queen_in_conflict]
        for b in successors:
            candidate_eval = b.get_conflicts_for_each_queen()[random_queen_in_conflict]
            #print(repr(b), best_eval, candidate_eval)
            if candidate_eval < best_eval:
                best_successor = b
                best_eval = candidate_eval
            
        #print("best", best_eval, "\n", best_successor)

        return best_successor, best_eval  
    
    #gets the index of a random queen that has a conflict
    def get_random_queen_in_conflict(self, board):
        #print(f"board\n {board}")
        conflicts = []
        #print(f"board conflicts {board.get_conflicts_for_each_queen()}")
        for i, n in enumerate(board.get_conflicts_for_each_queen()):
            if n > 0:
                conflicts.append(i)
        
        #print(f"conflicts: {conflicts}")
        random_queen_in_conflict = random.randint(0, len(conflicts)-1)
        #print(f"random queen {random_queen_in_conflict}")
        return random_queen_in_conflict
    

    def generate_successors(self, board, random_queen_in_conflict):
        successors = []
        board_q_p = board.get_queen_positions()
        new_board_q_p = board_q_p[:]
        n_plus = new_board_q_p[random_queen_in_conflict]  
        for i in range(board.board_size):
            self.search_cost += 1
            n_plus += 1
            if n_plus > board.board_size:
                n_plus = 1
            new_board_q_p[random_queen_in_conflict] = n_plus
            #print(f"new_board_q_p {new_board_q_p}")
            successors.append(NQueensBoard(board.board_size, new_board_q_p))
        #[print(x) for x in successors]
        return successors

    
    

if __name__ == '__main__':
    #print(HillClimb().run().board)
    #HillClimbRandomRestart().visualize()
    # yes = SimulatedAnnealing().run()
    # print(yes.board)
    # print(yes.search_cost)
    print(MinConflicts().run().board)
    