from typing import Type

from hex_game import *
from tools import *
from debug import *
from player import Player
from renderer import Renderer


class GameHandler:
    def __init__(self, player1: Type[Player], player2: Type[Player], size: int = 11) -> object:
        """
        Create new Game Handler
        :param player1: player 1
        :param player2: player 2
        """
        self.next_player = 0
        self.winner = -1
        self.board = init_board(size=size)
        self.renderer = Renderer(update_board=self.update, size=size, debug_text=True)
        self.players = [player1, player2]
        for p in self.players:
            p.init(self.renderer)

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
                    print("New Score:")
                    print(get_scores(self.board))
                    print("///////////////////////////")
                    self.next_player = 1 - self.next_player
            else:
                self.winner = 1 - self.next_player
                print("Player " + str(self.winner) + " won")

        return self.board
