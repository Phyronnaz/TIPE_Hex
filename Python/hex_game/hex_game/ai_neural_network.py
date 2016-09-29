import numpy

from hex_game.player import Player


class NeuralNetworkAI(Player):
    def __init__(self, size, neural_network=None):
        """
        Create new Neural Network AI
        :param size: Size of the board
        :param neural_network: Neural Network of this AI
        """

        self.neural_network = neural_network if not neural_network is None else numpy.random.rand(size ** 2, size ** 2)

    def play_move(self, player, hex_game):
        """
        Play a move
        :param player: Player playing
        :param hex_game: Hex Game to play on
        :return: Whether or not it succeed to play
        """
        board = numpy.reshape(hex_game.board, (1, hex_game.size ** 2)) - numpy.ones((1, hex_game.size ** 2))

        r = board * self.neural_network

        has_played = False
        count = 0
        while not has_played and count < 122:
            i = numpy.argmax(r)
            has_played = hex_game.play_move(i % hex_game.size, i // hex_game.size, player);
            r[i] = -10000000
            count += 1
        return has_played

    def get_child(self, variation):
        """
        Get AI child
        :param variation: variation between the child and the parent
        :return: NeuralNetworkAI
        """
        return self.neural_network + numpy.random.rand(self.neural_network.shape) * variation
