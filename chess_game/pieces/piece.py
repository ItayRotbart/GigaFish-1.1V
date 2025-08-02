class Piece:
    def __init__(self, color: bool) -> None:
        self.color = color

    def generate_legal_moves(
        self, current_row: int, current_col: int, board, *args, **kwargs
    ) -> list[tuple[int, int]]:
        legal_moves = []

        directions = kwargs.get("directions")
        if not directions:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not implement generate_legal_moves"
            )
        for direction in directions:
            new_row = current_row + direction[0]
            new_col = current_col + direction[1]
            to_square = board.get_piece(new_row, new_col)
            if to_square is False:
                continue
            if to_square and to_square.color == self.color:
                continue
            legal_moves.append((new_row, new_col))
        return legal_moves
