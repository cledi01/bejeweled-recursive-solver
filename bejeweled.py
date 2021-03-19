import random
import numpy as np
import copy

size_of_board = input("Input size of board, format 'row column': ")
# TODO: Implement max size for input
shape = size_of_board.split(" ")
row = int(shape[0])
col = int(shape[1])

gemsDict = {
    "empty": 0,
    "red": 1,
    "orange": 2,
    "yellow": 3,
}

board = []

def initializeBoard(board, initialBoard=None):
    if initialBoard == None:
        for i in range(row):
            currentColumn = []
            for j in range(col):
                currentColumn.append(random.randint(1, 3))
            board.append(currentColumn)
    else:
        board = initialBoard
    return board

def fall(board):
    """
    Effect: Make sure the gems fall to the ground
    """
    # Check each column for non-zero elements, re-initialize the 
    # column and push all elements to the bottom
    for i in range(col):
        nonZeroList = []
        for j in range(row):
            if (board[j][i] != 0):
                nonZeroList.append(board[j][i])
            # Reset the gems to 0s (empty)
            board[j][i] = 0
        # Reinitialize the column with gems pushed to bottom
        topRow = row - len(nonZeroList)
        for j in range(topRow, row):
            # j-topRow is such that it goes from 0 -> len(nonZeroList)
            board[j][i] = nonZeroList[j-topRow]

def printBoard(board):
    for i in range(row):
        print(board[i])

def checkCombo(board):
    """
    Effect: Resolves any solved gems and moves the board to the next state
    Returns: True if there was a solved combination, False otherwise
    """
    solved = False
    matchedBoard = np.ones((row,col))
    ## row combos
    for i in range(col):
        for j in range(1, row-1):
            if board[j][i] != 0:
                if board[j][i] == board[j-1][i] and board[j][i] == board[j+1][i]:
                    matchedBoard[j-1][i] = 0
                    matchedBoard[j][i] = 0
                    matchedBoard[j+1][i] = 0
                    solved = True

    ## column combos
    for i in range(row):
        for j in range(1, col-1):
            if board[i][j] != 0:
                if board[i][j] == board[i][j-1] and board[i][j] == board[i][j+1]:
                    matchedBoard[i][j-1] = 0
                    matchedBoard[i][j] = 0
                    matchedBoard[i][j+1] = 0
                    solved = True


    for i in range(row):
        for j in range(col):
            if matchedBoard[i][j] == 0:
                board[i][j]=0

    return solved

def swap(board, position1, position2):
    # position1, position2: [row, col]
    temp = board[position1[0]][position1[1]]
    board[position1[0]][position1[1]] = board[position2[0]][position2[1]]
    board[position2[0]][position2[1]] = temp

def isValidMove(board, position1, position2):
    virtualBoard = copy.deepcopy(board)
    swap(virtualBoard, position1, position2)

    if checkCombo(virtualBoard) == True:
        return True
    else:
        return False

def findAllValidMoves(board):
    validMoves = []
    for i in range(row):
        for j in range(col):
            # Edge cases, check if i + 1 == row, if so it is out of index, else 
            # bottom swap is valid
            if (i + 1) != row:
                if isValidMove(board, [i, j], [i + 1, j]):
                    validMoves.append([[i, j], [i+1, j]])
            if (j + 1) != col:
                if isValidMove(board, [i,j], [i, j+1]):
                    validMoves.append([[i,j], [i, j+1]])
    return validMoves

def nextState(board):
    while checkCombo(board):
        fall(board)

board = initializeBoard(board)
printBoard(board)
print("\n")
nextState(board)
printBoard(board)
print("\n")
print(findAllValidMoves(board))