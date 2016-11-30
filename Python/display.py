import random
from renderer import Renderer
from poisson import Poisson
from tools import *


class Display:
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
    debug_paths = False
    debug_poisson_ai = False

    renderers = []
    polygons = []

    @staticmethod
    def init(renderer: Renderer):
        Display.renderers.append(renderer)

    @staticmethod
    def _create_renderer():
        r = Renderer(visual_size=Display.renderers[0].real_size - 2)
        return r

    @staticmethod
    def clear():
        for r in Display.renderers:
            r.clear_lines()
            r.clear_hexagons()

    @staticmethod
    def update(board: numpy.ndarray):
        if Display.debug_groups:
            Display._display_groups(board)
        if Display.debug_poisson:
            Display._display_poisson(board)
        if Display.debug_indices:
            Display.renderers[0].show_texts()
        else:
            Display.renderers[0].hide_texts()

    @staticmethod
    def _display_groups(board: numpy.ndarray):
        groups = [get_groups(board, k) for k in [0, 1]]
        for k in [0, 1]:
            for g in groups[k]:
                color = "#" + ("%06x" % random.randint(0, 16777215))
                for c in g:
                    Display.renderers[0].create_line(c[0], c[1], color)

    @staticmethod
    def _display_poisson(board: numpy.ndarray):
        poisson = Poisson(board)
        poisson.iterations(board.shape[0] * 5)
        Display._display_array(poisson.U, renderer=1)

    @staticmethod
    def _display_array(array: numpy.ndarray, renderer=0):
        array = array.copy()
        array[array == -float("inf")] = -0.001
        array[array == float("inf")] = 0.001
        array[array == 0.001] = numpy.abs(array).max()
        array[array == -0.001] = -numpy.abs(array).max()
        array[0, 0] = 1
        array = array / numpy.abs(array).max()
        while renderer > len(Display.renderers) - 1:
            Display.renderers.append(None)
        if Display.renderers[renderer] is None:
            Display.renderers[renderer] = Display._create_renderer()
        Display.renderers[renderer].set_board(array)

    @staticmethod
    def start_text():
        if Display.debug_text:
            print("""
   ____                            ____  _             _           _
  / ___| __ _ _ __ ___   ___      / ___|| |_ __ _ _ __| |_ ___  __| |
 | |  _ / _` | '_ ` _ \ / _ \     \___ \| __/ _` | '__| __/ _ \/ _` |
 | |_| | (_| | | | | | |  __/      ___) | || (_| | |  | ||  __/ (_| |
  \____|\__,_|_| |_| |_|\___|     |____/ \__\__,_|_|   \__\___|\__,_|

            """)
            Display.print_line()

    @staticmethod
    def update_text(player: int, winner: int, player_response: PlayerResponse):
        if Display.debug_text:
            move, success = player_response["move"], player_response["success"]
            message, player_class = player_response["message"], player_response["player_class"]

            player_class_bold = Display.BOLD + player_class + Display.ENDC
            move_bold = Display.BOLD + str(move) + Display.ENDC
            message_bold = Display.BOLD + message + Display.ENDC

            print("Player {} ({}) played successfully at {}. Player message: {}"
                  .format(player, player_class_bold, move_bold, message_bold))

            if winner != -1:
                Display.print_line()
                print(Display.BOLD + Display.HEADER + "Player {} ({}) won.".format(player, player_class) + Display.ENDC)
                Display.print_line()
                Display.end_text()

            Display.print_line()

    @staticmethod
    def print_line(start=True, end=True):
        if start:
            print(Display.OKBLUE)
        print("---------------------------------------------------------------------------------------")
        if end:
            print(Display.ENDC)

    @staticmethod
    def end_text():
        if Display.debug_text:
            print("""
   ____                            _____           _          _
  / ___| __ _ _ __ ___   ___      | ____|_ __   __| | ___  __| |
 | |  _ / _` | '_ ` _ \ / _ \     |  _| | '_ \ / _` |/ _ \/ _` |
 | |_| | (_| | | | | | |  __/     | |___| | | | (_| |  __/ (_| |
  \____|\__,_|_| |_| |_|\___|     |_____|_| |_|\__,_|\___|\__,_|

            """)
            Display.print_line()

    @staticmethod
    def print_moves(moves: List[PlayerResponse]):
        print(Display.BOLD + "Moves:" + Display.ENDC)
        for player_response in moves:
            move, success = player_response["move"], player_response["success"]
            message, player_class = player_response["message"], player_response["player_class"]

            player_class_bold = Display.BOLD + player_class + Display.ENDC
            move_bold = Display.BOLD + str(move) + Display.ENDC
            message_bold = Display.BOLD + message + Display.ENDC

            print("Player {} played successfully at {}. Player message: {}"
                  .format(player_class_bold, move_bold, message_bold))
        Display.print_line()

    @staticmethod
    def display_path(path: List[Move]):
        if Display.debug_paths:
            last_move = path[0]
            for move in path:
                i, j = move
                Display.renderers[0].create_hexagon(i, j, "pink", outline=False, transparent=True)
                Display.renderers[0].create_line(last_move, move, arrow=True)
                last_move = move

    @staticmethod
    def display_poisson_ai(array: numpy.ndarray):
        if Display.debug_poisson_ai:
            Display._display_array(array, 2)
