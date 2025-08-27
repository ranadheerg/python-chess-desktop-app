
from tkinter import Tk
from gui.chess_window import ChessWindow

def main():
    root = Tk()
    window = ChessWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()