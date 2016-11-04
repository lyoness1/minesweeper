import minesweeper as ms 
from random import randint
import itertools
import numpy as np

HEIGHT = 10
WIDTH = 10
NUM_MINES = 10

TEST_CASES = 100000

# Extension method for Game class from minesweeper module
def solve(self):
    """Solver method on Game class"""

    try:
        while True:
            Solver(self, self.board).find_best_move().click()

    except ms.GameWonException:
        return True

    except ms.GameLossException:
        return False

# Add extension method to Game class
ms.Game.solve = solve


class Solver(object):
    """A solver class that returns a cell least likely to contain a mine.

    Step 1: Create a map of rules describing the current state of the board. 

    Step 2: For each covered cell on the board, calculate the probability that
    cell will contain a mine. 

    Step 3: Return the cell with the lowest probability of being a mine. If 
    multiple cells have the same lowest likelihood of being a mine, chose any. 
    """

    def __init__(self, game, board):
        """Initialize Solver object"""

        self.game = game    # contains board set-up for current game
        self.board = board      # current state of board in play
        self.rules = RuleMap(self.board)    # initialize RuleMap for curr state
        self.rules.make_rules(self.game.num_mines) # create rules for curr state
        self.probabilities = [0 
            for cell in xrange(board.cells_left)]   # init prob matrix

    def find_best_move(self):
        """Returns the cell with the least probability of containing a mine. 

        If all cells are covered (as with the first move the game), chose a cell
        randomly.
        """
        
        # only for first move of game
        if self.rules.rule_count <= 1:
            return self._pick_randomly()
        else:
            self._calculate_probabilities()
            best_cell = self.rules.all_covered_cells[
                            self.probabilities.index(min(self.probabilities))
                        ]
            return best_cell

    def _pick_randomly(self):
        """Returns a random, covered cell for first click of game."""

        while True:
            x = randint(0, self.board.height-1)
            y = randint(0, self.board.width-1)
            cell = self.board.cells[x][y]
            if not cell.uncovered:
                return cell

    def _calculate_probabilities(self):
        """Finds the probability of finding a mine for each covered cell.

        Uses linear programming to solve the least squares equation:

            Ax = B

        where:  A is the coeff_matrix,
                B is the mines_matrix,
                x is the vector containing probabilities of finding a mine for 
                    each covered cell for current board state.

        coeff_matrix:   Each row represents a rule.
                        Each value flags whether the covered cell corresponding 
                            to that index appears in the rule for that row. 

        mines_matrix:   Each value represents the number of mines surrounding 
                            the uncovered cell for the rule corresponding to 
                            that index.  

        solutions:      Each cell represents the probability that the covered 
                            cell corresponding to that index contains a mine. 
        """

        # Initialize coefficient matrix for all covered cells in all rules
        coeff_matrix = [[0 for _ in xrange(self.rules.num_covered)]
                        for _ in xrange(self.rules.rule_count)]
        
        # Initialize mines maxtrix to proper size
        mines_matrix = [0 for _ in xrange(self.rules.rule_count)]

        for rule in self.rules.rules:
            # Populate mines_matrix
            mines_matrix[rule.id] = rule.num_mines
            for cell in rule.cells:
                # Populate coeff_matrix
                cell_index = self.rules.all_covered_cells.index(cell)
                coeff_matrix[rule.id][cell_index] = 1

        # Use linear programming to solve the least squares equation
        A = np.array(coeff_matrix)
        B = np.array(mines_matrix)
        self.probabilities = np.linalg.lstsq(A, B)[0].tolist()


class RuleMap(object):
    """A map of rules for current state of the board.

    Each uncovered, numbered cell will create a rule. For each of these cells, 
    the rule is:

        sum(adjacent_covered_cells) = num_mines_surrounding_uncovered_cell

    These rules will later be used to create matricies from which probabilities
    of mine placements can be calculated, given every possible combination of
    mine placements for the current state of the board. 
    """

    def __init__(self, board):
        """Initialize rule map."""

        self.board = board
        self.rules = set()  # rules about board state
        self.rule_id = itertools.count()    # self-incrementer for rule id's
        self.all_covered_cells = []
        self.rule_count = 0     # for later use in creating calculation matrix
        self.num_covered = 0

    def make_rules(self, num_mines):
        """Creates a rule map of current board state."""

        # Iterate over all uncovered, numbered cells on border of play.
        # Create rule for each of these cells and add to rule map. 
        for x in xrange(self.board.height):
            for y in xrange(self.board.width):
                cell = self.board.cells[x][y]
                # only make rules for numbered cells with covered neighbors
                if cell.uncovered and cell.mines > 0:
                    self._add_rule(cell)
                # track all covered cells for later use in final rule creation.
                elif not cell.uncovered:
                    self.all_covered_cells.append(cell)

        # Add the final rule representing the mine density in all covered cells
        rule_id = next(self.rule_id)
        self.rules.add(Rule(num_mines, self.all_covered_cells, rule_id))

        # Update class attributes
        self.rule_count = len(self.rules)
        self.num_covered = len(self.all_covered_cells)

    def _add_rule(self, cell):
        """Adds a rule for an uncovered, numbered cell."""

        covered_neighbors = [n for n in cell.get_valid_neighbors()
                             if not n.uncovered]
        rule_id = next(self.rule_id)
        self.rules.add(Rule(cell.mines, covered_neighbors, rule_id))


class Rule(object):
    """A Rule object to store information about each uncovered numbered cell."""

    def __init__(self, num_mines, cells, rule_id):
        """Initialize Rule"""

        self.cells = cells  # list of covered, adjacent cells to numbered cell
        self.num_mines = num_mines  # num_mines surrounding numbered cell
        self.id = rule_id   # unique id for tracking placement in matrix


if __name__ == '__main__':
    import timeit
    time = 0
    num_won = 0
    for _ in xrange(TEST_CASES):
        start_time = timeit.default_timer()
        game = ms.Game(WIDTH, HEIGHT, NUM_MINES).solve()
        duration = timeit.default_timer() - start_time
        time += duration
        if game:
            num_won += 1

    print ("Solve rate: " + str(num_won) + " / " + str(TEST_CASES) + " = " +
           str((float(num_won)/TEST_CASES) * 100) + "%")

    print "Time to run", str(TEST_CASES), "trials:", time

