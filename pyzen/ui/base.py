import os

def img_path(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', name)
