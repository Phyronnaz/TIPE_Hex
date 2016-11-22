from typing import Type
from poisson import Poisson
from hex_game import *
from tools import *
from debug import *
from player import Player
from renderer import Renderer


class GameHandler:
    def __init__(self, player1: Type[Player], player2: Type[Player], visual_size: int = 11, scale: float = 30) -> object:
        """
        Create new Game Handler
        :param player1: player 1
        :param player2: player 2
        """
        self.next_player = 0
        self.winner = -1
        self.board = init_board(visual_size=visual_size)
        self.renderer = Renderer(update_board=self.update, visual_size=visual_size, debug_text=True, scale=scale)
        self.players = [player1, player2]
        for p in self.players:
            p.init(self.renderer)

        # TODO: lambdas
        self.renderer.canvas.bind("p", self.toggle_poisson)
        self.renderer.canvas.bind("r", self.restart)

        print("///////////////////////////")
        print("Game Started")
        print("///////////////////////////")

        self.renderer.start()

    def update(self):
        if self.winner == -1:
            if not has_win(self.board, 1 - self.next_player):
                player_response = self.players[self.next_player].play_move(self.next_player, self.board)
                if not player_response:
                    raise Exception("Error for player " + str(self.next_player))
                elif player_response == 2:
                    pass
                else:
                    self.renderer.clear_lines()
                    # Debug groups and scores
                    debug_groups(self.renderer, [get_groups(self.board, k) for k in [0, 1]])
                    class_name = str(type(self.players[self.next_player]).__name__)
                    print(class_name + " (Player " + str(self.next_player) + ") played")
                    print("New Scores:", get_scores(self.board)[0])
                    if self.poisson_enabled:
                        self.toggle_poisson()
                        self.toggle_poisson()
                    print("///////////////////////////")
                    self.next_player = 1 - self.next_player
            else:
                self.winner = 1 - self.next_player
                print("Player " + str(self.winner) + " won")

        return self.board

    def toggle_poisson(self, event=None):
        if self.poisson_enabled:
            for p in self.polygons:
                self.renderer.canvas.delete(p)
        else:
            self.poisson()
        self.poisson_enabled = not self.poisson_enabled

    def poisson(self):
        def hexa(f):
            s = str(hex(int(255 * f)))[2:]
            while len(s) < 2:
                s = "0" + s
            while len(s) > 2:
                s = s[:-1]
            return s

        poisson = Poisson(self.board)
        poisson.iterations(self.board.shape[0] * 5)
        n = poisson.U.shape[0]
        for i in range(n):
            for j in range(n):
                c = "#" + hexa(max(0, poisson.U[i, j])) + "00" + hexa(-min(0, poisson.U[i, j]))
                self.polygons.append(self.renderer.create_hexagon(i, j, c, outline=False))

        print("Norme: {}".format(poisson.norme()))

    def restart(self, event=None):
        self.board = init_board(visual_size=self.board.shape[0] - 2)
        if self.poisson_enabled:
            self.toggle_poisson()
        self.next_player = 0
        self.winner = -1
