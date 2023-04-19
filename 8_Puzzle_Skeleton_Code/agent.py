from __future__ import annotations
from board import Board
from collections.abc import Callable


'''
Heuristics
'''
def MT(board: Board) -> int:
    misplacedTiles = 0
    for i in range(1,9):
        if (i != board.state[(i-1)//3][(i-1)%3]): #(i-1)//3 is the expected row for number i, and (i-1)%3 is the expected column
            misplacedTiles+=1
    return misplacedTiles

def CB(board: Board) -> int:
    cityBlock = 0
    for i in range(1,9):
        j = 1
        while (i!=board.state[(j-1)//3][(j-1)%3]): #keep through the array until we find the tile -> it is guaranteed to happen so no infinite loop
            j+=1
        cityBlock += abs(((j-1)%3) - ((i-1)%3)) + abs(((j-1)//3) - ((i-1)//3)) #Adds the absolute difference in column with the absolute difference in row
        #print("i: " + str(i) + " j: " + str(j) + " cityBlock: " + str(cityBlock))
    return cityBlock


#I am going to be using a metric to try to put the "1" "2" and "3" tiles in position first
def NA(board: Board) -> int:
    prioritize123 = 0
    for i in range(1,4):
        if (i != board.state[0][i-1]): #only checking the first row
            prioritize123+=1
    return prioritize123



'''
A* Search 
'''
def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    




    return
