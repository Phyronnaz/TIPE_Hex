from Base.hex import Hex
import numpy


class AI:
    def __init__(self, nn):
        self.nn = nn

    def play_move(self, hex):
        board = numpy.reshape(hex.game, (1, hex.shape ** 2))
        r = numpy.zeros((self.nn.shape[0]))
        r = board * self.nn

        loop = True;
        c = 0;
        while loop:
            i = numpy.argmax(r)
            loop = not hex.play_move((i % hex.shape, i // hex.shape));
            r[i] = -10000000;
            c += 1
            if c == 122:
                return False;
        return True;

    def get_child(self, variation):
        return self.nn + numpy.random.rand(self.nn.shape) * variation
