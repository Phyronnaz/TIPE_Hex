import numpy


class Player:
    def play_move(self, player, hex_game):
        """
        Play a move
        :param player: Player playing
        :param hex_game: Hex Game to play on
        :return: Whether or not it succeed to play
        """
        tries_count = 0
        has_played = False
        while not has_played and tries_count < 1000:
            tries_count += 1
            move = (numpy.random.randint(hex_game.size), numpy.random.randint(hex_game.size))
            has_played = hex_game.play_move(move, player)

        return has_played
