from player import Player
from player_human import HumanPlayer
from hex_game import *


class Game:
    def __init__(self, player0: Player, player1: Player, visual_size: int = 11, board: numpy.ndarray = None):
        self.players = [player0, player1]
        self.board = init_board(visual_size) if board is None else board
        self.winner = -1
        self.moves = []
        self._winner_matrix = numpy.zeros(self.board.shape)
        self._winner_matrix[0, :] = -1
        self._winner_matrix[-1, :] = -2
        self._winner_matrix[:, 0] = 1
        self._winner_matrix[:, -1] = 2

        self.winner_counter = 3

    def get_copy(self):
        return Game(self.players[0], self.players[1], board=self.board.copy())

    def get_empty_copy(self):
        return Game(self.players[0], self.players[1], visual_size=self.board.shape[0] - 2)

    def play(self, player: int, check_for_winner: bool = True) -> PlayerResponse:
        if self.winner != -1:
            raise Exception("Game ended!")

        self.board.flags["WRITEABLE"] = False

        response = self.players[player].play_move(player, self.board.copy())

        try:
            move = response["move"]
        except ValueError:
            raise Exception("Player {} ({}) must return a 'move' value!".format(player, type(self.players[player])))
        try:
            success = response["success"]
        except ValueError:
            raise Exception("Player {} ({}) must return a 'success' value!".format(player, type(self.players[player])))
        try:
            message = response["message"]
        except ValueError:
            message = ""

        self.board.flags["WRITEABLE"] = True

        player_class = type(self.players[player]).__name__
        if not success:
            if type(self.players[player]) == HumanPlayer:
                return {"success": success, "move": move, "message": message, "player_class": player_class}
            else:
                raise Exception("Player {} ({}) failed and is not an human. Player message: {}"
                                .format(player, player_class, message))
        elif not can_play_move(self.board, move):
            raise Exception("Error for player {} ({}): Player tries to cheat. Payer move: {}. Player message: {}"
                            .format(player, player_class, move, message))
        else:
            new_response = {"success": success, "move": move, "message": message, "player_class": player_class}
            self.moves.append(new_response)
            play_move(self.board, move, player)
            if check_for_winner:
                self.check_for_winner(move, player)
            return new_response

    # TODO: do crash test against other method
    def check_for_winner(self, move: Move, player: int) -> None:
        p = (2 * player - 1)
        all_neighbors = [self._winner_matrix[n[0] + move[0], n[1] + move[1]] for n in NEIGHBORS_1]
        player_neighbors = numpy.array(list(set([k for k in all_neighbors if k * p > 0])))

        if len(player_neighbors) == 0:
            self._winner_matrix[move] = self.winner_counter * p
            self.winner_counter += 1
        elif len(player_neighbors) == 1:
            self._winner_matrix[move] = player_neighbors[0]
        elif 1 * p in player_neighbors and 2 * p in player_neighbors:
            self.winner = player
        else:
            m = min(abs(player_neighbors)) * p
            for k in player_neighbors:
                if k != m:
                    self._winner_matrix[self._winner_matrix == k] = m
            self._winner_matrix[move] = m
