from editor import Editor
from game import Game

if __name__ == "__main__":
    editormode=True
    if editormode:
        game= Editor()
    else:
        game = Game()
    game.run()
