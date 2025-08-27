def board_to_fen(board):
    fen = ""
    empty_count = 0

    for row in board:
        for square in row:
            if square is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                fen += square
        if empty_count > 0:
            fen += str(empty_count)
            empty_count = 0
        fen += "/"

    fen = fen[:-1]  # Remove the trailing slash
    return fen

def fen_to_board(fen):
    board = []
    rows = fen.split("/")
    
    for row in rows:
        board_row = []
        for char in row:
            if char.isdigit():
                board_row.extend([None] * int(char))
            else:
                board_row.append(char)
        board.append(board_row)
    
    return board

def is_valid_fen(fen):
    # Basic validation for FEN format
    parts = fen.split()
    if len(parts) != 6:
        return False

    # Validate the board part
    rows = parts[0].split("/")
    if len(rows) != 8:
        return False

    for row in rows:
        count = 0
        for char in row:
            if char.isdigit():
                count += int(char)
            elif char in "rnbqkpRNBQKP":
                count += 1
            else:
                return False
        if count != 8:
            return False

    return True