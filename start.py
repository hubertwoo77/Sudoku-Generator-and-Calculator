import random
from copy import deepcopy
import randomize
import tkinter as tk
from tkinter import *
from functools import partial

grid = []
puzzleGrid = []
difficulty = ""

def welcome():
    '''
    Creates the main screen from which the user chooses to either do a Sudoku, select its difficulty, or use the Sudoku calculator
    '''
    global difficulty
    sudokuWindow = tk.Tk(None, None, " Sudoku Startup", 1)
    sudokuWindow.geometry("1920x1080")

    welcomeMessage = tk.Label(sudokuWindow, text = "Welcome to the Sudoku Solver! A set of random numbers will be generated in random positions and you can solve it yourself then check your answer with the program.", font = ('Arial', 12))
    difficulty = tk.StringVar()
    difficulty.set("EASY")
    startButton = tk.Button(sudokuWindow, text = "Start Game", font = ('Arial', 12), command = loadGame)

    sudokuCalculator = tk.Button(sudokuWindow, text = "Sudoku Calculator", font = ('Arial', 12), command = solveSudoku)

    welcomeMessage.pack()
    (tk.Radiobutton(sudokuWindow, text = "EASY", variable = difficulty, value = "EASY")).pack(anchor=W, pady = 20)
    (tk.Radiobutton(sudokuWindow, text = "MEDIUM", variable = difficulty, value = "MEDIUM")).pack(anchor=W, pady = 20)
    (tk.Radiobutton(sudokuWindow, text = "HARD", variable = difficulty, value = "HARD")).pack(anchor=W, pady = 20)
    startButton.pack(padx = 20, pady = 20)
    sudokuCalculator.pack()
    sudokuWindow.mainloop()

def solveSudoku():
    '''
    Creates the interface for the Sudoku calculator, providing an empty sudoku grid for the user to input numbers
    '''
    createGrid()
    calculationGrid = randomize.flattenGrid(grid)
    indexCountForFlatPuzzle = 0
    changeNumOfButton = {}
    sudokuCalculator = tk.Tk(None, None, " Sudoku Calculator", 1)
    sudokuCalculator.geometry("1920x1080")
    sudokuGrid = Frame(sudokuCalculator)

    def takeUserNum(indexNum: int):
        '''
        Used to change a square in the Sudoku. Assume that the changeNumOfButton dictionary is already defined.

            Parameters:
                indexNum (int): The position of the square to be changed
        '''
        userNum = ""
        unFlattenGrid = randomize.returnToGrid(calculationGrid)
        possibleOptions = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        def getUserNum():
            '''
            Allows the user to choose which number is to be inputted into the square
            '''
            userNum = takeNum.get()
            if userNum not in possibleOptions and userNum != ".":
                createPopUp("Please enter a number from 1-9 (with no spaces).")
            else:    
                changeNumOfButton[indexNum].config(text = userNum)
                calculationGrid[indexNum] = userNum
            enterNum.destroy()

        enterNum = Tk()
        enterNum.title("Add a number")
        Label(enterNum, text='Enter a number: ').grid(row=0)

        takeNum = Entry(enterNum)
        takeNum.grid(row=0, column=1)

        closeNumEntry = Button(enterNum, text = "Close", command = enterNum.destroy)
        closeNumEntry.grid(row=1, column=1)
        confirmNum = tk.Button(enterNum, text = "Enter", command = getUserNum)
        confirmNum.grid(row = 1)
        enterNum.mainloop()
    
    def getSolution():
        '''
        Calculates the Sudoku given from the user
        '''
        nonlocal calculationGrid
        gridSolution = randomize.returnToGrid(calculationGrid)
        if randomize.checkValidPuzzle(gridSolution) and randomize.solve(gridSolution):
            calculationGrid = randomize.flattenGrid(gridSolution) 
            for index in range(len(calculationGrid)):
                changeNumOfButton[index].config(text = calculationGrid[index])
        else:
            createPopUp("This Sudoku is unsolvable!") 

    for numColumn in range(9):
        sudokuGrid.columnconfigure(numColumn, weight = 9)
    for gridRow in range(0,9):
        for gridCol in range(0,9):
            newButton = tk.Button(sudokuGrid, text = calculationGrid[indexCountForFlatPuzzle], font = ('Arial', 12), command = partial(takeUserNum, indexCountForFlatPuzzle))
            (newButton).grid(row = gridRow, column = gridCol)
            changeNumOfButton[indexCountForFlatPuzzle] = newButton
            indexCountForFlatPuzzle += 1

    calculateButton = Button(sudokuCalculator, text = "Calculate", command = getSolution)
    (tk.Label(sudokuCalculator, text = "Click on an empty space to type in a number. If you want to remove a number, you can type \".\" as well.", font = ('Arial', 12))).pack()
    (tk.Label(sudokuCalculator, text = "Make sure you type in every clue given in the Sudoku to get the solution specific to YOUR puzzle (if not created properly, Sudoku puzzles with up to 77 clues can have more than one solution!). ", font = ('Arial', 12))).pack()
    (tk.Label(sudokuCalculator, text = "If you want to remove a number, you can type \".\" as well.", font = ('Arial', 12))).pack()
    sudokuGrid.pack()
    calculateButton.pack()
    sudokuCalculator.mainloop()


def loadGame():
    '''
    Generates the sudoku puzzle and opens up a new window for the game to be played.
    '''
    global difficulty
    global grid
    global puzzleGrid
    grid = []
    puzzleGrid = []
    createGrid()
    difficultyStr = difficulty.get()
    grid = randomize.generateRandomSolution(grid)  
    makePuzzle(difficultyStr)  
    #Creates puzzleGrid
    flatPuzzle = randomize.flattenGrid(puzzleGrid)
    indexCountForFlatPuzzle = 0
    changeNumOfButton = {}

    sudokuPlay = tk.Tk(None, None, " Sudoku Play", 1)
    sudokuPlay.geometry("1920x1080")
    sudokuGrid = Frame(sudokuPlay)

    def takeUserNum(indexNum: int):
        '''
        Used to change a square in the Sudoku. Assume that the changeNumOfButton dictionary is already defined.

            Parameters:
                indexNum (int): The position of the square to be changed
        '''
        userNum = ""
        compareToSolution = randomize.flattenGrid(grid)
        def getUserNum():
            '''
            Allows the user to choose which number is to be inputted into the square
            '''
            if flatPuzzle[indexNum] == ".":
                userNum = takeNum.get()
                if userNum == compareToSolution[indexNum]:
                    flatPuzzle[indexNum] = userNum
                    changeNumOfButton[indexNum].config(text = userNum)
                    if (flatPuzzle == compareToSolution):
                        createPopUp("Congratulations! You have solved this puzzle.")
                else:
                    createPopUp("Wrong! Try Again.")
            else:
                createPopUp("This cell is already filled!")     
            enterNum.destroy()

        enterNum = Tk()
        enterNum.title("Add a number")
        Label(enterNum, text='Enter a number: ').grid(row=0)

        takeNum = Entry(enterNum)
        takeNum.grid(row=0, column=1)

        closeNumEntry = Button(enterNum, text = "Close", command = enterNum.destroy)
        closeNumEntry.grid(row=1, column=1)
        confirmNum = tk.Button(enterNum, text = "Enter", command = getUserNum)
        confirmNum.grid(row = 1)
        enterNum.mainloop()

    def showAnswer():
        '''
        Fills all the cells with the right numbers
        '''
        flatGridSolution = randomize.flattenGrid(grid)
        for index in range(len(flatPuzzle)):
            flatPuzzle[index] = flatGridSolution[index]
            changeNumOfButton[index].config(text = flatGridSolution[index])

    for numColumn in range(9):
        sudokuGrid.columnconfigure(numColumn, weight = 9)
    for gridRow in range(0,9):
        for gridCol in range(0,9):
            newButton = tk.Button(sudokuGrid, text = flatPuzzle[indexCountForFlatPuzzle], font = ('Arial', 12), command = partial(takeUserNum, indexCountForFlatPuzzle))
            (newButton).grid(row = gridRow, column = gridCol)
            changeNumOfButton[indexCountForFlatPuzzle] = newButton
            indexCountForFlatPuzzle += 1
    (tk.Label(sudokuPlay, text = "Click on an empty space to type in a number and check if your answer is correct or not!", font = ('Arial', 12))).pack()
    sudokuGrid.pack()

    goToAnswer = Button(sudokuPlay, text = "Show Answer", command = showAnswer)
    goToAnswer.pack()

    sudokuPlay.mainloop()

def createPopUp(message: str):
    '''
    Creates a new window with a message alert for the user to see
        
        Parameters:
            message (str): The string alaert that will be printed on the pop up window
    '''
    displayPopUp = Tk()
    displayPopUp.title("ALERT")
    displayMessage = Label(displayPopUp, text = message)

    closeMessage = Button(displayPopUp, text = "Close", command = displayPopUp.destroy)
    displayMessage.pack()
    closeMessage.pack()
    displayPopUp.mainloop()

def printGrid(grid: list):
    '''
    Used to print the Sudoku grid in the console output rather than a window. Used for testing and debugging purposes.
        
        Parameters:
            grid (list): The Sudoku grid to be printed
    '''
    row = 1
    print("          A    B    C      D    E    F      G    H    I")
    for gridRow in range(0, len(grid)):
        if gridRow in [2,5]:
            print(row, "    ", grid[gridRow], "\n")
            row += 1
        elif gridRow == 8:
            print(row, "    ", grid[gridRow], "\n")
            print("---------------------------------------------------\n")
            row += 1
        else:
            print(row,"    ", grid[gridRow])
            row += 1

def createGrid():
    '''
    Creates a Sudoku grid
    '''
    global grid
    for rows in range(9):
        row =  [['.','.','.'], ['.','.','.'], ['.','.','.']]
        grid = grid + [row]



def makePuzzle(userResponse: str):
    '''
    Making the puzzle for the user after generating a random solution

        Parameters:
            userResponse (str): The difficulty that the user selected for their Sudoku (either easy, medium, or hard).
    '''
    global puzzleGrid
    countOfNumsRemoved = 0
    numOfNumsNeedRemoved = 0
    puzzleGrid = deepcopy(grid)
    if userResponse == "EASY":
        numOfNumsNeedRemoved = 45
    elif userResponse == "MEDIUM":
        numOfNumsNeedRemoved = 54
    elif userResponse == "HARD":
        numOfNumsNeedRemoved = 62     
    while countOfNumsRemoved < numOfNumsNeedRemoved:
        randomGridRow = random.randint(0, len(grid) - 1)
        randomGridColumn = random.randint(0,2)
        randomGridSpace = random.randint(0,2)
        if puzzleGrid[randomGridRow][randomGridColumn][randomGridSpace].isdigit():
            puzzleGrid[randomGridRow][randomGridColumn][randomGridSpace] = "."
            countOfNumsRemoved += 1