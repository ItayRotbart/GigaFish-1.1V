from ..constants import BOARD_SIZE
from ..enums import Color


class Piece:
    def __init__(self, color: Color.WHITE.value | Color.BLACK.value) -> None:
        self.color = color

    def generate_legal_moves(
        self, current_row: int, current_col: int, board, directions=None, sliding=False
    ) -> list[tuple[int, int]]:
        legal_moves = []

        if not directions:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not implement generate_legal_moves"
            )
        if not sliding:
            for dir_row, dir_col in directions:
                target_row = current_row + dir_row
                target_col = current_col + dir_col
                square_state = board.get_square(target_row, target_col)
                if not square_state.in_bounds:
                    continue
                if square_state.is_occupied and square_state.piece.color == self.color:
                    continue
                legal_moves.append((target_row, target_col))
            return legal_moves

        for row_dir, col_dir in directions:
            for step in range(1, BOARD_SIZE):
                target_row = current_row + (row_dir * step)
                target_col = current_col + (col_dir * step)
                square_state = board.get_square(target_row, target_col)

                if not square_state.in_bounds:
                    break
                if square_state.is_occupied and square_state.piece.color == self.color:
                    break

                legal_moves.append((target_row, target_col))

                if square_state.is_occupied:
                    break

        return legal_moves
