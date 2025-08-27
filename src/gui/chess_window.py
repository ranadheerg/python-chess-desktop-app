from tkinter import Tk, Frame, Button, Label, messagebox, StringVar, OptionMenu
from chess.board import Board

class ChessWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Chess Game")

        self.mode = StringVar(value="Two Player")
        self.mode_menu = OptionMenu(self.master, self.mode, "Two Player", "Play with AI", command=self.on_mode_change)
        self.mode_menu.pack(side="top")

        self.board_frame = Frame(self.master)
        self.board_frame.pack()

        self.start_button = Button(self.master, text="Start", command=self.start_game)
        self.start_button.pack(side="left")

        self.pause_button = Button(self.master, text="Pause", command=self.pause_analysis)
        self.pause_button.pack(side="left")

        self.status_label = Label(self.master, text="Welcome to Chess!")
        self.status_label.pack(side="bottom")

        self.illegal_moves_white = 0
        self.illegal_moves_black = 0
        self.illegal_label = Label(self.master, text="Illegal moves - White: 0, Black: 0")
        self.illegal_label.pack(side="bottom")

        self.board = Board()
        self.selected = None  # (row, col) of selected piece
        self.images = self.load_images()
        self.draw_board()

    def load_images(self):
        from tkinter import PhotoImage
        import os
        img_dir = "/Users/ranadheergorrepati/Downloads/pieces/"
        pieces = {
            'K': 'wK.png', 'Q': 'wQ.png', 'R': 'wR.png', 'B': 'wB.png', 'N': 'wN.png', 'P': 'wP.png',
            'k': 'bK.png', 'q': 'bQ.png', 'r': 'bR.png', 'b': 'bB.png', 'n': 'bN.png', 'p': 'bP.png',
            '.': 'blank_square.png'  # Add blank square for empty squares
        }
        images = {}
        for key, fname in pieces.items():
            path = os.path.join(img_dir, fname)
            images[key] = PhotoImage(file=path)
        return images

    def draw_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        board_state = self.board.get_board()
        for i in range(8):
            self.board_frame.rowconfigure(i, weight=1, minsize=64)
            self.board_frame.columnconfigure(i, weight=1, minsize=64)
        for i, row in enumerate(board_state):
            for j, piece in enumerate(row):
                bg = "#F0D9B5" if (i + j) % 2 == 0 else "#B58863"
                if self.selected == (i, j):
                    bg = "#FFD700"
                img = self.images[piece] if piece in self.images else self.images['.']
                widget = Button(
                    self.board_frame,
                    image=img,
                    bg=bg,
                    relief="ridge",
                    borderwidth=2,
                    command=lambda r=i, c=j: self.on_square_click(r, c)
                )
                widget.image = img  # Prevent garbage collection
                widget.grid(row=i, column=j, sticky="nsew", padx=0, pady=0)

    def on_square_click(self, row, col):
        board_state = self.board.get_board()
        piece = board_state[row][col]
        turn = self.board.current_turn

        # If AI mode and it's black's turn, block manual move
        if self.mode.get() == "Play with AI" and turn == 'black':
            self.status_label.config(text="It's my turn! Please wait.")
            return

        if self.selected is None:
            if piece != '.' and self.is_current_player_piece(piece):
                self.selected = (row, col)
                self.status_label.config(text=f"Selected {piece} at {chr(col+97)}{8-row}")
                self.draw_board()
            else:
                self.status_label.config(text="Select your own piece to move.")
        else:
            start = self.selected
            end = (row, col)
            if start == end:
                self.selected = None
                self.status_label.config(text="Selection cleared.")
                self.draw_board()
                return
            try:
                # Only catch exceptions from move validation
                if self.is_pawn_promotion(start, end):
                    promotion_piece = self.prompt_promotion(turn)
                    self.board.move_piece(start, end, promotion=promotion_piece)
                else:
                    self.board.move_piece(start, end)
                self.selected = None
                self.status_label.config(text=f"Move made: {chr(start[1]+97)}{8-start[0]} to {chr(end[1]+97)}{8-end[0]}")
                self.draw_board()
                self.check_game_end()
                self.board.current_turn = 'black' if turn == 'white' else 'white'
                if self.mode.get() == "Play with AI" and self.board.current_turn == 'black':
                    self.master.after(500, self.ai_move)
            except Exception as e:
                # Only increment illegal move count if an exception is raised
                if turn == 'white':
                    self.illegal_moves_white += 1
                else:
                    self.illegal_moves_black += 1
                self.illegal_label.config(
                    text=f"Illegal moves - White: {self.illegal_moves_white}, Black: {self.illegal_moves_black}"
                )
                self.status_label.config(text=f"Illegal move: {str(e)}")
                self.selected = None
                self.draw_board()

    def ai_move(self):
        fen = self.board.to_fen()
        move = self.get_ai_move(fen)
        if move:
            try:
                self.board.make_move(move)
                self.status_label.config(text=f"I played: {move}")
                self.draw_board()
                self.board.current_turn = 'white'
            except Exception as e:
                self.illegal_moves_black += 1
                self.illegal_label.config(
                    text=f"Illegal moves - White: {self.illegal_moves_white}, Black: {self.illegal_moves_black}"
                )
                self.status_label.config(text=f"My illegal move: {str(e)}")
        else:
            self.status_label.config(text="I have no legal moves!")

    def get_ai_move(self, fen):
        print(f"AI (Copilot) turn. Current FEN: {fen}")
        move = input("Enter Copilot's move in algebraic notation (e.g., e7e5): ")
        return move

    def is_current_player_piece(self, piece):
        turn = self.board.current_turn
        if turn == 'white':
            return piece.isupper()
        else:
            return piece.islower()

    def start_game(self):
        self.board.reset_board()
        self.status_label.config(text="Game started!")
        self.illegal_moves_white = 0
        self.illegal_moves_black = 0
        self.illegal_label.config(text="Illegal moves - White: 0, Black: 0")
        self.draw_board()

    def pause_analysis(self):
        self.status_label.config(text="Analysis paused.")

    def on_mode_change(self, value):
        self.status_label.config(text=f"Mode changed to: {value}")
        self.start_game()

    def is_pawn_promotion(self, start, end):
        piece = self.board.get_board()[start[0]][start[1]]
        if piece.lower() == 'p':
            if (piece.isupper() and end[0] == 0) or (piece.islower() and end[0] == 7):
                return True
        return False

    def prompt_promotion(self, turn):
        # Show a dialog to select promotion piece
        pieces = ['Q', 'R', 'B', 'N'] if turn == 'white' else ['q', 'r', 'b', 'n']
        import tkinter.simpledialog
        choice = tkinter.simpledialog.askstring(
            "Pawn Promotion",
            f"Promote pawn to ({', '.join(pieces)}):",
            initialvalue=pieces[0]
        )
        if choice and choice in pieces:
            return choice
        return pieces[0]  # Default to Queen

    def check_game_end(self):
        result = self.board.get_game_result()  # You need to implement this in your Board class
        if result:
            messagebox.showinfo("Game Over", result)
            self.status_label.config(text=f"Game Over: {result}")
            # Optionally disable further moves
            self.board.current_turn = None


def main():
    root = Tk()
    chess_window = ChessWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# ...existing code...

# ...existing code...