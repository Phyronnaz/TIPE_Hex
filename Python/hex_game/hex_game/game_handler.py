from hex_game.hex_game import HexGame
from hex_game.renderer import Renderer


class GameHandler:
    def __init__(self, player1, player2, size=11):
        """
        Create new Game Handler
        :param player1: player 1
        :param player2: player 2
        """
        self.next_player = 0
        self.hex_game = HexGame(size=size)
        self.renderer = Renderer(self.update, self.hex_game, rotation=3.14 / 6, debug_text=True)
        self.players = [player1, player2]
        for p in self.players:
            p.init(self.renderer)

        self.renderer.start()

    def update(self):
        if not self.hex_game.has_win(1 - self.next_player):
            player_response = self.players[self.next_player].play_move(self.next_player, self.hex_game)
            if not player_response:
                print("Error for players " + str(self.next_player))
            elif player_response == 2:
                return
            else:
                self.next_player = 1 - self.next_player
        elif self.hex_game.winner == -1:
            print("Player " + str(self.hex_game.get_winner()) + " won")
