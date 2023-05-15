from OthelloBoard import OthelloBoard

class Player:
    """Base player class"""
    def __init__(self, symbol):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol
    
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    """Human subclass with text input in command line"""
    def __init__(self, symbol):
        Player.__init__(self, symbol)
        self.total_nodes_seen = 0

    def clone(self):
        return HumanPlayer(self.symbol)
        
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class AlphaBetaPlayer(Player):
    """Class for Alphabeta AI: implement functions minimax, eval_board, get_successors, get_move
    eval_type: int
        0 for H0, 1 for H1, 2 for H2
    prune: bool
        1 for alpha-beta, 0 otherwise
    max_depth: one move makes the depth of a position to 1, search should not exceed depth
    total_nodes_seen: used to keep track of the number of nodes the algorithm has seearched through
    symbol: X for player 1 and O for player 2
    """
    def __init__(self, symbol, eval_type, prune, max_depth):
        Player.__init__(self, symbol)
        self.eval_type = int(eval_type)
        self.prune = prune
        self.max_depth = int(max_depth) 
        self.max_depth_seen = 0
        self.total_nodes_seen = 0
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'


    def terminal_state(self, board: OthelloBoard):
        # If either player can make a move, it's not a terminal state
        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_legal_move(c, r, "X") or board.is_legal_move(c, r, "O"):
                    return False 
        return True 


    def terminal_value(self, board: OthelloBoard):
        # Regardless of X or O, a win is float('inf')
        state = board.count_score(self.symbol) - board.count_score(self.oppSym)
        if state == 0:
            return 0
        elif state > 0:
            return float('inf')
        else:
            return -float('inf')


    def flip_symbol(self, symbol):
        # Short function to flip a symbol
        if symbol == "X":
            return "O"
        else:
            return "X"


    #returns the utility value, column, and row of the best move 
    #symbol will always be self.symbol
    def max_value(self,board: OthelloBoard,alpha,beta,depth): #returns (value,col,row) 
        self.total_nodes_seen+=1
        if (not board.has_legal_moves_remaining(self.symbol) or depth == self.max_depth):
            return (self.eval_board(board), 0, 0) #returns the utility value and an arbitrary "move"
        bestValue = -17
        bestColumn = 0
        bestRow = 0
        successors = self.get_successors(board,self.symbol)
        for (newBoard,c,r) in successors:
            tempValue = self.min_value(newBoard,alpha,beta,depth+1)
            if (tempValue > bestValue):
                bestValue = tempValue
                bestColumn = c
                bestRow = r
            if (bestValue >= beta): #we can prune this branch
                return (bestValue,c,r) #this branch will be pruned
            if (bestValue> alpha): #we have found a better move
                alpha = bestValue
        return (bestValue,bestColumn,bestRow)

    #returns the utility value, column, and row of the opponents best move 
    #symbol will always be self.oppSym
    def min_value(self,board: OthelloBoard,alpha,beta,depth): #returns (value,col,row)
        self.total_nodes_seen+=1
        if (not board.has_legal_moves_remaining(self.oppSym) or depth == self.max_depth):
            return self.eval_board(board) #returns the utility value and an arbitrary "move"
        oppBestValue = 17
        successors = self.get_successors(board,self.oppSym)
        for (newBoard,c,r) in successors:
            (tempValue,tempR,tempC) = self.max_value(newBoard,alpha,beta,depth+1)
            if (tempValue < oppBestValue):
                oppBestValue = tempValue
            if (oppBestValue <= alpha): #we can prune this branch
                return oppBestValue #this branch will be pruned
            if (oppBestValue < beta): #we have found a better move
                beta = oppBestValue
        return oppBestValue


    def alphabeta(self, board: OthelloBoard):
        # Write minimax function here using eval_board and get_successors
        # type:(board) -> (int, int)
        col, row = 0, 0
        (value, col, row) = self.max_value(board,-17,17,0)
        return (col, row)



    """THIS IS THE BUGGY PART OF THE CODE"""
    def eval_board(self, board: OthelloBoard):
        # Write eval function here
        # type:(board) -> (float)
        value = 0
        #print("My eval type: " +  str(self.eval_type) + " typeof evaltype: " + str(type(self.eval_type)))
        if (self.eval_type == 0): #Piece Difference
            #print("Calcing piece difference")
            myPieces = 0
            opposingPieces = 0
            for c in range(board.get_num_cols()):
                for r in range(board.get_num_rows()):
                    if (board.get_cell(c,r) == self.symbol):
                        myPieces += 1
                    elif (board.get_cell(c,r) == self.oppSym):
                        opposingPieces  += 1
            #print("Mine: " + str(myPieces) + "Opp: " + str(opposingPieces))
            value = myPieces - opposingPieces     
        elif (self.eval_type == 1): #Mobility
            myMoves = 0
            opposingMoves = 0
            for c in range(board.get_num_cols()):
                for r in range(board.get_num_rows()):
                    if (board.is_legal_move(c,r,self.symbol)):
                        myMoves += 1
                    elif (board.is_legal_move(c,r,self.oppSym)):
                        opposingMoves  += 1
            value = myMoves - opposingMoves
        elif (self.eval_type == 2): #Own Function: 3*corner pieces + 1*legal corner move - ...
            myScore = 0
            opposingScore = 0
            #0,0 ; 0,row ; col, o; row, col
            c = 0
            r = 0
            while 1: #Loop for each corner of the board
                if (board.get_cell(c,r) == self.symbol):
                    myScore += 3
                elif (board.get_cell(c,r) == self.oppSym):
                    opposingScore  += 3
                if (board.is_legal_move(c,r,self.symbol)):
                    myScore += 1
                elif (board.is_legal_move(c,r,self.oppSym)):
                    opposingScore += 1
                if c==0:
                    if r==0:
                        r=board.get_num_rows()-1
                    else:
                        c=board.get_num_cols()-1
                        r=0
                else:
                    if r==0:
                       r=board.get_num_rows()-1
                    else:
                        break 
            value = myScore - opposingScore
        return value



    def get_successors(self, board: OthelloBoard, player_symbol):
        # Write function that takes the current state and generates all successors obtained by legal moves
        # type:(board, player_symbol) -> (list)
        successors = [] #stores (board,column,row)
        for c in range(board.get_num_cols()):
            for r in range(board.get_num_rows()):
                if board.is_legal_move(c,r,player_symbol):
                    newBoard = board.cloneOBoard()
                    newBoard.play_move(c,r,player_symbol)
                    successors.append((newBoard,c,r))      
        return successors 


    def get_move(self, board: OthelloBoard):
        # Write function that returns a move (column, row) here using minimax
        # type:(board) -> (int, int)


        """FOR TESTING PURPOSES:"""
        #print("Current Boards evaluation: " + str(self.eval_board(board)) + "\n")
        #exit(0)

        return self.alphabeta(board)

       
        





