from chess_game.constants import KING_DIRECTIONS
from .piece import Piece


class King(Piece):
    def __str__(self):
        return "♚"

    def generate_legal_moves(
        self, current_row: int, current_col: int, board, *args, **kwargs
    ) -> list[tuple[int, int]]:
        return super().generate_legal_moves(
            current_row, current_col, board, directions=KING_DIRECTIONS
        )
