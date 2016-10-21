import hex_game.hex_game as hex
from hex_game.renderer import Renderer


class GameHandler:
    def __init__(self, player1: object, player2: object, size: int = 11) -> object:
        """
        Create new Game Handler
        :param player1: player 1
        :param player2: player 2
        """
        self.next_player = 0
        self.winner = -1
        self.board = hex.init_board(size=size)
        self.renderer = Renderer(self.update, self.board, debug_text=True)
        self.players = [player1, player2]
        for p in self.players:
            p.init(self.renderer)

        self.renderer.start()

    def update(self):
        if not hex.has_win(self.board, 1 - self.next_player):
            player_response = self.players[self.next_player].play_move(self.next_player, self.board)
            if not player_response:
                print("Error for player " + str(self.next_player))
            elif player_response == 2:
                pass
            else:
                self.next_player = 1 - self.next_player
        elif self.winner == -1:
            print("Player " + str(1 - self.next_player) + " won")

        return self.board
