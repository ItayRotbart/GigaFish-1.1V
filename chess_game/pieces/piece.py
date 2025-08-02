from chess_game.constants import BOARD_SIZE


class Piece:
    def __init__(self, color: bool) -> None:
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
            for direction in directions:
                target_row = current_row + direction[0]
                target_col = current_col + direction[1]
                target_square = board.get_piece(target_row, target_col)
                if target_square is False:
                    continue
                if target_square and target_square.color == self.color:
                    continue
                legal_moves.append((target_row, target_col))
            return legal_moves

        for row_dir, col_dir in directions:
            for step in range(1, BOARD_SIZE):
                target_row = current_row + (row_dir * step)
                target_col = current_col + (col_dir * step)
                square = board.get_piece(target_row, target_col)

                if square is False:
                    break
                if square is not None and square.color == self.color:
                    break

                legal_moves.append((target_row, target_col))

                if square is not None:
                    break

        return legal_moves
