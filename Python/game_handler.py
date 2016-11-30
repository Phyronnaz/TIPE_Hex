from tkinter import *
from display import Display
from player import Player
from renderer import Renderer
from game import Game
from player_human import HumanPlayer


class GameHandler:
    def __init__(self, player0: Player, player1: Player, visual_size: int = 11, rate=50):
        """
        Create new Game Handler
        :param player0: player 0
        :param player1: player 1
        :param visual_size: size of the board
        :param rate: time between refresh in ms
        """
        self.rate = rate
        self.next_player = 0
        self.game = Game(player0, player1, visual_size)

        # Initialize Tk and Canvas
        self.master = Tk()
        self.canvas = Canvas(self.master)

        # Init buttons
        self.debug_text = IntVar(value=Display.debug_text)
        self.debug_groups = IntVar(value=Display.debug_groups)
        self.debug_indices = IntVar(value=Display.debug_indices)
        self.debug_paths = IntVar(value=Display.debug_paths)
        self.debug_poisson_ai = IntVar(value=Display.debug_poisson_ai)
        self.debug_poisson = IntVar(value=Display.debug_poisson)

        self.checkbuttons = [Checkbutton(self.master, text="Debug text", variable=self.debug_text,
                                         command=self.update_values),
                             Checkbutton(self.master, text="Display groups", variable=self.debug_groups,
                                         command=self.update_values),
                             Checkbutton(self.master, text="Display indices", variable=self.debug_indices,
                                         command=self.update_values),
                             Checkbutton(self.master, text="Display paths", variable=self.debug_paths,
                                         command=self.update_values),
                             Checkbutton(self.master, text="Display poisson ai", variable=self.debug_poisson_ai,
                                         command=self.update_values),
                             Checkbutton(self.master, text="Display poisson", variable=self.debug_poisson,
                                         command=self.update_values)]

        for c in self.checkbuttons:
            c.pack()

        self.canvas.pack()
        self.canvas.update()

        # Setup renderer
        self.renderer = Renderer(visual_size=visual_size)
        self.renderer.canvas.bind("m", lambda event: self.print_moves())
        self.renderer.canvas.bind("r", lambda event: self.restart())

        # Init Display
        Display.init(self.renderer)
        Display.start_text()
        Display.update(self.game.board)

        self.master.after(self.rate, self.update)
        mainloop()

    def update(self):
        is_human = type(self.game.players[self.next_player]) == HumanPlayer

        if not is_human:
            Display.clear()

        if self.game.winner == -1:
            response = self.game.play(self.next_player)
            if not is_human or response["success"]:
                if is_human:
                    Display.clear()
                self.next_player = 1 - self.next_player
                Display.update(self.game.board)
                Display.update_text(self.next_player, self.game.winner, response)

        self.renderer.set_board(self.game.board, white=True)
        self.master.after(self.rate, self.update)

    def restart(self):
        self.game = self.game.get_empty_copy()
        self.next_player = 0
        Display.start_text()

    def update_values(self):
        Display.debug_text = self.debug_text.get()
        Display.debug_groups = self.debug_groups.get()
        Display.debug_indices = self.debug_indices.get()
        Display.debug_paths = self.debug_paths.get()
        Display.debug_poisson_ai = self.debug_poisson_ai.get()
        Display.debug_poisson = self.debug_poisson.get()

        Display.clear()
        Display.update(self.game.board)

    def print_moves(self):
        Display.print_moves(self.game.moves)
