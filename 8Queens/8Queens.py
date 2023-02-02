# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 16:33:18 2022

@author: Graham Young
"""

from algo import *
import traceback

"""
to do:
    
"""
        
class MassGenerate:
    """
    Takes an input number of boards to run and runs each algorithm that many times
    Then prints out the average search cost and percent solved for each algorithm
    """
    def __init__(self):
        self.num = 0
        self.algorithm_types = []
        self.algorithm_types.append(MinConflicts)
        self.algorithm_types.append(HillClimb)
        self.algorithm_types.append(HillClimbRandomRestart)
        self.algorithm_types.append(GeneticAlgorithm)
        self.algorithm_types.append(SimulatedAnnealing)
        
        
    
    def run(self):
        
        #get input
        user_input = self.__get_input__()
        for a in self.algorithm_types:
            self.__run__(user_input, a)
            
    
    def __get_input__(self):
        retry = True
        while retry == True:
            retry = False
            try:
                user_input = int(input("Enter the number of boards you wish to generate: "))
                print()
            except ValueError:
                #traceback.print_exc()
                print("invalid input")
                retry = True
        return user_input
    
    def __output__(self, algorithm_list, algorithm_type):
        print("\r", end="")
        print(algorithm_type.__name__, ": ", end="")
        self.__get_search_costs_and_avg(algorithm_list)
    
    def __run__(self, num_boards, algorithm_type):
        
        # print("Running ", end="")
        algorithm_list = []
        
        #run each algorithm for the amount of times the user specified
        for i in range(num_boards):
            algorithm_list.append(algorithm_type().run())
            #visual to show its running
            if i % 5 == 0:
                print(".", end="")
            
        self.__output__(algorithm_list, algorithm_type)
        
    def __get_search_costs_and_avg(self, algorithm_list):
        #get the search costs for the algorithms
        search_costs = []
        solved_list = []
        for a in algorithm_list:
            search_costs.append(a.get_search_cost())
            solved_list.append(a.solved)
        #find the average
        #print(solved_list)
        avg_cost = sum(search_costs)/len(search_costs)
        #find the number of solved algos
        trues = 0
        for i in solved_list:
            if i:
                trues += 1
        #calculate the percent of solved boards
        solved_percent = (trues/len(search_costs))*100
        print("average cost: %.1f, percent solved: %.1f"  % (avg_cost, solved_percent))
        
   
class Visualize:
    """
    Takes an input and runs the selected algorithm then prints out the best board 
    from each iteration for that algorithm
    """   
    def __init__(self):
        genetic_pop = 25
        s_a_time = 100000
        self.options = {}
        self.options["S"] = SimulatedAnnealing(s_a_time)
        self.options["G"] = GeneticAlgorithm(genetic_pop)
        self.options["H"] = HillClimb()
        self.options["HR"] = HillClimbRandomRestart()
    
    def run(self):
        prompt = "Type \n 'S' for SimulatedAnnealing,\n "
        prompt += "'G' for Genetic,\n "
        prompt += "'H' for HillClimb,\n  "
        prompt += "'HR' for HillClimb with Random Restart\n "
        prompt += "or 'Q' to Quit:\n"
        
        retry = True
        while retry == True:
            retry = False
            user_choice = input(prompt)
            try:
                if user_choice.casefold() == 'q'.casefold():
                    return
                else:
                    self.options.get(user_choice.upper()).visualize()
            except AttributeError:
                #traceback.print_exc()
                print("invalid input")
                retry = True
        
def main():
    options = {"V": Visualize(), "M": MassGenerate()}
    retry = True
    while retry:
        retry = False
        user_input = input("Type 'V' to Visualize one board or 'M' to Mass Generate or 'Q' to Quit:\n")
        try:
            if user_input.casefold() == 'q'.casefold():
                break
            else:
                options.get(user_input.capitalize()).run()
        except AttributeError:
            #traceback.print_exc()
            print("invalid input")
            retry = True
            
if __name__ == '__main__':
    main()