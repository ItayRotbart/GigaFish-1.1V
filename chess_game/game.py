from .enums import Color
from .constants import FILES, RANKS
from .board import Board


def turn(board: Board, color: Color.WHITE.value | Color.BLACK.value):
    def get_valid_coordinate(prompt: str) -> tuple[int, int]:
        while True:
            coord = input(prompt)
            valid_chords = is_valid_cords(coord)
            if valid_chords or valid_chords == "cancel":
                return None if valid_chords == "cancel" else translate_to_num_units(coord)
            print("Invalid input. Please enter a valid coordinate like e2 or e4.")

    def get_user_move() -> tuple[tuple[int, int], tuple[int, int]] | None:
        while True:
            piece_start_pos = get_valid_coordinate("Enter the position of the piece you want to move (e.g., e2): ")

            if not is_valid_start(piece_start_pos):
                print("Not your piece or no piece there.")
                continue
            piece_target_pos = get_valid_coordinate(
                "Enter the position of the square you want to move the piece to (e.g., e4): ")

            if piece_target_pos is None:
                continue

            if is_valid_move(piece_start_pos, piece_target_pos):
                return piece_start_pos, piece_target_pos

            else:
                print("Illegal move. Please try again.")

    def is_valid_cords(coord: str) -> bool | str:
        return coord if coord == "cancel" or coord is not None else coord[0] in FILES and coord[1] in RANKS and len(coord) == 2

    def translate_to_num_units(coord: str) -> tuple[int, int]:
        file = FILES.index(coord[0])
        rank = RANKS.index(coord[1])
        return rank, file

    def is_valid_move(position: tuple[int, int], move: tuple[int, int]) -> bool:
        piece = board.get_piece(position[0], position[1])
        if piece is None:
            return False
        legal_moves = piece.generate_legal_moves(position[0], position[1], board)
        return move in legal_moves

    def is_valid_start(position: tuple[int, int]) -> bool:
        square = board.get_piece(position[0], position[1])
        if square is None or square.color != color:
            return False
        return True

    def make_move(start: tuple[int, int], move: tuple[int, int]) -> None:
        piece = board.get_piece(start[0], start[1])
        if piece is not None:
            board.set_piece(start[0], start[1], None)
            board.set_piece(move[0], move[1], piece)

    print(f"\n{'White' if color else 'Black'}'s turn")

    # Get the move once and store it
    start_pos, target_pos = get_user_move()
    make_move(start_pos, target_pos)

    # Print updated board after move
    print("\nBoard after move:")
    board.print_board()


def main() -> None:
    board = Board()
    board.print_board()
    color = Color.WHITE.value
    while True:
        turn(board, color)
        color = not color


if __name__ == "__main__":
    main()
