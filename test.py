from game.board import create_board, apply_move, PLAYER_AI
from game.rules import check_winner, is_draw
from game.utils import print_board, get_valid_moves
from ai.random_ai import get_move

# game mechanics test ----->

# board = create_board()
# print_board(board)

# winner = 0

# while (winner == 0 and not is_draw(board)):
#     move = int(input("Enter your move: ")) - 1
#     apply_move(board, move, 1)
#     print_board(board)
#     moveAI = int(input("Enter your move AI: ")) - 1
#     apply_move(board, moveAI, -1)
#     print_board(board)
#     winner = check_winner(board)

# print("Valid moves:", get_valid_moves(board))
# print("Winner:", check_winner(board))
# print("Draw?", is_draw(board))


# random_ai.py test ----->

# board = create_board()
# print_board(board)

# col = get_move(board)
# apply_move(board, col, PLAYER_AI)

# col = get_move(board)
# apply_move(board, col, PLAYER_AI)

# print("AI played column:", col)
# print_board(board)


# minimax_ai.py test ----->

# from game.board import create_board, apply_move, PLAYER_AI, PLAYER_HUMAN
# from ai.minimax_ai import get_move
# from game.utils import print_board

# board = create_board()
# apply_move(board, 3, PLAYER_HUMAN)
# apply_move(board, 2, PLAYER_AI)
# apply_move(board, 3, PLAYER_HUMAN)

# print_board(board)

# col = get_move(board)
# apply_move(board, col, PLAYER_AI)

# print("Minimax AI played:", col)
# print_board(board)