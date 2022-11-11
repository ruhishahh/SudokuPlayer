#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 13:51:16 2022

@author: ruhishah
"""



board = [
    
    
    
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]



def showBoard(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("----------------------")
        for j in range(len(board)):
            if j % 3 == 0 and j !=0:
                print("| ", end="")
            if (j == ((len(board))-1)):
                print(board[i][j])
            else:
                print(str(board[i][j])+" ", end="")
    return False


def findEmpty(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return (i, j)
    return False
     
# go thru this with pen and paper tomorrow
def solver(board):
    if findEmpty(board) == False:
        return True
    else:
        move = findEmpty(board)
    
    for i in range(1,10):
        if checkValid(board, move, i):
            board[move[0]][move[1]] = i
            
            if solver(board):
                return True
            board[move[0]][move[1]] = 0
    
        
    return False;


def checkRow(board, move, moveValue):
    for i in range(len(board)):
        if board[move[0]][i] == moveValue:
            return False
    return True;

def checkColumn(board, move, moveValue):
    for i in range(len(board)):
        if board[i][move[1]] == moveValue:
            return False
    return True


def checkSquare(board, move, moveValue):
    yVal = int(move[0] // (len(board)** (1/2)))
    xVal = int(move[1] // (len(board) ** (1/2)))
    
    
    for i in range(yVal*3, yVal*3+3):
        for j in range(xVal*3, xVal*3+3):
            if (board[i][j] != move and board[i][j] == moveValue):
                return False
    return True


def checkValid(board, move, moveValue):
    if checkRow(board, move, moveValue) and checkColumn(board, move, moveValue) and checkSquare(board, move, moveValue):
        return True
    return False

        
    
    
showBoard(board)

solver(board)
print("")

showBoard(board)




