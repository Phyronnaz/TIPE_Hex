from debug import Debug
from player import Player
from renderer import Renderer
from game import Game
from player_human import HumanPlayer


class GameHandler:
    def __init__(self, player0: Player, player1: Player, visual_size: int = 11) -> object:
        """
        Create new Game Handler
        :param player0: player 0
        :param player1: player 1
        """
        self.next_player = 0
        self.game = Game(player0, player1, visual_size)
        self.renderer = Renderer(update_board=self.update, visual_size=visual_size)
        Debug.init(self.renderer)
        for p in [player0, player1]:
            if type(p) == HumanPlayer:
                p.init(self.renderer)

        Debug.start_text()
        Debug.update(self.game.board)
        self.renderer.canvas.bind("p", lambda event: self.toggle("poisson"))
        self.renderer.canvas.bind("t", lambda event: self.toggle("text"))
        self.renderer.canvas.bind("g", lambda event: self.toggle("groups"))
        self.renderer.canvas.bind("i", lambda event: self.toggle("indices"))
        self.renderer.canvas.bind("r", lambda event: self.restart())
        self.renderer.canvas.bind("m", lambda event: self.print_moves())
        self.renderer.start()

    def update(self):
        is_human = type(self.game.players[self.next_player]) == HumanPlayer
        if not is_human:
            Debug.clear()

        if self.game.winner == -1:
            response = self.game.play(self.next_player)
            if not is_human or response["success"]:
                self.next_player = 1 - self.next_player
                if is_human:
                    Debug.clear()
                Debug.update(self.game.board)
                Debug.update_text(self.next_player, self.game.winner, response)
        return self.game.board

    def toggle(self, s):
        if s == "poisson":
            Debug.debug_poisson = not Debug.debug_poisson
        elif s == "text":
            Debug.debug_text = not Debug.debug_text
        elif s == "groups":
            Debug.debug_groups = not Debug.debug_groups
        elif s == "indices":
            Debug.debug_indices = not Debug.debug_indices
        else:
            raise Exception("Unknow toggle: {}".format(s))
        Debug.update(self.game.board)

    def restart(self):
        self.game = self.game.get_empty_copy()
        self.next_player = 0
        Debug.start_text()

    def print_moves(self):
        Debug.print_moves(self.game.moves)
