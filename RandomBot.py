import random
from ChessBoard import ChessBoard

class RandomBot:
    def __init__(self, chessboard: ChessBoard, side: str):
        self.chessboard = chessboard
        self.side = side

    def make_random_move(self):
        pieces_positions = self.chessboard.get_pieces_positions(self.side) 
        random_piece = random.choice(pieces_positions)
        possible_moves = self.chessboard.get_possible_moves_with_coords(random_piece)
        if not possible_moves:
            raise Exception("没有可行的移动。")
        random_move = random.choice(possible_moves)
        success = self.chessboard.move_piece_with_coords(random_piece, random_move)
        if not success:
            raise Exception("移动失败。")