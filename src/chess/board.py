import copy
class Board:
    def get_board(self):
        return self.board
    def __init__(self):
        self.board = self.create_initial_board()
        self.current_turn = 'white'
        self.move_history = []

    def create_initial_board(self):
        # Initialize the board with pieces in their starting positions
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def is_valid_move(self, start_pos, end_pos):
        # Implement logic to validate moves based on chess rules
        return True  # Placeholder for actual validation logic

    def move_piece(self, start_pos, end_pos):
        if self.is_valid_move(start_pos, end_pos):
            piece = self.board[start_pos[0]][start_pos[1]]
            self.board[end_pos[0]][end_pos[1]] = piece
            self.board[start_pos[0]][start_pos[1]] = '.'
            self.move_history.append((start_pos, end_pos))
            self.switch_turn()
        else:
            raise ValueError("Illegal move")

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def get_fen(self):
        # Convert the board state to FEN format
        fen = ''
        for row in self.board:
            empty_count = 0
            for square in row:
                if square == '.':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += square
            if empty_count > 0:
                fen += str(empty_count)
            fen += '/'
        return fen[:-1] + ' ' + self.current_turn[0] + ' - - 0 1'  # Placeholder for full FEN string

    def reset_board(self):
        self.board = self.create_initial_board()
        self.current_turn = 'white'
        self.move_history = []
    
    def get_board(self):
        return copy.deepcopy(self.board)

    def get_piece(self, pos):
        row, col = pos
        return self.board[row][col]

    def is_legal(self, start, end):
        piece = self.get_piece(start)
        if piece == '.':
            return False
        if self.current_turn == 'white' and not piece.isupper():
            return False
        if self.current_turn == 'black' and not piece.islower():
            return False
        if piece.upper() == 'P':
            return self.is_legal_pawn_move(start, end)
        elif piece.upper() == 'R':
            return self.is_legal_rook_move(start, end)
        elif piece.upper() == 'N':
            return self.is_legal_knight_move(start, end)
        elif piece.upper() == 'B':
            return self.is_legal_bishop_move(start, end)
        elif piece.upper() == 'Q':
            return self.is_legal_queen_move(start, end)
        elif piece.upper() == 'K':
            return self.is_legal_king_move(start, end)
        return False

    def move_piece(self, start, end):
        if not self.is_legal(start, end):
            raise Exception("Illegal move")
        piece = self.get_piece(start)
        target = self.get_piece(end)
        # En passant
        if piece.upper() == 'P' and self.en_passant_target == end and target == '.':
            if piece.isupper():
                self.board[end[0]+1][end[1]] = '.'
            else:
                self.board[end[0]-1][end[1]] = '.'
        # Castling
        if piece.upper() == 'K' and abs(start[1] - end[1]) == 2:
            if end[1] == 6:  # King-side
                rook_start = (start[0], 7)
                rook_end = (start[0], 5)
            else:  # Queen-side
                rook_start = (start[0], 0)
                rook_end = (start[0], 3)
            self.board[rook_end[0]][rook_end[1]] = self.board[rook_start[0]][rook_start[1]]
            self.board[rook_start[0]][rook_start[1]] = '.'
        # Move piece
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = '.'
        # Pawn promotion (to Queen for simplicity)
        if piece.upper() == 'P':
            if piece.isupper() and end[0] == 0:
                self.board[end[0]][end[1]] = 'Q'
            elif piece.islower() and end[0] == 7:
                self.board[end[0]][end[1]] = 'q'
        # Update en passant target
        self.en_passant_target = None
        if piece.upper() == 'P' and abs(start[0] - end[0]) == 2:
            ep_row = (start[0] + end[0]) // 2
            self.en_passant_target = (ep_row, start[1])
        # Update castling rights
        if piece.upper() == 'K':
            self.castling_rights[self.current_turn]['K'] = False
            self.castling_rights[self.current_turn]['Q'] = False
        if piece.upper() == 'R':
            if start == (7,0): self.castling_rights['white']['Q'] = False
            if start == (7,7): self.castling_rights['white']['K'] = False
            if start == (0,0): self.castling_rights['black']['Q'] = False
            if start == (0,7): self.castling_rights['black']['K'] = False
        # Update turn
        self.last_move = (start, end)
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        if self.current_turn == 'white':
            self.fullmove_number += 1

    def is_legal_pawn_move(self, start, end):
        sr, sc = start
        er, ec = end
        piece = self.get_piece(start)
        direction = -1 if piece.isupper() else 1
        start_row = 6 if piece.isupper() else 1
        # Forward move
        if sc == ec and self.get_piece(end) == '.':
            if er - sr == direction:
                return True
            if sr == start_row and er - sr == 2 * direction and self.get_piece((sr + direction, sc)) == '.':
                return True
        # Capture
        if abs(sc - ec) == 1 and er - sr == direction:
            if self.get_piece(end) != '.' and self.is_opponent_piece(piece, self.get_piece(end)):
                return True
            # En passant
            if self.en_passant_target == end:
                return True
        return False

    def is_legal_rook_move(self, start, end):
        sr, sc = start
        er, ec = end
        if sr != er and sc != ec:
            return False
        if not self.is_path_clear(start, end):
            return False
        return self.is_target_valid(start, end)

    def is_legal_knight_move(self, start, end):
        sr, sc = start
        er, ec = end
        if (abs(sr-er), abs(sc-ec)) in [(2,1),(1,2)]:
            return self.is_target_valid(start, end)
        return False

    def is_legal_bishop_move(self, start, end):
        sr, sc = start
        er, ec = end
        if abs(sr-er) != abs(sc-ec):
            return False
        if not self.is_path_clear(start, end):
            return False
        return self.is_target_valid(start, end)

    def is_legal_queen_move(self, start, end):
        return self.is_legal_rook_move(start, end) or self.is_legal_bishop_move(start, end)

    def is_legal_king_move(self, start, end):
        sr, sc = start
        er, ec = end
        if abs(sr-er) <= 1 and abs(sc-ec) <= 1:
            return self.is_target_valid(start, end)
        # Castling
        if sr == er and abs(sc-ec) == 2:
            color = 'white' if self.get_piece(start).isupper() else 'black'
            if sc < ec:  # King-side
                rook_pos = (sr, 7)
                path = [(sr, sc+1), (sr, sc+2)]
            else:  # Queen-side
                rook_pos = (sr, 0)
                path = [(sr, sc-1), (sr, sc-2), (sr, sc-3)]
            # Check castling rights
            if not self.castling_rights[color]['K' if sc < ec else 'Q']:
                return False
            # Check rook present
            rook_piece = self.get_piece(rook_pos)
            if rook_piece.upper() != 'R' or (color == 'white' and not rook_piece.isupper()) or (color == 'black' and not rook_piece.islower()):
                return False
            # Check path clear
            for pos in path:
                if self.get_piece(pos) != '.':
                    return False
            # TODO: Check squares not attacked (requires attack detection)
            return True
        return False

    def is_path_clear(self, start, end):
        sr, sc = start
        er, ec = end
        dr = er - sr
        dc = ec - sc
        if dr == 0 and dc == 0:
            return False
        step_r = (dr and (1 if dr > 0 else -1)) if dr != 0 else 0
        step_c = (dc and (1 if dc > 0 else -1)) if dc != 0 else 0
        r, c = sr + step_r, sc + step_c
        while (r, c) != (er, ec):
            if self.board[r][c] != '.':
                return False
            r += step_r
            c += step_c
        return True

    def is_target_valid(self, start, end):
        piece = self.get_piece(start)
        target = self.get_piece(end)
        if target == '.':
            return True
        return self.is_opponent_piece(piece, target)

    def is_opponent_piece(self, piece, target):
        return (piece.isupper() and target.islower()) or (piece.islower() and target.isupper())

    def to_fen(self):
        fen_rows = []
        for row in self.board:
            empty = 0
            fen_row = ''
            for cell in row:
                if cell == '.':
                    empty += 1
                else:
                    if empty:
                        fen_row += str(empty)
                        empty = 0
                    fen_row += cell
            if empty:
                fen_row += str(empty)
            fen_rows.append(fen_row)
        fen = '/'.join(fen_rows)
        fen += ' ' + ('w' if self.current_turn == 'white' else 'b')
        # Castling rights
        cr = ''
        if self.castling_rights['white']['K']: cr += 'K'
        if self.castling_rights['white']['Q']: cr += 'Q'
        if self.castling_rights['black']['K']: cr += 'k'
        if self.castling_rights['black']['Q']: cr += 'q'
        fen += ' ' + (cr if cr else '-')
        # En passant
        if self.en_passant_target:
            fen += ' ' + self.coord_to_alg(self.en_passant_target)
        else:
            fen += ' -'
        fen += f' {self.halfmove_clock} {self.fullmove_number}'
        return fen

    def coord_to_alg(self, coord):
        row, col = coord
        return chr(col + ord('a')) + str(8 - row)

    def make_move(self, move):
        # move should be in algebraic notation, e.g., 'e2e4'
        if len(move) != 4:
            raise Exception("Invalid move format")
        start = (8 - int(move[1]), ord(move[0]) - ord('a'))
        end = (8 - int(move[3]), ord(move[2]) - ord('a'))
        self.move_piece(start, end)
    