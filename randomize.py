import random
from copy import deepcopy
import start


def checkValidPuzzle( grid: list) -> bool:
    '''
    Checking the correctness of the sudoku puzzle but only checks for doubles of numbers in the same row, column, or 3x3 block.

        Parameters:
            grid (list): Sudoku Puzzle that is to be checked

        Returns:
            bool: True if the Puzzle doesn't have any repeats of numbers, False if there are repeats    
    '''
    for row in range(0,9):
        for col in range(0,3):
            for space in range(0,3):
                if grid[row][col][space].isdigit():
                    currentNumber = int(grid[row][col][space])
                    #Save the current value
                    grid[row][col][space] = "."
                    if not checkIntegrity( currentNumber, row, col, space, grid):
                        grid[row][col][space] = str(currentNumber) 
                        return False
                    else:
                        grid[row][col][space] = str(currentNumber)    
    return True

def checkIntegrity( num: int, row: int, col: int, space: int, grid: list) -> bool:
    '''
    Checking the correctness of the number to be inputted into the grid and making sure there are no invalid repeats of numbers

        Parameters:
            num (int): The number to be inputted
            row (int): The row that that the number will be inputted
            col (int): The 3x3 column that the number will be inputted (there are 3 block columns, each with 3 individual spaces)
            space (int): The individual space that the number will be inputted
            grid (list): Sudoku Puzzle that is to be checked

        Returns:
            bool: True if the Puzzle doesn't have any repeats of numbers, False if there are repeats    
    '''

    for checkEachCol in range(0,3): 
        #Checking if that number is in that row already
        if str(num) in grid[row][checkEachCol]:
            return False
    
    for checkSection in range(0,3): 
        #Checking if that number is in that section already
        if row in [0,1,2]:
            if str(num) in grid[0][col] or str(num) in grid[1][col] or str(num) in grid[2][col]:
                return False

        elif row in [3,4,5]:
            if str(num) in grid[3][col] or str(num) in grid[4][col] or str(num) in grid[5][col]:
                return False

        elif row in [6,7,8]:
            if str(num) in grid[6][col] or str(num) in grid[7][col] or str(num) in grid[8][col]:
                return False       

    for checkEachRow in range (0,9): 
        #Checking if the number is in the individual column already
        if str(num) in grid[checkEachRow][col][space]:
            return False                   
    return True        

def generateRandomSolution(grid: list) -> list:
    '''
    Creates a random solution of a sudoku

        Parameters:
            grid (list): Sudoku Puzzle that is to be created

        Returns:
            grid (list): The same Sudoku Puzzle after the solution is generated 
    '''
    solutionSet =  [7,5,9,4,6,2,8,1,3,
                    4,6,3,5,1,8,2,9,7,
                    1,2,8,9,7,3,6,4,5,
                    6,9,7,1,8,4,5,3,2,
                    5,8,4,2,3,6,9,7,1,
                    2,3,1,7,9,5,4,8,6,
                    3,4,5,8,2,1,7,6,9,
                    9,1,2,6,4,7,3,5,8,
                    8,7,6,3,5,9,1,2,4]
    #Real solution set to use and randomize the order of the numbers to create a solvable Sudoku
    for gridRow in range(0, 9):
        for gridCol in range(0,3):
            for colSpace in range(0,3):
                grid[gridRow][gridCol][colSpace] = str(solutionSet.pop(0))
    
    for numRepeatProcess in range(0,10):
        grid = randomizeGrid(grid)
    return grid
  
def solve(testGrid: list):
    '''
    Checks if the inputted test grid is solvable or not and solves the given grid

        Parameters:
            testGrid (list): Sudoku Puzzle that is to be created

        Returns:
            bool: True if the puzzle has been solved, False if the puzzle cannot be solved
    '''
    if all(space.isdigit() for space in flattenGrid(testGrid)):
        #Recursion base case
        return True 
    for row in range(0, 9):
        for col in range(0, 3):
            for space in range(0, 3):
                if not testGrid[row][col][space].isdigit():
                    for num in range(1, 10):
                        if checkIntegrity( num, row, col, space, testGrid):
                            testGrid[row][col][space] = str(num)
                            if solve(testGrid):
                                #Recursive call
                                return True
                            testGrid[row][col][space] = "."
                            #Backtracking
                    return False
    

def flattenGrid(grid: list) -> list:
    '''
    Takes a given grid with nested lists and creates a singular flat list containing all the Sudoku puzzle data

        Parameters:
            grid (list): Sudoku Puzzle that is to be flattened

        Returns:
            resultList (list): Flattened list made from the input
    '''
    resultList = []
    for row in range(0, 9):
        for col in range(0, 3):
            for space in range(0, 3):
                resultList = resultList + [grid[row][col][space]]
    return resultList  

def returnToGrid( flatGrid: list) -> list:
    '''
    Converts a flattened grid into a sudoku grid

        Parameters:
            flatGrid (list): Sudoku Puzzle that is to be converted a Sudoku grid

        Returns:
            resultGrid (list): The Sudoku grid form of the flattened list 
    '''
    resultGrid = []
    indexOfFlat = 0
    for rows in range(9):
        row =  [['.','.','.'], ['.','.','.'], ['.','.','.']]
        resultGrid = resultGrid + [row]
    for row in range(0, 9):
        for col in range(0, 3):
            for space in range(0, 3):
                resultGrid[row][col][space] = flatGrid[indexOfFlat]
                indexOfFlat += 1
    return resultGrid
  
def randomizeGrid(grid: list) -> list:
    '''
    Takes a Sudoku grid with a generated solution and randomizes the numbers to create unique puzzles

        Parameters:
            grid (list): Sudoku Puzzle that is to be randomized

        Returns:
            grid (list): The randomized Sudoku solution
    '''
    grid = randomizeBlockRows(grid)
    grid = randomizeBlockColumns(grid)
    grid = randomizeSingleRows(grid)
    grid = randomizeSingleColumns(grid)
    return grid

def randomizeBlockRows(grid: list) -> list:
    '''
    Swap any row of 3x3 blocks with any other row

        Parameters:
            grid (list): Sudoku Puzzle that is to be randomized

        Returns:
            grid (list): The randomized Sudoku solution
    '''
    blockRow1 = grid[:3]
    blockRow2 = grid[3:6]
    blockRow3 = grid[6:]
    randomizeRows = [blockRow1, blockRow2, blockRow3]
    newGrid = []
    for changeGrid in range(0,3):
        newGrid = newGrid + randomizeRows.pop(random.randint(0, len(randomizeRows) - 1)) 
    grid = newGrid 
    return grid

def randomizeBlockColumns(grid: list) -> list:
    '''
    Swap any column of 3x3 blocks with any other column

        Parameters:
            grid (list): Sudoku Puzzle that is to be randomized

        Returns:
            grid (list): The randomized Sudoku solution
    '''
    indexOfColumns = [0,1,2]
    pickColumn1 = indexOfColumns.pop(random.randint(0, len(indexOfColumns) - 1))
    pickColumn2 = indexOfColumns.pop(random.randint(0, len(indexOfColumns) - 1))
    remainingColumn = indexOfColumns[0]
    newGrid = []
    for gridRow in range(0, len(grid)):
        newGrid = newGrid + [[grid[gridRow][pickColumn1], grid[gridRow][pickColumn2], grid[gridRow][remainingColumn]]]
    grid = newGrid
    return grid
    
def randomizeSingleRows(grid: list) -> list:
    '''
    Swap any single row with other single rows inside their respective block rows

        Parameters:
            grid (list): Sudoku Puzzle that is to be randomized

        Returns:
            grid (list): The randomized Sudoku solution
    '''
    newGrid = []
    for rows in range(0, len(grid), 3):
        row1 = grid[rows]
        row2 = grid[rows + 1]
        row3 = grid[rows + 2]
        changeRows = [row1, row2, row3]
        for addToNewGrid in range(0,3):
            newGrid = newGrid + [changeRows.pop(random.randint(0, len(changeRows) - 1))]
    grid = newGrid
    return grid

def randomizeSingleColumns(grid: list) -> list:
    '''
    Swap any single column with other single columns inside their respective block columns

        Parameters:
            grid (list): Sudoku Puzzle that is to be randomized

        Returns:
            grid (list): The randomized Sudoku solution
    '''
    newGrid = []   
    numInBlockSingleRow = [0,1,2]
    chooseBlockColumn = random.randint(0,2)
    chooseSingleColumn = numInBlockSingleRow.pop(random.randint(0, len(numInBlockSingleRow) - 1))
    chooseSingleColumn2 = numInBlockSingleRow.pop(random.randint(0, len(numInBlockSingleRow) - 1))
    remainingSingleColumn = numInBlockSingleRow[0]
    for row in range(0, len(grid)):
        newSingleRow = []
        for blockColumn in range(0, len(grid[row])):
            if blockColumn == chooseBlockColumn:
                newBlockSingleRow = [grid[row][blockColumn][chooseSingleColumn], grid[row][blockColumn][chooseSingleColumn2], grid[row][blockColumn][remainingSingleColumn]]
                newSingleRow = newSingleRow + [newBlockSingleRow]
            else:
                newSingleRow = newSingleRow + [grid[row][blockColumn]]     
        newGrid = newGrid + [newSingleRow]
    grid = newGrid 
    return grid