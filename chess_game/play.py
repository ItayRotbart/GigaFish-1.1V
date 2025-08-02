from chess_game.board import Board
from chess_game.constants import LINE


def main() -> None:
    board = Board()
    board.move_piece(1, 7, 3, 7)
    board.print_board()
    print(LINE)
    piece = board.get_piece(0, 7)
    if piece:
        print(f"Testing {piece.__class__.__name__} at (0,7)")
        print(f"Legal moves: {piece.generate_legal_moves(0, 7, board)}")
    else:
        print("No piece found at (0,7)")


if __name__ == "__main__":
    main()
