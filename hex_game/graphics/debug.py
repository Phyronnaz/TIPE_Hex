debug_play_text = None
play_ui = None

def debug_play(text):
    print(text)
    if debug_play_text is not None:
        debug_play_text.appendPlainText(text)

def debug_path(path):
    print(path)
    if play_ui is not None:
        play_ui.debug_path(path)
