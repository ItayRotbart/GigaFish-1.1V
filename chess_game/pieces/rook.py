from chess_game.constants import BOARD_SIZE, ROOK_DIRECTIONS
from .piece import Piece


class Rook(Piece):
    def __str__(self):
        return "♜"

    def generate_legal_moves(
        self, current_row: int, current_col: int, board, *args, **kwargs
    ) -> list[tuple[int, int]]:
        legal_moves = []

        for row_dir, col_dir in ROOK_DIRECTIONS:
            for step in range(1, BOARD_SIZE):
                new_row = current_row + (row_dir * step)
                new_col = current_col + (col_dir * step)
                square = board.get_piece(new_row, new_col)

                if square is False:
                    break
                if square is not None and square.color == self.color:
                    break

                legal_moves.append((new_row, new_col))

                if square is not None:
                    break

        return legal_moves
