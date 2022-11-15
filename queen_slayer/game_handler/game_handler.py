import chess
from engine_handler.engine_handler import EngineHandler

engine_handler = EngineHandler('model/model3.json', 'model/model3.h5')
board = chess.Board()

print("\n\n########## GAME START ##########\n")
print(board)

def user_turn():
    print("\n########## USER TURN ##########\n")
    user_move = input("Please input a move: ")
    print('\n')
    board.push_uci(user_move)
    print(board)


def ai_turn():
    print("\n########## AI TURN ##########\n")
    best_move, eval = engine_handler.predict_move(board=board)
    board.push_uci(best_move)
    print(f'Best move: {best_move} | Eval: {round(float(eval), 2)}\n')
    print(board)


while __name__ == '__main__':

    user_turn()
    if board.is_checkmate() == True:
        break

    ai_turn()
    if board.is_checkmate() == True:
        break
