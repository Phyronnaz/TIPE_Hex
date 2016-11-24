from tkinter import *


class ResizingCanvas(Canvas):
    def __init__(self, parent, size, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.relative_scale = min(self.winfo_height() / size, self.winfo_width() / 1.5 / size) * 200

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        scale = float(event.width) / self.width
        self.width = event.width
        self.height = event.height

        self.relative_scale *= scale

        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, scale, scale)
