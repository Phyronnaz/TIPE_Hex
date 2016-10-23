from typing import Type

import hex_game.debug as debug
import hex_game.hex_game as hex
import hex_game.tools as tools
from hex_game.player import Player
from hex_game.renderer import Renderer


class GameHandler:
    def __init__(self, player1: Type[Player], player2: Type[Player], size: int = 11) -> object:
        """
        Create new Game Handler
        :param player1: player 1
        :param player2: player 2
        """
        self.next_player = 0
        self.winner = -1
        self.board = hex.init_board(size=size)
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
            if not hex.has_win(self.board, 1 - self.next_player):
                player_response = self.players[self.next_player].play_move(self.next_player, self.board)
                if not player_response:
                    raise Exception("Error for player " + str(self.next_player))
                elif player_response == 2:
                    pass
                else:
                    self.renderer.clear_lines()
                    # Debug groups and scores
                    debug.debug_groups(self.renderer, [tools.get_groups(self.board, k) for k in [0, 1]])
                    class_name = str(type(self.players[self.next_player]).__name__)
                    print(class_name + " (Player " + str(self.next_player) + ") played")
                    print("///////////////////////////")
                    self.next_player = 1 - self.next_player
            else:
                self.winner = 1 - self.next_player
                print("Player " + str(self.winner) + " won")

        return self.board
