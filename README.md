# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In naked twins problem constraint propagation is used for reducing the search space by specifying some rules. These rules include 1) there must be only two boxes in a unit that contain identical two digits, 2) the unit can be any of the following: row, column, square, or diagonal. After twins are identified, we can then safely proceed to eliminating values found in the twins from the twins' unit peers as the values in twins can be placed only in their twin boxes and nowhere else.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In diagonal sudoku problem constraint propagation results in solution in which all diagonals' values are as unique as it would be in row, column or square units. Simply put, constraint propagation in diagonal sudoku problem adds another unit (in this case diagonal) that must be taken into account in order to solve the problem. We can specify the diagonal unit's coordinates and add them to the list of all units and continue applying various strategies for solving sudoku as normal.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.