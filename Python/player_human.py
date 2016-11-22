from hex_game import *
from player import Player
from debug import Debug


class HumanPlayer(Player):
    def __init__(self):
        self.click_position = None
        self.renderer = None

    def init(self, renderer):
        self.renderer = renderer
        self.renderer.click_delegates.append(self.click)

    def play_move(self, player: int, board: numpy.ndarray) -> PlayerResponse:
        if self.click_position is None:
            success = False
            message = Debug.WARNING + "Waiting for click"
            move = None
        else:
            move = self.click_position
            self.click_position = None
            success = can_play_move(board, move, player)
            message = "Click"

        return {'move': move, 'success': success, 'message': message}

    def click(self, event):
        id = event.widget.find_closest(event.x, event.y)
        s = self.renderer.canvas.gettags(id)
        if len(s) >= 2:
            self.click_position = int(s[0]), int(s[1])
