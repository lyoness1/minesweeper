import minesweeper as ms
import solver
import unittest

from contextlib import contextmanager

@contextmanager
def mockRawInput(mock):
    original_raw_input = __builtins__.raw_input
    __builtins__.raw_input = lambda _: mock
    yield
    __builtins__.raw_input = original_raw_input


class MinesweeperGameUnitTestCase(unittest.TestCase):
    """Unit tests for minesweeper Game class."""

    def setUp(self):
        """Stuff to do before every test."""
        self.game = ms.Game(10, 10, 10)
        self.losing_game = ms.Game(1, 1, 1)
        self.winning_game = ms.Game(1, 1, 0)

    def tearDown(self):
        """Do at end of every test."""
        del self.game
        del self.losing_game
        del self.winning_game

    def test_get_move_ok(self):
        with mockRawInput('aa'):
            self.assertIsInstance(self.game.get_move(), ms.Cell)

    def test_get_move_index_error(self):
        with mockRawInput('zz'):
            self.assertRaises(IndexError)

    def test_get_move_eof_error(self):
        with mockRawInput(''):
            self.assertRaises(EOFError)

    def test_play_ok(self, cell):
        with mockRawInput('aa'):
            

    def test_play_win_exception(self):
        with mockRawInput('aa'):
            self.losing_game.play()
            self.assertRaises(ms.GameLossException)

    def test_play_lose_exception(self):
        with mockRawInput('aa'):
            self.winning_game.play()
            self.assertRaises(ms.GameWonException)

    



if __name__ == '__main__':
    unittest.main()