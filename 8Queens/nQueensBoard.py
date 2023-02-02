# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 13:42:09 2022

@author: Graham Young
"""
import random
class NQueensBoard:
    """
    holds a board in the following format where n = board_size (default of 8):
        - - - - - - - - . . . n
        - - - - - - - -         
        - - - - - - - -
        - - - - - - - -
        - - - - - - - -
        - - - - - - - -
        - - - - - - - -
        - - - - - - - -
        .
        .
        .
        n
    with "Q" replacing each "-" where a queen exists. i.e. 
        - - - - Q - - -
        - - - - - - - Q
        - - Q - - - - -
        - - - - - - Q -
        Q - - - - - - -
        - - - - - Q - -
        - - - Q - - - -
        - Q - - - - - -
    for an 8 x 8 board with queen_posistions [4,1,6,2,8,3,5,7] 
    
    """

    def __init__(self, board_size=8, queen_positions=[]):
        self.board_size = board_size
        
        #create a board
        self.board = self.__create_empty_board__()
        
        #if queen_positions is the default get a random list otherwise use the passed argument
        if queen_positions == []:
            self.queen_positions = self.__get_random_queens__()
        else:
            self.queen_positions = queen_positions
            
        #put the queens into the board
        self.__set_queens__(self.queen_positions)
        
        #compute the hueristic
        self.heuristic = self.__compute_heuristic__()
        self.conflicts_for_each_queen = self.get_conflicts_for_each_queen()
        
    #get a list of length n (self.board_size) that has a random number between 1 and n
    def __get_random_queens__(self):
        queen_positions = []
        for i in range(self.board_size):
            queen_positions.append(random.randint(1,self.board_size))
        return queen_positions
    
    #create an n x n (n = self.board_size) board with "-" as the default value
    def __create_empty_board__(self):
        board = []
        for row in range(self.board_size):
            board.append(["-"]*self.board_size)           
        return board
    
    #set the queen positions in the board
    def __set_queens__(self, queen_positions):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if queen_positions[i]-1 == j:
                   self.board[j][i] = "♛"
                   break    
    
    #compute the heuristic based on the number of horizontal and diagonal conflicts
    def __compute_heuristic__(self):
       
        #check for horizontal conflicts
        conflicts_horizontal = self.__check_conflicts_horizontal__(self.queen_positions)
        #print(heuristic)
        #check for diagonal conflicts
        conflicts_diagonal = self.__check_conflicts_diagonal__(self.queen_positions)
        #print(heuristic)
        
        return sum(conflicts_diagonal) + sum(conflicts_horizontal)
                    
    def get_conflicts_for_each_queen(self):
        conflicts = []
        conflicts_horizontal = self.__check_conflicts_horizontal__(self.queen_positions)
        
        conflicts_horizontal_rev = self.__check_conflicts_horizontal__(self.queen_positions[::-1])[::-1]
        #print(heuristic)
        
        #check for diagonal conflicts
        conflicts_diagonal = self.__check_conflicts_diagonal__(self.queen_positions)
        
        conflicts_diagonal_rev = self.__check_conflicts_diagonal__(self.queen_positions[::-1])[::-1]
        #print(heuristic)
        
        for i, n in enumerate(conflicts_horizontal):
            conflicts.append(n + conflicts_diagonal[i] + conflicts_diagonal_rev[i] + conflicts_horizontal_rev[i])
            
            
        return conflicts
    
    def __check_conflicts_horizontal__(self, queen_positions):
        heuristic_horizontal = [0]*self.board_size
        #check if there are values that appear multiple times
        for i in range(len(queen_positions)):
            for j in range(i+1, len(queen_positions)):
                num_at_i = queen_positions[i]
                num_at_j = queen_positions[j]
                if num_at_i == num_at_j:
                    heuristic_horizontal[i] += 1
                
        return heuristic_horizontal
    
    
    def __check_conflicts_diagonal__(self, queen_positions):
        heuristic_diagonal = [0]*self.board_size
        #check if the abs of the difference in value minus the difference in index is 0
        #i.e. if theres a queen in row 1 column 0 and a queen in row 2 column 1
        #then 2-1 = 1-0 and that means they are on the same diagonal
        for i in range(len(queen_positions)):
            for j in range(i+1, len(queen_positions)):
                deltaValues = (queen_positions[i] - queen_positions[j])
                deltaIndices = (i - j)
                if abs(deltaValues) - abs(deltaIndices) == 0:
                    heuristic_diagonal[i] += 1
        return heuristic_diagonal
    
    
    #returns a new board of queen positions that has one random change in the list
    #a random index of queen_positions will be changed to a random number
    def get_successor(self):
        new_positions = self.queen_positions
        new_positions[random.randint(0, self.board_size-1)] = random.randint(1, self.board_size)
        return NQueensBoard(self.board_size, new_positions)
        
    def get_heuristic(self):
        self.heuristic =  self.__compute_heuristic__()
        return self.heuristic
    
    def get_queen_positions(self):
        return self.queen_positions  
    
    def __repr__(self):
        return repr((self.queen_positions, self.heuristic))
    
    def __str__(self):
        #print(self.queen_positions)
        string = ""
        for row in reversed(self.board):
            new_string = ' '.join(row) + "\n"
            string += new_string
        string += ' '.join([str(x) for x in self.queen_positions]) +"\n"
        string += "h = " + str(self.get_heuristic()) + "\n"
        string += ' '.join([str(x) for x in self.conflicts_for_each_queen])
        return string
    




if __name__ == '__main__':
    board = NQueensBoard()
    print(board)
    print(board.get_heuristic())
    board2 = NQueensBoard(8, [8,6,4,2,7,5,3,1])
    print(board2)
    print(board2.get_conflicts_for_each_queen())
    print(board2.get_heuristic())
    board3 = NQueensBoard(8, [5,1,8,4,2,7,3,6])
    print(board3)
    print(board3.get_conflicts_for_each_queen())
    print(board3.get_heuristic())
    board3 = NQueensBoard(8, [4,7,5,8,2,7,3,6])
    print(board3)
    print(board3.get_heuristic())
    print(board3.get_conflicts_for_each_queen())
    