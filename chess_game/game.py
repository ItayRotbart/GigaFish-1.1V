from chess_game.enums import Color
from chess_game.constants import FILES, RANKS
from chess_game.board import Board


def turn(board: Board, color: Color.value):
    def get_valid_coordinate(prompt: str) -> tuple[int, int]:
        while True:
            coord = input(prompt)
            if is_valid_cords(coord):
                return translate_to_num_units(coord)
            print("Invalid input. Please enter a valid coordinate like e2 or e4.")

    def get_user_move() -> tuple[tuple[int, int], tuple[int, int]]:
        start_pos = get_valid_coordinate("Enter the position of the piece you want to move (e.g., e2): ")
        handle_invalid_start(start_pos)
        target_pos = get_valid_coordinate("Enter the position of the square you want to move the piece to (e.g., e4): ")
        handle_invalid_move(start_pos, target_pos)
        return start_pos, target_pos

    def is_valid_cords(coord: str) -> bool:
        return coord[0] in FILES and coord[1] in RANKS and len(coord) == 2

    def translate_to_num_units(coord: str) -> tuple[int, int]:
        file = FILES.index(coord[0])
        rank = RANKS.index(coord[1])
        return file, rank

    def is_valid_move(position: tuple[int, int], move: tuple[int, int]) -> bool:
        piece = board.get_piece(position[0], position[1])
        if move in piece.generate_legal_moves(position[0], position[1], board):
            return True
        return False

    def is_valid_start(position: tuple[int, int]) -> bool:
        square = board.get_piece(position[0], position[1])
        if square is None or square.color == color:
            return False
        return True

    def handle_invalid_start(position: tuple[int, int]) -> None:
        while True:
            if is_valid_start(position):
                break
            print("Not your piece or no piece there.")
            get_user_move()

    def handle_invalid_move(position: tuple[int, int], move: tuple[int, int]) -> None:
        while True:
            if is_valid_move(position, move):
                break
            print("Illegal move. Please try again.")
            get_user_move()

    def make_move(start: tuple[int, int], move: tuple[int, int]) -> None:
        piece = board.get_piece(start[0], start[1])
        board.set_piece(move[0], move[1], piece)

    make_move(get_user_move()[0], get_user_move()[1])
    board.print_board()


def main() -> None:
    board = Board()
    color = Color.WHITE.value
    while True:
        turn(board, color)
        color = not color


if __name__ == "__main__":
    main()
