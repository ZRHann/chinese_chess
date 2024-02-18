from RandomBot import RandomBot
from MCTSBot import MCTSBot
from ChessBoard import ChessBoard
from ChessBoard import ChessPiece
from AlphaBetaBot import AlphaBetaBot
chess_board = ChessBoard()
# chess_board.place_pieces(
#     [
#         ChessPiece("将", "black", "f9"),
#         ChessPiece("帅", "red", "f1"),
#     ]
# )
chess_board.set_initial_pieces()
chess_board.print_board()

# random_bot = RandomBot(chess_board, "red")
# MCTS_bot = MCTSBot(chess_board, "red")
alphabetabot = AlphaBetaBot(chess_board, "red", 3)

while True:
    alphabetabot.make_move()
    chess_board.print_board()
    if chess_board.winner is not None:
        print(f"{chess_board.winner} wins!")
        break
    user_input = input("Enter your move (e.g., 'e2 e4') or 'quit' to exit: ")
    if user_input.lower() == 'quit':
        break
    src, dest = user_input.split()
    chess_board.move_piece(src, dest)
    chess_board.print_board()
    if chess_board.winner is not None:
        print(f"{chess_board.winner} wins!")
        break