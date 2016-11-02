import minesweeper as ms 

HEIGHT = 10
WIDTH = 10
NUM_MINES = 10

TEST_CASES = 10

# Extension methods for Game class
def solve(self):
    """Solver method on Game class"""

    try:
        while True:
            self.get_best_move().click()
            return False

    except ms.GameWonException:
        return True

    except ms.GameLossException:
        return False


def get_best_move(self):
    """Method on Game class returning best cell to click"""

    return self.board.cells[0][0]

# Add extension methods to Game class
ms.Game.solve = solve
ms.Game.get_best_move = get_best_move


class Solver(object):
    """A Solver class that stores probabilities for picking best cell"""

    def __init__(self, game, width, height):
        """Initialize Solver object"""

        self.game = game
        self.width = width
        self.height = height
        self.cells = self.cells = [
            [Cell(self, x, y) for x in xrange(width)] for y in xrange(height)
        ]


# http://codereview.stackexchange.com/questions/54737/analyzing-minesweeper-probabilities
# http://math.stackexchange.com/questions/969589/overlapping-probability-in-minesweeper/970264#970264






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
           str(float(num_won)/TEST_CASES))

    print "Time to run ", str(TEST_CASES), " trials: ", time

