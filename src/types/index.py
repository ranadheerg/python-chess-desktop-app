# This file exports types and constants used throughout the application, such as piece types and move formats.

PIECE_TYPES = {
    'P': 'Pawn',
    'R': 'Rook',
    'N': 'Knight',
    'B': 'Bishop',
    'Q': 'Queen',
    'K': 'King'
}

MOVE_FORMATS = {
    'normal': 'e2e4',
    'capture': 'e2xe4',
    'castling': 'O-O',
    'promotion': 'e7e8=Q'
}