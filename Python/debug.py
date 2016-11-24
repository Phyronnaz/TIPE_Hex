import random
from renderer import Renderer
from poisson import Poisson
from tools import *


class Debug:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    debug_groups = False
    debug_poisson = False
    debug_indices = True
    debug_text = True

    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.polygons = []

    def update(self, board: numpy.ndarray):
        self.renderer.clear_lines()
        self.renderer.clear_hexagons()
        if Debug.debug_groups:
            self._display_groups(board)
        if Debug.debug_poisson:
            self._display_poisson(board)
        if Debug.debug_indices:
            self.renderer.show_texts()
        else:
            self.renderer.hide_texts()

    def _display_groups(self, board: numpy.ndarray):
        groups = [get_groups(board, k) for k in [0, 1]]
        for k in [0, 1]:
            for g in groups[k]:
                color = "#" + ("%06x" % random.randint(0, 16777215))
                for c in g:
                    self.renderer.create_line(c[0], c[1], color)

    def _display_poisson(self, board: numpy.ndarray):
        def hexa(f):
            s = str(hex(int(255 * f)))[2:]
            while len(s) < 2:
                s = "0" + s
            while len(s) > 2:
                s = s[:-1]
            return s

        poisson = Poisson(board)
        poisson.iterations(board.shape[0] * 5)
        n = poisson.U.shape[0]
        for i in range(n):
            for j in range(n):
                c = "#" + hexa(max(0, poisson.U[i, j])) + "00" + hexa(-min(0, poisson.U[i, j]))
                self.renderer.create_hexagon(i, j, c, outline=False)

    def start_text(self):
        if Debug.debug_text:
            print("""
   ____                            ____  _             _           _
  / ___| __ _ _ __ ___   ___      / ___|| |_ __ _ _ __| |_ ___  __| |
 | |  _ / _` | '_ ` _ \ / _ \     \___ \| __/ _` | '__| __/ _ \/ _` |
 | |_| | (_| | | | | | |  __/      ___) | || (_| | |  | ||  __/ (_| |
  \____|\__,_|_| |_| |_|\___|     |____/ \__\__,_|_|   \__\___|\__,_|

            """)
            self.print_line()

    def update_text(self, player: int, winner: int, player_response: PlayerResponse):
        if Debug.debug_text:
            move, success = player_response["move"], player_response["success"]
            message, player_class = player_response["message"], player_response["player_class"]

            player_class_bold = Debug.BOLD + player_class + Debug.ENDC
            move_bold = Debug.BOLD + str(move) + Debug.ENDC
            message_bold = Debug.BOLD + message + Debug.ENDC

            print("Player {} ({}) played successfully at {}. Player message: {}"
                  .format(player, player_class_bold, move_bold, message_bold))

            if winner != -1:
                self.print_line()
                print(Debug.BOLD + Debug.HEADER + "Player {} ({}) won.".format(player, player_class) + Debug.ENDC)
                self.print_line()
                self.end_text()

            self.print_line()

    def print_line(self):
        print(Debug.OKBLUE)
        print("---------------------------------------------------------------------------------------")
        print(Debug.ENDC)

    def end_text(self):
        if Debug.debug_text:
            print("""
   ____                            _____           _          _
  / ___| __ _ _ __ ___   ___      | ____|_ __   __| | ___  __| |
 | |  _ / _` | '_ ` _ \ / _ \     |  _| | '_ \ / _` |/ _ \/ _` |
 | |_| | (_| | | | | | |  __/     | |___| | | | (_| |  __/ (_| |
  \____|\__,_|_| |_| |_|\___|     |_____|_| |_|\__,_|\___|\__,_|

            """)
            self.print_line()

