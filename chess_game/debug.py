from .board import Board
from .constants import LINE


def main() -> None:
    board = Board()
    board.move_piece(1, 4, 3, 4)
    board.move_piece(1, 5, 3, 5)
    board.print_board()
    print(LINE)
    piece = board.get_piece(0, 4)
    if piece:
        print(f"Testing {piece.__class__.__name__} at (0,4)")
        print(f"Legal moves: {piece.generate_legal_moves(0, 4, board)}")
    else:
        print("No piece found at (0,4)")


if __name__ == "__main__":
    main()
