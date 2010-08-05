import sys

def load_ui():
    if sys.platform == 'darwin':
        from pyzen.ui.osx import GrowlUI
        return GrowlUI()
    elif sys.platform == 'win32':
        from pyzen.ui.win32 import Win32UI
        return Win32UI()
    else:
        return None