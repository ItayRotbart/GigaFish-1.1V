from colorama import Fore, Style
from dataclasses import dataclass
from typing import Optional

from .constants import BOARD_SIZE, EMPTY_SPOT, EMPTY_RANKS, BOARD_MIN_SIZE, FILES, RANKS
from .enums import Color
from .pieces import Rook, Knight, Bishop, Queen, King, Pawn, Piece

BACK_RANK_PIECES = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]


@dataclass(frozen=True)
class SquareState:
    in_bounds: bool
    piece: Optional[Piece]

    @property
    def is_empty(self) -> bool:
        return self.in_bounds and self.piece is None

    @property
    def is_occupied(self) -> bool:
        return self.in_bounds and self.piece is not None


class Board:
    def __init__(self):
        self.grid: list[list[Piece | None]] = self._init_board()

    def get_square(self, row: int, col: int) -> SquareState:
        in_bounds = self._is_in_bounds(row, col)
        if not in_bounds:
            return SquareState(False, None)
        return SquareState(True, self.grid[row][col])

    def get_square_val(self, row: int, col: int) -> Piece | bool:
        square_state = self.get_square(row, col)
        if not square_state.in_bounds:
            return False
        return square_state.piece

    def set_square_val(self, row: int, col: int, piece: Piece | None) -> None:
        self.grid[row][col] = piece

    def move_piece(
        self, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> None:

        piece = self.get_square_val(from_row, from_col)

        self.set_square_val(from_row, from_col, None)
        self.set_square_val(to_row, to_col, piece)

    def is_legal_move(self, position: tuple[int, int], move: tuple[int, int]) -> bool:
        source_state = self.get_square(position[0], position[1])
        if not source_state.in_bounds or source_state.piece is None:
            return False
        piece = source_state.piece
        legal_moves = piece.generate_legal_moves(position[0], position[1], self)
        return move in legal_moves

    @staticmethod
    def _is_in_bounds(row: int, col: int) -> bool:
        return BOARD_MIN_SIZE <= row < BOARD_SIZE and BOARD_MIN_SIZE <= col < BOARD_SIZE

    def print_board(self) -> None:
        i = 0
        for row in reversed(self.grid):
            for piece in row:
                if piece:
                    color_code = (
                        Fore.LIGHTWHITE_EX if piece.color else Fore.LIGHTBLACK_EX
                    )
                    print(color_code + str(piece) + Style.RESET_ALL, end=" ")
                else:
                    print(EMPTY_SPOT, end=" ")
            i += 1
            print(RANKS[len(RANKS) - i])
        for file in FILES:
            print(file, end=" ")

    def __str__(self) -> str:
        lines = [
            " ".join(str(piece) if piece else EMPTY_SPOT for piece in row)
            for row in self.grid
        ]
        return "\n".join(lines)

    @staticmethod
    def _init_board() -> list[list[Piece | None]]:
        board = [
            [piece_class(Color.WHITE.value) for piece_class in BACK_RANK_PIECES],
            [Pawn(Color.WHITE.value) for _ in range(BOARD_SIZE)],
            *[[None for _ in range(BOARD_SIZE)] for _ in range(EMPTY_RANKS)],
            [Pawn(Color.BLACK.value) for _ in range(BOARD_SIZE)],
            [piece_class(Color.BLACK.value) for piece_class in BACK_RANK_PIECES],
        ]
        return board
