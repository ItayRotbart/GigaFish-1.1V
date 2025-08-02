from .piece import Piece


class Queen(Piece):
    def __str__(self):
        return "♛"

    def generate_legal_moves(
        self, current_row: int, current_col: int, board, *args, **kwargs
    ) -> list[tuple[int, int]]:
        pass
