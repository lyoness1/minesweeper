# Minesweeper & Solver 

### Files
minesweeper.py contains the user-playable game. 

solver.py contains an algorithm for solving a game with the highest probability of winning given the state of the board at any given time.
You can chose the heigh, width, and number of desired mines for each test case at the top of the file. Type `$ python solver.py` in the root folder containing the file to run. 

### To Play
Clone this repo and type `$ python minesweeper.py` in the root folder containing the minesweeper.py file. 

Enter your desired board height, width, and number of mines, to be placed randomly. 

Chose a cell to uncover by typing the row then the column letters, such as 'ab' for the cell in the first row and second column. 

Cells marked with "X" are still covered, cells marked with "." are empty, and cells with numbers represent the number of adjacent (including diagonals) cells that contain a mine. 

### Rules
A game is won when all cells *not* containing mines are uncovered. 
