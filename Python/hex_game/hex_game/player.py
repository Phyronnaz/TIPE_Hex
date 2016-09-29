import numpy


class Player:
    def play_move(self, player, hex_game):
        """
        Play a move
        :param player: Player playing
        :param hex_game: Hex Game to play on
        :return: 0 : fail, 1 :  success, 2 : wait
        """
        tries_count = 0
        has_played = False
        while not has_played and tries_count < hex_game.size ** 2:
            tries_count += 1
            x = numpy.random.randint(hex_game.size)
            y = numpy.random.randint(hex_game.size)
            has_played = hex_game.play_move(x, y, player)

        return has_played
