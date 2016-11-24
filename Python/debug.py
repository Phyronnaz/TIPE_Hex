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
    debug_poisson = True
    debug_indices = True
    debug_text = True

    renderers = []
    polygons = []

    @staticmethod
    def init(renderer: Renderer):
        Debug.renderers.append(renderer)

    @staticmethod
    def create_renderer():
        r = Renderer(visual_size=Debug.renderers[0].real_size - 2)
        r.start(False)
        Debug.renderers.append(r)

    @staticmethod
    def clear():
        for r in Debug.renderers:
            r.clear_lines()
            r.clear_hexagons()

    @staticmethod
    def update(board: numpy.ndarray):
        if Debug.debug_groups:
            Debug._display_groups(board)
        if Debug.debug_poisson:
            Debug._display_poisson(board)
        if Debug.debug_indices:
            Debug.renderers[0].show_texts()
        else:
            Debug.renderers[0].hide_texts()

    @staticmethod
    def _display_groups(board: numpy.ndarray):
        groups = [get_groups(board, k) for k in [0, 1]]
        for k in [0, 1]:
            for g in groups[k]:
                color = "#" + ("%06x" % random.randint(0, 16777215))
                for c in g:
                    Debug.renderers[0].create_line(c[0], c[1], color)

    @staticmethod
    def _display_poisson(board: numpy.ndarray):
        poisson = Poisson(board)
        poisson.iterations(board.shape[0] * 5)
        Debug.display_array(poisson.U, renderer=1)

    @staticmethod
    def display_array(array: numpy.ndarray, renderer=0):
        array = array.copy()
        array[array == -float("inf")] = -0.001
        array[array == float("inf")] = 0.001
        array[array == 0.001] = numpy.abs(array).max()
        array[array == -0.001] = -numpy.abs(array).max()
        array[0, 0] = 1
        array = array / numpy.abs(array).max()
        while renderer > len(Debug.renderers) - 1:
            Debug.create_renderer()
        Debug.renderers[renderer].set_board(array)

    @staticmethod
    def start_text():
        if Debug.debug_text:
            print("""
   ____                            ____  _             _           _
  / ___| __ _ _ __ ___   ___      / ___|| |_ __ _ _ __| |_ ___  __| |
 | |  _ / _` | '_ ` _ \ / _ \     \___ \| __/ _` | '__| __/ _ \/ _` |
 | |_| | (_| | | | | | |  __/      ___) | || (_| | |  | ||  __/ (_| |
  \____|\__,_|_| |_| |_|\___|     |____/ \__\__,_|_|   \__\___|\__,_|

            """)
            Debug.print_line()

    @staticmethod
    def update_text(player: int, winner: int, player_response: PlayerResponse):
        if Debug.debug_text:
            move, success = player_response["move"], player_response["success"]
            message, player_class = player_response["message"], player_response["player_class"]

            player_class_bold = Debug.BOLD + player_class + Debug.ENDC
            move_bold = Debug.BOLD + str(move) + Debug.ENDC
            message_bold = Debug.BOLD + message + Debug.ENDC

            print("Player {} ({}) played successfully at {}. Player message: {}"
                  .format(player, player_class_bold, move_bold, message_bold))

            if winner != -1:
                Debug.print_line()
                print(Debug.BOLD + Debug.HEADER + "Player {} ({}) won.".format(player, player_class) + Debug.ENDC)
                Debug.print_line()
                Debug.end_text()

            Debug.print_line()

    @staticmethod
    def print_line(start=True, end=True):
        if start:
            print(Debug.OKBLUE)
        print("---------------------------------------------------------------------------------------")
        if end:
            print(Debug.ENDC)

    @staticmethod
    def end_text():
        if Debug.debug_text:
            print("""
   ____                            _____           _          _
  / ___| __ _ _ __ ___   ___      | ____|_ __   __| | ___  __| |
 | |  _ / _` | '_ ` _ \ / _ \     |  _| | '_ \ / _` |/ _ \/ _` |
 | |_| | (_| | | | | | |  __/     | |___| | | | (_| |  __/ (_| |
  \____|\__,_|_| |_| |_|\___|     |_____|_| |_|\__,_|\___|\__,_|

            """)
            Debug.print_line()

    @staticmethod
    def print_moves(moves: List[PlayerResponse]):
        print(Debug.BOLD + "Moves:" + Debug.ENDC)
        for player_response in moves:
            move, success = player_response["move"], player_response["success"]
            message, player_class = player_response["message"], player_response["player_class"]

            player_class_bold = Debug.BOLD + player_class + Debug.ENDC
            move_bold = Debug.BOLD + str(move) + Debug.ENDC
            message_bold = Debug.BOLD + message + Debug.ENDC

            print("Player {} played successfully at {}. Player message: {}"
                  .format(player_class_bold, move_bold, message_bold))
        Debug.print_line()

    @staticmethod
    def debug_path(path: List[Move]):
        for move in path:
            i, j = move
            Debug.renderers[0].create_hexagon(i, j, "pink", outline=False, transparent=True)
