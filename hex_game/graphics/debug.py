class Debug:
    debug_play_text = None

    @staticmethod
    def set_debug_play_text(obj):
        obj.clear()
        Debug.debug_play_text = obj

    @staticmethod
    def debug_play(text):
        print(text)
        Debug.debug_play_text.appendPlainText(text)