import numpy
import hex_game
from tools import Position


class PlayerMiniMax:
    def init(self, renderer):
        pass

    def play_move(self, player: int, board: numpy.ndarray) -> bool:
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        :return: 0 : fail, 1 :  success, 2 : wait
        """
        self.count = 0
        depth = 23
        moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
        move = moves[numpy.argmax(
            [-self.minimax(hex_game.play_move_copy(board, move[0], move[1], player), depth, 1 - player) for move in
             moves])]
        return hex_game.play_move(board, move[0], move[1], player)

    def minimax(self, board: numpy.ndarray, depth: int, player: int) -> float:
        """

        :param board: numpy array
        :param depth: int
        :param play_move: param : board, player, move -> board
        :param get_score: param : board, -> score player0 - score player1
        :param get_moves: param : board, player -> tuple list
        :return: score player0-score player1
        """
        self.count += 1
        if self.count % 100 == 0:
            print(self.count)
        if depth == 0:
            return hex_game.get_scores(board)[0][player]
        else:
            moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
            if len(moves) == 0:
                return hex_game.get_scores(board)[0][player]
            else:
                return max(
                    [-self.minimax(hex_game.play_move_copy(board, move[0], move[1], player), depth - 1, 1 - player)
                     for move in moves])
            
<<<<<<< Updated upstream
    def alphabeta(self, board: numpy.ndarray, depth: int, player: int, alpha: float, beta: float) -> float
        if depth == 0:
            return hex_game.get_scores(board)[0][player]
        else:
            moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
            if len(moves) == 0:
                return hex_game.get_scores(board)[0][player]
            else:
                u = -inf
                for k in moves:
                    val = -alphabeta(self, 
                
=======
    # def alphabeta(self, board: numpy.ndarray, depth: int, player: int) -> float:
    #     if depth == 0:
    #         return hex_game.get_scores(board)[0][player]
    #     else:
    #         return(noeud_max(board, depth, player, -inf, +inf))
    #     def noeud_max(board: numpy.ndarray, depth: int, player: int, alpha: float, beta: float):
    #         moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
    #         if len(moves) == 0:
    #             return hex_game.get_scores(board)[0][player]
    #         else: #à compléter
>>>>>>> Stashed changes
                
               
