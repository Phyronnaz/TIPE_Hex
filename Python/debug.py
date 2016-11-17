import random

from renderer import Renderer


def debug_groups(renderer: Renderer, groups):
    """
    Debug groups
    :param renderer: Renderer
    :param groups: [groups_player_0, groups_player_1]
    """
    for k in [0, 1]:
        for g in groups[k]:
            color = "#" + ("%06x" % random.randint(0, 16777215))
            for c in g:
                renderer.create_line(c[0], c[1], color)
