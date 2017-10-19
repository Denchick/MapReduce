from . import piece


class Extremum:
    def __init__(self, data, piece_obj):
        if not isinstance(piece_obj, piece.Piece) and piece_obj is not None:
            raise TypeError("piece_obj must be of instance of piece.Piece")
        self.data = data
        self.piece_obj = piece_obj
