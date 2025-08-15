import colorama
from colorama import Fore, Style

from .constants import BOARD_SIZE, EMPTY_SPOT, EMPTY_RANKS, BOARD_MIN_SIZE
from .enums import Color
from .pieces import Rook, Knight, Bishop, Queen, King, Pawn, Piece

BACK_RANK_PIECES = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]


class Board:
    def __init__(self):
        self.grid: list[list[Piece | None]] = self._init_board()
        # Attack maps: white_attacks[row][col] = True if white attacks this square
        self.white_attacks: list[list[bool]] = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.black_attacks: list[list[bool]] = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self._update_attack_maps()

    def get_piece(self, row: int, col: int) -> Piece | None:
        if not self._is_valid_position(row, col):
            return None
        return self.grid[row][col]

    def set_piece(self, row: int, col: int, piece: Piece | None) -> bool:
        if not self._is_valid_position(row, col):
            return False
        self.grid[row][col] = piece
        self._update_attack_maps()  # Recalculate attack maps when pieces change
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
        self._update_attack_maps()  # Recalculate attack maps after move
        return True

    def _update_attack_maps(self) -> None:
        """Recalculate attack maps for both colors"""
        # Reset attack maps
        self.white_attacks = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.black_attacks = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        
        # Calculate attacks for each piece
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.grid[row][col]
                if piece:
                    self._add_piece_attacks(row, col, piece)

    def _add_piece_attacks(self, row: int, col: int, piece: Piece) -> None:
        """Add all squares this piece attacks to the appropriate attack map"""
        attack_map = self.white_attacks if piece.color else self.black_attacks
        
        # Get all squares this piece can attack (including through other pieces for sliding pieces)
        attack_squares = piece.generate_attack_squares(row, col, self)
        
        for attack_row, attack_col in attack_squares:
            if self._is_valid_position(attack_row, attack_col):
                attack_map[attack_row][attack_col] = True

    def is_square_under_attack(self, row: int, col: int, by_color: bool) -> bool:
        """Check if a square is under attack by the specified color"""
        if not self._is_valid_position(row, col):
            return False
        return self.white_attacks[row][col] if by_color else self.black_attacks[row][col]

    def is_king_in_check(self, color: bool) -> bool:
        """Check if the king of the specified color is in check"""
        # Find the king
        king_row, king_col = self._find_king(color)
        if king_row is None:
            return False
        
        # Check if the king's square is under attack by the opposite color
        return self.is_square_under_attack(king_row, king_col, not color)

    def _find_king(self, color: bool) -> tuple[int | None, int | None]:
        """Find the position of the king of the specified color"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.grid[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return row, col
        return None, None

    def is_checkmate(self, color: bool) -> bool:
        """Check if the specified color is in checkmate"""
        if not self.is_king_in_check(color):
            return False
        
        # Check if any legal move can get out of check
        return not self._has_legal_moves(color)

    def is_stalemate(self, color: bool) -> bool:
        """Check if the specified color is in stalemate"""
        if self.is_king_in_check(color):
            return False
        
        # Check if there are any legal moves
        return not self._has_legal_moves(color)

    def _has_legal_moves(self, color: bool) -> bool:
        """Check if the specified color has any legal moves"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    legal_moves = piece.generate_legal_moves(row, col, self)
                    for move_row, move_col in legal_moves:
                        if self._is_move_legal(row, col, move_row, move_col, color):
                            return True
        return False

    def _is_move_legal(self, from_row: int, from_col: int, to_row: int, to_col: int, color: bool) -> bool:
        """Check if a move is legal (doesn't leave own king in check)"""
        # Temporarily make the move
        original_piece = self.grid[to_row][to_col]
        moving_piece = self.grid[from_row][from_col]
        
        self.grid[to_row][to_col] = moving_piece
        self.grid[from_row][from_col] = None
        
        # Check if this leaves the king in check
        leaves_king_in_check = self.is_king_in_check(color)
        
        # Undo the move
        self.grid[from_row][from_col] = moving_piece
        self.grid[to_row][to_col] = original_piece
        
        return not leaves_king_in_check

    def get_legal_moves(self, row: int, col: int) -> list[tuple[int, int]]:
        """Get legal moves for a piece, filtering out moves that would leave king in check"""
        piece = self.grid[row][col]
        if not piece:
            return []
        
        all_moves = piece.generate_legal_moves(row, col, self)
        legal_moves = []
        
        for move_row, move_col in all_moves:
            if self._is_move_legal(row, col, move_row, move_col, piece.color):
                legal_moves.append((move_row, move_col))
        
        return legal_moves

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
