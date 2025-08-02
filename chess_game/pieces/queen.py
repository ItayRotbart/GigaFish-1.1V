from .piece import Piece
from chess_game.constants import BISHOP_DIRECTIONS, ROOK_DIRECTIONS


class Queen(Piece):
    def __str__(self):
        return "♛"

    def generate_legal_moves(
        self, current_row: int, current_col: int, board, directions=None, sliding=False
    ) -> list[tuple[int, int]]:
        queen_directions = BISHOP_DIRECTIONS + ROOK_DIRECTIONS
        return super().generate_legal_moves(
            current_row, current_col, board, directions=queen_directions, sliding=True
        )
