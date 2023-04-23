from board import Board
from agent import BF, MT, CB, NA, a_star_search
import numpy as np
import time

def main():
    
    for m in [10,20,30,40,50]:
        total_cpu_time = 0
        total_solution_length = 0
        problems_solved = 0
        print("\n\n\nFor m = " + str(m) + ":\n\n")
        for seed in range(0,10):
            # Sets the seed of the problem so all students solve the same problems
            board = Board(m, seed)
            
            start =  time.process_time()   
            '''
            ***********************************************
            Solve the Board state here with A*
            ***********************************************
            '''
            solution_string_array = a_star_search(board,NA)

            total_solution_length+= len(solution_string_array)

            if (len(solution_string_array) >0):
                problems_solved += 1 

            
            end =  time.process_time()
            solution_cpu_time = end-start
            total_cpu_time += solution_cpu_time
            print("CPU time: ", str(solution_cpu_time))

        #Info for each of the plots 
        print("\n\nInfo for m = " + str(m) + ":")
        print("\nProblems Solved: " + str(problems_solved) + "/10 = " + str(problems_solved/10)) 
        #Number of search nodes generated was printed out within the a* search function
        #We were unfortunately unable to find a way to automate the total nodes
        #Instead, we had to add the ten results for each m
        print("Number of Search Nodes Generated?") 
        print("Average CPU Time: " + str(total_cpu_time/10))
        if (problems_solved>0):
            print("Average Solution Length: " + str(total_solution_length/problems_solved) + "\n\n\n")
        else:
            print("Average Solution Length : N/A\n\n\n")





if __name__ == "__main__":
    main()
