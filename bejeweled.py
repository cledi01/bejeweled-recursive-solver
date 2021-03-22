import random
import time
import numpy as np
import copy
import pygame
import os

pygame.init()
clock = pygame.time.Clock()

size_of_board = input("Input size of board, format 'row column': ")
# TODO: Implement max size for input
shape = size_of_board.split(" ")
row = int(shape[0])
col = int(shape[1])

red_gem = pygame.image.load(os.path.join("images","red_gem.jpg"))
red_gem = pygame.transform.scale(red_gem, (90, 90))

orange_gem = pygame.image.load(os.path.join("images","orange_gem.jpg"))
orange_gem = pygame.transform.scale(orange_gem, (90, 90))

yellow_gem = pygame.image.load(os.path.join("images","yellow_gem.jpg"))
yellow_gem = pygame.transform.scale(yellow_gem, (90, 90))

gemsDict = {
    1: red_gem,
    2: orange_gem,
    3: yellow_gem,
}

board = []

def initializeBoard(board, initialBoard=None):
    if initialBoard == None:
        while 1:
            board = []
            for i in range(row):
                currentColumn = []
                for j in range(col):
                    currentColumn.append(random.randint(1, 3))
                board.append(currentColumn)
            if (not checkCombo(board)):
                break
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

def isEmpty(board):
    for column in board:
        for gem in column:
            if (gem != 0):
                return False
    return True

def solve(board, previousMove=None):
    # Assumes board is initially in a stable state
    # printBoard(board)
    # print(f'previousMove: {previousMove}')
    if isEmpty(board):
        return [previousMove]
    moves = findAllValidMoves(board)
    # print(f'moves: {moves}')
    if len(moves) == 0:
        return []
    for move in moves:
        # print(f'move: {move}')
        virtualBoard = copy.deepcopy(board)
        swap(virtualBoard, move[0], move[1])
        nextState(virtualBoard)
        sequence = solve(virtualBoard, move)
        # print(f'Sequence: {sequence}')
        if len(sequence) != 0:
            if previousMove != None:
                sequence.insert(0, previousMove)
                return sequence
            else:
                return sequence
    return []

def nextState(board):
    while checkCombo(board):
        fall(board)

def drawBoard(board, row, col):
    black = (0, 0, 0)
    bg = pygame.image.load(os.path.join('images','bejeweled_bg.jpg'))

    width = 100 * col
    height = 100 * row

    screen = pygame.display.set_mode((width, height))
    screen.blit(bg, (0, 0))

    for i in range(row):
        pygame.draw.line(screen, black, (0, ((height / row) * i)), (width, ((height / row) * i)), 5)
    
    for j in range(col):
        pygame.draw.line(screen, black, ((width / col) * j, 0), ((width / col) * j, height), 5)
    
    # Test
    for i in range(row):
        for j in range(col):
            if (board[i][j] == 0): continue
            screen.blit(gemsDict[board[i][j]], (j * 100, i * 100))

    return screen

board = initializeBoard(board)
# printBoard(board)
# print("\n")
# nextState(board)
# printBoard(board)
# print("\n")
# print(findAllValidMoves(board))

# Example Boards
# [[1,2,1,0,1,2,1],
#  [2,1,2,0,2,1,2]]
# Sequence: [[[0, 1], [1, 1]], [[0, 5], [1, 5]]]

# [[3, 2, 1, 2, 3, 2], 
#  [1, 3, 2, 1, 1, 3], 
#  [3, 1, 2, 3, 2, 1]]

# Sequence: [[[0, 1], [0, 2]], [[1, 0], [1, 1]], [[1, 5], [2, 5]], [[1, 4], [2, 4]]]

while 1:
    sequence = []
    board = initializeBoard(board, [[3, 2, 1, 2, 3, 2],[1, 3, 2, 1, 1, 3],[3, 1, 2, 3, 2, 1]])
    nextState(board)
    sequence = solve(board)
    if (len(sequence) > 0):
        printBoard(board)
        print(f'Sequence: {sequence}')
        break
print("Solved board")
for move in sequence:
    swap(board, move[0], move[1])
    nextState(board)
print(board)

# screen = drawBoard(board, row, col)

# oddeven = 1
# while True:
#     oddeven += 1
#     screen = drawBoard(board, row, col)
#     if (oddeven == 1):
#         fall(board)
#         time.sleep(1)
#     else:
#         checkCombo(board)
#         time.sleep(1)
#     if (isEmpty(board)):
#         time.sleep(2)
#         print("Solved")
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: pygame.quit()
#     pygame.display.update()
#     oddeven = oddeven % 2
    