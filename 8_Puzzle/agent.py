from __future__ import annotations
from board import Board
from collections.abc import Callable
import heapq
from typing import List


'''
Heuristics
'''
def BF(board: Board) -> int:
    return 0


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

#A Non-admissable heuristic that hates going left
def NA2(board: Board) -> int:
    children = board.next_action_states()
    for child in children:
        if (child[1]=="left"):
            return 10
    return 0



class Node:
    def __init__(self, myBoard: Board, myG: int, myH: int, myPreviousAction: str,myPath: List[str]):
        self.board = myBoard
        self.g = myG
        self.h = myH
        self.value = self.g + self.h
        self.previousAction = myPreviousAction
        self.path = []
        if myPath is not None and isinstance(myPath, list):
            self.path.extend(myPath)
            self.path.append(self.previousAction)

    def __lt__ (self, other):
        return self.value < other.value
    
    def conflictingAction(self,action: str) -> bool:
        if (action == "right" and self.previousAction == "left"):
            return True
        if (action == "left" and self.previousAction == "right"):
            return True
        if (action == "up" and self.previousAction == "down"):
            return True
        if (action == "down" and self.previousAction == "up"):
            return True
        return False


'''
A* Search 
'''
def a_star_search(board: Board, heuristic: Callable[[Board], int]):

    #This is the state of the first board position:
        #Its board is in the beginning state
        #Its value is the number of iterations so far (0) + the heuristic
        #Its path is nothing, since its the first one
    currentBoard = Node(board,0,heuristic(board),"", None)

    #We store the next nodes in a heap
        #Note that it begins empty, as we do not need to add the first board to the heap
        #since we would just immediately pop it
    heap = []

    #This defines the max number of nodes we are allowed to test before the function quits
    Nmax = 100000
    numberOfNodes = 0

    while(numberOfNodes<Nmax):
        numberOfNodes+=1

        #If we have found a solution, return the path
        if (currentBoard.board.goal_test()):
            # print("Solution: \n",currentBoard.board)
            print("Solution Found")
            print("Number of Nodes: ", str(numberOfNodes))
            # print("Solution : ",currentBoard.path)
            return currentBoard.path
        
        #Add Children to the heap

        for child in currentBoard.board.next_action_states():
            #print(child[1])
            #add each child which does not conflict with the action taken to get to the current board
            if (not currentBoard.conflictingAction(child[1])):
                #Creates a new child node for the child
                    #child[0] is the board state of the child
                    #curren....g+1 is the depth up to this point basically
                    #heur..child[0]) is the heuristic of the child
                    #child[1] is the "previous action" so that it can be stored
                    #curr...path adds the path we have gone through to get to this point
                heapq.heappush(heap, Node(child[0],currentBoard.g+1,heuristic(child[0]),child[1],currentBoard.path))

        #Update current board
        currentBoard = heapq.heappop(heap)
        

    #If we reach Nmax nodes without finding a solution, print this statement
    print("Failed to find solution in under "+ str(Nmax) + " nodes")
    return []
