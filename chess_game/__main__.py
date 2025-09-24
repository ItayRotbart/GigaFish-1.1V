from .enums import Color
from .constants import FILES, RANKS
from .board import Board


def turn(board: Board, color: Color.WHITE.value | Color.BLACK.value):
    def get_valid_coordinate(prompt: str) -> tuple[int, int]:
        while True:
            coord = input(prompt)
            if is_valid_coords(coord):
                return translate_to_num_units(coord)
            print("Invalid input. Please enter a valid coordinate like e2 or e4.")

    def get_user_move() -> tuple[tuple[int, int], tuple[int, int]] | None:
        while True:
            piece_start_pos = get_valid_coordinate(
                "Enter the position of the piece you want to move (e.g., e2): "
            )

            if not is_valid_start(piece_start_pos):
                print("Not your piece or no piece there.")
                continue
            piece_target_pos = get_valid_coordinate(
                "Enter the position of the square you want to move the piece to (e.g., e4): "
            )

            if board.is_legal_move(piece_start_pos, piece_target_pos):
                return piece_start_pos, piece_target_pos

            else:
                print("Illegal move. Please try again.")

    def is_valid_coords(coord: str) -> bool:
        return len(coord) == 2 and coord[0] in FILES and coord[1] in RANKS

    def translate_to_num_units(coord: str) -> tuple[int, int]:
        file = FILES.index(coord[0])
        rank = RANKS.index(coord[1])
        return rank, file

    def is_valid_start(position: tuple[int, int]) -> bool:
        square = board.get_square_val(position[0], position[1])
        if square is None or square.color != color:
            return False
        return True

    print(f"\n{'White' if color else 'Black'}'s turn")

    # Get the move once and store it
    start_pos, target_pos = get_user_move()
    board.move_piece(start_pos[0], start_pos[1], target_pos[0], target_pos[1])

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
