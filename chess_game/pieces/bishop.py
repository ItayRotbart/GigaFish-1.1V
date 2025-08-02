from .piece import Piece
from chess_game.constants import BISHOP_DIRECTIONS, BOARD_SIZE


class Bishop(Piece):
    def __str__(self):
        return "♝"

    def generate_legal_moves(
        self, current_row: int, current_col: int, board, *args, **kwargs
    ) -> list[tuple[int, int]]:
        legal_moves = []

        for direction in BISHOP_DIRECTIONS:
            for step in range(1, BOARD_SIZE):
                target_row = current_row + (direction[0] * step)
                target_col = current_col + (direction[1] * step)
                square = board.get_piece(target_row, target_col)

                if square is False:
                    break
                if square is not None and square.color == self.color:
                    break

                legal_moves.append((target_row, target_col))

                if square is not None:
                    break

        return legal_moves
