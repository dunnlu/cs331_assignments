from board import Board
from agent import MT, CB, NA, a_star_search
import numpy as np
import time

def main():

    for m in [10,20,30,40,50]:
        for seed in range(0,10):
            # Sets the seed of the problem so all students solve the same problems
            board = Board(m, seed)
            
            start =  time.process_time()   
            '''
            ***********************************************
            Solve the Board state here with A*
            ***********************************************
            '''
            print(board)
            print("Misplaced Tiles: " + str(MT(board)))
            print("City Block Distance: " + str(CB(board)))
            print("Prioritize 123 Distance: " + str(NA(board)))
            



            end =  time.process_time()
            solution_cpu_time = end-start

if __name__ == "__main__":
    main()
