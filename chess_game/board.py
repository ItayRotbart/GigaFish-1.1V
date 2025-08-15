import colorama
from colorama import Fore, Style

from .constants import BOARD_SIZE, EMPTY_SPOT, EMPTY_RANKS, BOARD_MIN_SIZE
from .enums import Color
from .pieces import Rook, Knight, Bishop, Queen, King, Pawn, Piece

BACK_RANK_PIECES = [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]


class Board:
    def __init__(self):
        self.grid: list[list[Piece | None]] = self._init_board()

    def get_piece(self, row: int, col: int) -> Piece | None:
        if not self._is_valid_position(row, col):
            return None
        return self.grid[row][col]

    def set_piece(self, row: int, col: int, piece: Piece | None) -> bool:
        if not self._is_valid_position(row, col):
            return False
        self.grid[row][col] = piece
        return True

    def move_piece(
            self, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> bool:
        if not self._is_valid_position(
                from_row, from_col
        ) or not self._is_valid_position(to_row, to_col):
            return False

        piece = self.grid[from_row][from_col]
        if piece is None:
            return False

        if (to_row, to_col) not in piece.generate_legal_moves(from_row, from_col, self):
            return False

        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
        return True

    @staticmethod
    def _is_valid_position(row: int, col: int) -> bool:
        return BOARD_MIN_SIZE <= row < BOARD_SIZE and BOARD_MIN_SIZE <= col < BOARD_SIZE

    def print_board(self) -> None:
        for row in reversed(self.grid):
            for piece in row:
                if piece:
                    color_code = (
                        Fore.LIGHTWHITE_EX if piece.color else Fore.LIGHTBLACK_EX
                    )
                    print(color_code + str(piece) + Style.RESET_ALL, end=" ")
                else:
                    print(EMPTY_SPOT, end=" ")
            print()

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
