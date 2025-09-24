from ..constants import (
    WHITE_DIRECTION,
    BLACK_DIRECTION,
    EAST_OFFSET,
    WEST_OFFSET,
    WHITE_PAWN_RANK,
    BLACK_PAWN_RANK,
    DOUBLE,
)
from .piece import Piece


class Pawn(Piece):
    def __str__(self):
        return "♙"

    def generate_legal_moves(
        self, current_row: int, current_col: int, board, directions=None, sliding=False
    ) -> list[tuple[int, int]]:
        legal_moves = []
        direction = WHITE_DIRECTION if self.color else BLACK_DIRECTION
        next_row = current_row + direction

        next_square = board.get_square(next_row, current_col)
        if next_square.in_bounds and next_square.is_empty:
            legal_moves.append((next_row, current_col))
            self._try_double_move(
                legal_moves, current_row, current_col, direction, board
            )

        self._add_captures(legal_moves, current_row, current_col, board, direction)
        return legal_moves

    def _add_captures(
        self, legal_moves: list, current_row: int, current_col: int, board, direction
    ):
        next_row = current_row + direction

        for col_offset in [WEST_OFFSET, EAST_OFFSET]:
            capture_col = current_col + col_offset

            target_state = board.get_square(next_row, capture_col)
            if (
                target_state.in_bounds
                and target_state.is_occupied
                and target_state.piece.color != self.color
            ):
                legal_moves.append((next_row, capture_col))

    def _try_double_move(self, legal_moves, current_row, current_col, direction, board):
        starting_rank_ok = (self.color and current_row == WHITE_PAWN_RANK) or (
            not self.color and current_row == BLACK_PAWN_RANK
        )
        if not starting_rank_ok:
            return
        first_step_state = board.get_square(current_row + direction, current_col)
        second_step_state = board.get_square(
            current_row + (direction * DOUBLE), current_col
        )
        if (not first_step_state.in_bounds or not first_step_state.is_empty) or (
            not second_step_state.in_bounds or not second_step_state.is_empty
        ):
            return

        legal_moves.append((current_row + direction * DOUBLE, current_col))
