class MoveTracker:
    def __init__(self):
        self.moves = []
        self.illegal_moves = []

    def log_move(self, move):
        if self.is_legal_move(move):
            self.moves.append(move)
        else:
            self.illegal_moves.append(move)

    def is_legal_move(self, move):
        # Placeholder for legality check logic
        # This should integrate with the Board class to validate moves
        return True  # Replace with actual legality check

    def get_illegal_moves(self):
        return self.illegal_moves

    def reset(self):
        self.moves = []
        self.illegal_moves = []