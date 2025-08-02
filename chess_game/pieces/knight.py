from chess_game.constants import KNIGHT_DIRECTIONS
from .piece import Piece


class Knight(Piece):
    def __str__(self):
        return "♞"

    def generate_legal_moves(
        self, current_row: int, current_col: int, board, directions=None, sliding=False
    ) -> list[tuple[int, int]]:
        return super().generate_legal_moves(
            current_row, current_col, board, directions=KNIGHT_DIRECTIONS
        )
