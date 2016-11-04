from random import sample   # sample(range, num) -> random num items in range
from string import lowercase    # string of all lowercase letters


class Game(object):
    """Minesweeper."""

    def __init__(self, width, height, num_mines):
        """Initialize game. 

        - Set up Board
        - Place mines
        """

        self.num_mines = num_mines
        self.board = Board(self, width, height)
        self.board.place_mines(num_mines)

    def get_move(self):
        """Returns cell object at user inputted cell location."""

        while True:
            try: 
                move = raw_input("Enter move (row col, like 'ab'): ")
                row = ord(move[0].upper()) - ord('A')  # A -> 0, B -> 1, ...
                col = ord(move[1].upper()) - ord('A')
                cell = self.board.cells[row][col]

                # Got a legal move, can stop asking for a move
                return cell

            except (IndexError, EOFError) as e:
                print "\n(%s: try again)\n" % e

    def play(self):
        """Main game play loop"""

        try:
            while True:
                self.board.show()
                self.get_move().click()

        except GameWonException:
            end = "You won!!!"

        except GameLossException:
            end = "You Lost :("

        self.board.show(show_mines=True)
        print end


class Board(object):
    """The board"""

    def __init__(self, game, width, height):
        """Initialize the baord. 

    Set game, width, height, # cells left, and create raw grid
    """

        assert 1 <= height <= len(lowercase) and 1 <= width <= len(lowercase)

        self.game = game    # game object
        self.width = width
        self.height = height
        self.cells_left = (width * height)  # number of non-mine, uncovered cells
        self.cells = [
            [Cell(self, x, y) for x in xrange(width)] for y in xrange(height)
        ]

    def place_mines(self, num_mines):
        """Place mines and update neighbors' counts"""

        for mine_cell in sample(xrange(self.width * self.height), num_mines):
            cell = self.cells[mine_cell / self.width][mine_cell % self.width]
            cell.mine = True
            self.cells_left -= 1

            for n in cell.get_valid_neighbors():
                n.mines += 1

    def show(self, show_mines=False):
        """Show board"""

        # Print heading
        print "\n ",
        for col in lowercase[:self.width]:
            print col,  # print in one line
        print   # new line after heading

        # Print each row, with heading on left
        for i, row in enumerate(self.cells):
            print lowercase[i],

            for cell in row:
                print cell.show(show_mines=show_mines),
            print

        print   # new line after entire board


class Cell(object):
    """A cell in the board grid"""

    NEIGHBORS = [(-1, -1), (0, -1), (+1, -1),
                 (-1, 0),           (+1, 0),
                 (-1, +1), (0, +1), (+1, +1)]

    def __init__(self, board, col, row):
        self.board = board  # board object
        self.col = col  # 0 .. width-1
        self.row = row  # 0 .. height-1
        self.mine = False   # whether cell contains a mine or not
        self.uncovered = False  # whether cell is uncovered yet
        self.mines = 0  # number of adjacent mine cells

    def __repr__(self):
        """Human readable representation of cell contents"""

        return "<%s%s: %s, %s, %s>" % (
            self.row,
            self.col,
            "M" if self.mine else "",
            "U" if self.uncovered else "",
            self.mines)

    def get_valid_neighbors(self):
        """Return valid neighbors of cell within grid"""

        return [self.board.cells[self.row + r][self.col + c]
               for c, r in self.NEIGHBORS
               if (0 <= self.col + c < self.board.width and
                   0 <= self.row + r < self.board.height)]

    def reveal_and_show_neighbors(self):
        """Reveal this cell and all neighbor cells."""

        to_check = {self}
        seen = set()

        while to_check:
            cell = to_check.pop()
            seen.add(cell)

            if not cell.mine and not cell.uncovered:
                cell.uncovered = True
                self.board.cells_left -= 1

                if cell.mines == 0:
                    to_check.update(set(cell.get_valid_neighbors()) - seen)

    def click(self):
        """Uncover a cell.

        - If mine, reveal all cells and end game with loss.
        - Check and reveal neighbors. If last non-mine cell, end with win. 
        """

        if self.mine:
            raise GameLossException()

        else:
            self.reveal_and_show_neighbors()

            if self.board.cells_left == 0:
                raise GameWonException()

    def show(self, show_mines=False):
        """Show a cell"""

        if not show_mines and not self.uncovered:
            return "X"

        elif self.mine:
            return "M"

        else:
            return self.mines if self.mines > 0 else "."


class GameLossException(Exception):
    """Raised when game is lost."""


class GameWonException(Exception):
    """Raised when game is won."""


if __name__ == '__main__':
    g_width = int(raw_input("How wide would you like the board to be (0-26)? "))
    g_height = int(raw_input("How tall would you like the board to be (0-26)? "))
    g_mines = int(raw_input("How many mines would you like there to be? "))
    Game(g_width, g_height, g_mines).play()

