from hex_game.hex_game import HexGame
from hex_game.player_human import HumanPlayer
from hex_game.renderer import Renderer


class GameHandler:
    def __init__(self, player1=None, player2=None):
        """
        Create new Game Handler
        :param player1: player 1, human if not specified
        :param player2: player 2, human if not specified
        """
        self.next_player = 1
        self.hex_game = HexGame()
        self.renderer = Renderer(self.update, self.hex_game)

        player1 = player1 if player1 is not None else HumanPlayer(self.renderer)
        player2 = player2 if player2 is not None else HumanPlayer(self.renderer)
        self.player = [player1, player2]
        self.renderer.start()

    def update(self):
        if not self.hex_game.has_win(3 - self.next_player):
            player_response = self.player[self.next_player - 1].play_move(self.next_player, self.hex_game)
            if not player_response:
                print("Error for player " + str(self.next_player))
            elif player_response == 2:
                return
            else:
                self.next_player = 3 - self.next_player
        elif self.hex_game.winner == 0:
            print("Player " + str(self.hex_game.get_winner()) + " won")
