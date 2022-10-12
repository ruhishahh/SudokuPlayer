#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 13:04:46 2022

@author: ruhishah
"""

import pygame
import requests
#import time
from sudokuSolver import solver, checkValid, findEmpty


# uses valid if we wanna check if one number is a valid solution or not

#so we would check if move is valid, then place onto board 
#and see if solver returns true, meaning a solution is possible with number there


WINSIZE = 550
BOARDSIZE = 9

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
newBoard = response.json()['board']


#check how to do this, copied it
newBoardhardcopy = [[newBoard[i][j] for j in range(len(newBoard[0]))] for i in range(len(newBoard))]



'''
Inserts number into sudoku board from keyboard
'''
def insertNum(pos, window):
    numFont = pygame.font.SysFont('gabriola', 30)
    
    # Calculates index of sudoku board array from mouse position
    boardPos = ((pos[1]-55)//55, (pos[0])//55)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                # Can not change original sudoku board numbers
                if newBoardhardcopy[boardPos[0]][boardPos[1]] != 0:
                    return
                # Erases a number
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_0:
                    newBoard[boardPos[1]][boardPos[0]] = 0
                    pygame.draw.rect(window, (255, 255, 255), (boardPos[1]*55 + 10, boardPos[0]*55 + 60, 45, 45))
                    pygame.display.update()
                    return
                elif event.key == pygame.K_1:
                    key = 1
                elif event.key == pygame.K_2:
                    key = 2
                elif event.key == pygame.K_3:
                    key = 3
                elif event.key == pygame.K_4:
                    key = 4
                elif event.key == pygame.K_5:
                    key = 5
                elif event.key == pygame.K_6:
                    key = 6
                elif event.key == pygame.K_7:
                    key = 7
                elif event.key == pygame.K_8:
                    key = 8
                elif event.key == pygame.K_9:
                    key = 9
                else:
                    return
                #Erases potential previous number
                pygame.draw.rect(window, (255, 255, 255), (boardPos[1]*55 + 10, boardPos[0]*55 + 60, 45, 45))
                
                # Adds number onto GUI board
                val = numFont.render(str(key), True, (100, 100, 100))
                window.blit(val, (55*boardPos[1] + 25, 55*boardPos[0] + 70))
                
                # Updates sudoku array board
                newBoard[boardPos[0]][boardPos[1]] = key
                
                pygame.display.update()   
                return
                               
'''
Clears out earlier message and adds new message onto GUI window
'''     
def printMessage(message, window):
    buttonFont = pygame.font.SysFont('cambria', 25)
    solveText = buttonFont.render((message), True, (0, 0, 0))
    
    pygame.draw.rect(window,(255, 255, 255),(195, 15, 180, 30))
    window.blit(solveText, (195, 20))
    pygame.display.update()
    
    
'''
Checks to see if the board has been successfully solved
'''   
def isBoardSolved(window):
    copy = [[newBoardhardcopy[i][j] for j in range(len(newBoardhardcopy[0]))] for i in range(len(newBoardhardcopy))]
    solver(copy)
    B = newBoard
    for i in range(len(newBoard)):
            for j in range(len(newBoard)):
                if copy[i][j] != B[i][j]:
                    printMessage("Not Solved", window)
                    return False
    printMessage("board is solved", window)
    return True


'''
Checks to see if all the moves made so far are correct
'''                  
def isBoardOkay(window):
    copy = [[newBoardhardcopy[i][j] for j in range(len(newBoardhardcopy[0]))] for i in range(len(newBoardhardcopy))]
    solver(copy)
    B = newBoard
    for i in range(len(newBoard)):
            for j in range(len(newBoard)):
                print(i, j)
                if B[i][j] != 0 and copy[i][j] != B[i][j]:
                    printMessage("Not Doing okay", window)
                    return False
    
    printMessage("Doing okay", window)
    return True


'''
Solves board and shows solution
'''
def solveBoard(window):
    numFont = pygame.font.SysFont('gabriola', 30)
    copy =  [[newBoardhardcopy[i][j] for j in range(len(newBoardhardcopy[0]))] for i in range(len(newBoardhardcopy))]
    solver(copy)
    for i in range(len(newBoard[0])):
        for j in range(len(newBoard[0])):
            if newBoardhardcopy != 0:
                pygame.draw.rect(window, (255, 255, 255), (10+55*j, 60+55*i, 40, 40))
                val = numFont.render(str(copy[i][j]), True, (0, 0, 0))
                window.blit(val, (24+55*j, 74+55*i))
                pygame.display.update()
                pygame.time.delay(50)
    printMessage("SOLVED", window)
  

#need to fix this
'''
Solves board while  displaying the backtracking algorithm
'''
def solveBoardAlg(window):
    numFont = pygame.font.SysFont('gabriola', 30)
    if findEmpty(newBoardhardcopy) == False:
        return True
    else:
        move = findEmpty(newBoardhardcopy)
    
    for i in range(1,10):
        if checkValid(newBoardhardcopy, move, i):
            newBoardhardcopy[move[0]][move[1]] = i
            pygame.draw.rect(window, (255, 255, 255), (10+55*move[1], 60+55*move[0], 40, 40))
            val = numFont.render(str(i), True, (0, 0, 0))
            window.blit(val, (24+55*move[1], 74+55*move[0]))
            pygame.display.update()
            
            
            if solveBoardAlg(newBoardhardcopy):
                return True
            newBoard[move[0]][move[1]] = 0
            val = numFont.render(str(0), True, (0, 0, 0))
            window.blit(val, (24+55*move[1], 74+55*move[0]))
    return False


                
def main():
    pygame.init()
    
    # Initializes window
    window = pygame.display.set_mode((WINSIZE+60, WINSIZE))
    window.fill((255,255, 255))
    pygame.display.set_caption("Sudoku")
    
    checkSolved = Button(510, 60, 25, 90, (0, 0, 0), 'CHECK SOLVED', 'arial.ttf', 15, isBoardSolved)
    checkSolved.addButton(window)
    
    checkOkay = Button(510, 100, 25, 90, (0, 0, 0), 'CHECK OKAY', 'arial.ttf', 15, isBoardOkay)
    checkOkay.addButton(window)

    solveGame = Button(510, 140, 25, 90, (0, 0, 0), "SOLVE BOARD", 'arial.ttf', 15, solveBoardAlg)
    solveGame.addButton(window)
    
    buttonList = []
    buttonList.append(checkSolved)
    buttonList.append(checkOkay)
    buttonList.append(solveGame)
    
    
    run = True
    
    # Creates board on window
    for i in range(BOARDSIZE+1):
        if i % (BOARDSIZE**(1/2)) == 0:
            pygame.draw.line(window,(0, 0, 0),(55*i+2, 52), (55*i+2, 547), 3)
            pygame.draw.line(window,(0, 0, 0),(2, 55*i+52), (497, 55*i+52), 3)
        else:
            pygame.draw.line(window,(0, 0, 0),(55*i+2, 52), (55*i+2, 547), 1)
            pygame.draw.line(window,(0, 0, 0),(2, 55*i+52), (497, 55*i+52), 1)
       

    # Adds numbers from initialized game onto board
    numFont = pygame.font.SysFont('gabriola', 30)
    for i in range(len(newBoard[0])):
        for j in range(len(newBoard[0])):
            if 1 <= newBoard[i][j] <= 9:
                val = numFont.render(str(newBoard[i][j]), True, (0, 0, 0))
                window.blit(val, (24+55*j, 74+55*i))
    pygame.display.flip() 
    
    while run:
        for event in pygame.event.get():
            # Creates Quit functionality
            if event.type == pygame.QUIT:
                pygame.quit()
                #run = False
                return
            pos = pygame.mouse.get_pos()
            # Checks if mouse is over any button
            if event.type == pygame.MOUSEMOTION:
                checkOkay.overButton(window, pos)
                checkSolved.overButton(window, pos)
                solveGame.overButton(window, pos)
                
            # Checks if user clicked on a valid block on board
            #fix ^
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttonList:
                    if button.getXPos() < pos[0] < button.getXPos()+ button.getWidth() and button.getYPos() < pos[1] < button.getYPos() + button.getHeight():
                        button.getFunction()(window)
                if pos[0] < 510 and pos[1] > 55:
                    insertNum(pos, window)

              



'''
This class represents a button. It contains the basic methods to access its attrubutes, 
as well as methods for adding button to window, checking if the button has a mouse over 
it and if it has been clicked
'''
class Button():
    def __init__(self, xPos, yPos, height, width, color, text, font, size, function):
        self.__xPos = xPos
        self.__yPos = yPos
        self.__height = height
        self.__width = width
        self.__color = color
        self.__text = text
        self.__font = font
        self.__size = int(size)
        self.__function = function
    
    def getXPos(self):
        return self.__xPos
    
    def getYPos(self):
        return self.__yPos
    
    def getWidth(self):
        return self.__width
    
    def getHeight(self):
        return self.__height
    
    def getFunction(self):
        return self.__function
     
    def addButton(self, window):
        buttonFont = pygame.font.SysFont(self.__font, self.__size)
        boardText = buttonFont.render(self.__text, True, self.__color)
        pygame.draw.rect(window, (0, 0, 0), (self.__xPos-2, self.__yPos-2, self.__width+5, self.__height+5), 0, 3)
        pygame.draw.rect(window, (204, 229, 255), (self.__xPos, self.__yPos, self.__width, self.__height), 0, 3)
        # need to center button
        window.blit(boardText, (self.__xPos + self.__height//6, self.__yPos+10))
        
    def overButton(self, window, pos):
        if self.__xPos <= pos[0] <= (self.__xPos + self.__width*4) and self.__yPos <= pos[1] <= (self.__yPos + self.__height):
            overFont = pygame.font.SysFont(self.__font, self.__size)
            overText = overFont.render(self.__text, True, (255, 255, 255))

            #pygame.draw.rect(window,(255, 255, 255),(self.__xPos-2, self.__yPos-2, self.__height+5, self.__width+5))
            pygame.draw.rect(window,(0, 0, 0),(self.__xPos, self.__yPos, self.__width, self.__height))
    
            window.blit(overText, (self.__xPos + self.__height//6, self.__yPos+10))
            pygame.display.update()
        else:
            overFont = pygame.font.SysFont(self.__font, self.__size)
            overText = overFont.render(self.__text, True, (0, 0, 0))

            #pygame.draw.rect(window,(255, 255, 255),(self.__xPos-2, self.__yPos-2, self.__height+5, self.__width+5))
            pygame.draw.rect(window,(204, 229, 255),(self.__xPos, self.__yPos, self.__width, self.__height))
    
            window.blit(overText, (self.__xPos + self.__height//6, self.__yPos+10))
            pygame.display.update()
            

    def clickedButton(self, window):
            overFont = pygame.font.SysFont(self.__font, self.__size)
            overText = overFont.render(self.__text, True, (0, 0, 0))

            #pygame.draw.rect(window,(255, 255, 255),(self.__xPos-2, self.__yPos-2, self.__height+5, self.__width+5))
            pygame.draw.rect(window,(255, 255, 255),(self.__xPos, self.__yPos, self.__width, self.__height))
    
            window.blit(overText, (self.__xPos + self.__height//6, self.__yPos+10))
            pygame.display.update()
        
    def overSquare(self, window, pos):
        return False

     
       
main()

