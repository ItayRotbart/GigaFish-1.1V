from .enums import Color
from .constants import FILES, RANKS
from .board import Board
from .advanced_logic import AdvancedChessLogic


def turn(board: Board, color: Color.WHITE.value | Color.BLACK.value):
    advanced_logic = AdvancedChessLogic(board)
    
    def get_valid_coordinate(prompt: str) -> tuple[int, int] | None:
        while True:
            coord = input(prompt)
            valid_chords = is_valid_cords(coord)
            if valid_chords == "cancel":
                return None
            if valid_chords:
                return translate_to_num_units(coord)
            print("Invalid input. Please enter a valid coordinate like e2 or e4.")

    def get_user_move() -> tuple[tuple[int, int], tuple[int, int]] | None:
        while True:
            piece_start_pos = get_valid_coordinate("Enter the position of the piece you want to move (e.g., e2): ")

            if not is_valid_start(piece_start_pos):
                print("Not your piece or no piece there.")
                continue
                
            # Show legal moves for the selected piece
            legal_moves = board.get_legal_moves(piece_start_pos[0], piece_start_pos[1])
            if not legal_moves:
                print("This piece has no legal moves.")
                continue
                
            print(f"Legal moves for {board.get_piece(piece_start_pos[0], piece_start_pos[1])}: {legal_moves}")
            
            piece_target_pos = get_valid_coordinate(
                "Enter the position of the square you want to move the piece to (e.g., e4): ")

            if piece_target_pos is None:
                continue

            if is_valid_move(piece_start_pos, piece_target_pos):
                return piece_start_pos, piece_target_pos

            else:
                print("Illegal move. Please try again.")

    def is_valid_cords(coord: str) -> bool | str:
        if coord == "cancel":
            return "cancel"
        if coord is None:
            return False
        if len(coord) != 2:
            return False
        return coord[0] in FILES and coord[1] in RANKS

    def translate_to_num_units(coord: str) -> tuple[int, int]:
        file = FILES.index(coord[0])
        rank = RANKS.index(coord[1])
        return rank, file

    def is_valid_move(position: tuple[int, int], move: tuple[int, int]) -> bool:
        piece = board.get_piece(position[0], position[1])
        if piece is None:
            return False
        legal_moves = board.get_legal_moves(position[0], position[1])
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

    def check_game_state() -> None:
        """Check and display the current game state"""
        opponent_color = not color
        
        # Check for check
        if board.is_king_in_check(opponent_color):
            print(f"{'Black' if opponent_color else 'White'} is in CHECK!")
            
            # Check for checkmate
            if board.is_checkmate(opponent_color):
                print(f"{'Black' if opponent_color else 'White'} is in CHECKMATE!")
                print(f"{'White' if color else 'Black'} wins!")
                return True
        else:
            # Check for stalemate
            if board.is_stalemate(opponent_color):
                print("STALEMATE! The game is a draw.")
                return True
        
        # Show tactical opportunities
        tactical_moves = advanced_logic.get_tactical_moves(color)
        if tactical_moves:
            print("Tactical opportunities:")
            for from_pos, from_col, to_row, to_col, move_type in tactical_moves:
                piece = board.get_piece(from_pos, from_col)
                print(f"  {piece} at {FILES[from_col]}{RANKS[from_pos]} -> {FILES[to_col]}{RANKS[to_row]} ({move_type})")
        
        return False

    print(f"\n{'White' if color else 'Black'}'s turn")

    # Get the move once and store it
    start_pos, target_pos = get_user_move()
    make_move(start_pos, target_pos)

    # Print updated board after move
    print("\nBoard after move:")
    board.print_board()
    
    # Check game state
    game_over = check_game_state()
    return game_over


def main() -> None:
    board = Board()
    board.print_board()
    color = Color.WHITE.value
    
    print("\nChess Game Started!")
    print("White moves first.")
    
    while True:
        game_over = turn(board, color)
        if game_over:
            break
        color = not color


if __name__ == "__main__":
    main()
