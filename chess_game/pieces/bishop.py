from .piece import Piece
from chess_game.constants import BISHOP_DIRECTIONS, BOARD_SIZE


class Bishop(Piece):
    def __str__(self):
        return "♝"

    def generate_legal_moves(
        self, current_row: int, current_col: int, board, directions=None, sliding=False
    ) -> list[tuple[int, int]]:
        return super().generate_legal_moves(
            current_row, current_col, board, directions=BISHOP_DIRECTIONS, sliding=True
        )
