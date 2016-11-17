from hex_game import *
from tools import *
from player import Player


class SimpleAI(Player):
    def init(self, renderer):
        pass

    def play_move(self, player: int, board: numpy.ndarray) -> int:
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        :return: 0 : fail, 1 :  success, 2 : wait
        """
        nombre_coup = get_move_count(board)
        if nombre_coup <= 1:
            return self.first_move(player, board)
        # elif:


                # for c in group:
                #     if c[2] == 1:
                #         p1, p2 = tools.get_common_neighbours(c[0], c[1])
                #         if board[p1] == -1 and board[p2] == 1 - player:
                #             moves += [(len(moves), p1)]
                #         elif board[p2] == -1 and board[p1] == 1 - player:
                #             moves += [(len(moves), p2)]
                # if len(moves) == 0:
                #     return None
                # else:
                #     print("Counter counter")
                #     return moves
