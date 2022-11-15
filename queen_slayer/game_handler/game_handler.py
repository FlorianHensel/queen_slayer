import chess
from engine_handler.engine_handler import EngineHandler

engine_handler = EngineHandler('model/model2.json', 'model/model2.h5')
board = chess.Board()

print("\n\n########## GAME START ##########\n")
print(board)

while __name__ == '__main__':

    print("\n########## USER TURN ##########\n")
    user_move = input("Please input a move: ")
    print('\n')
    board.push_uci(user_move)
    print(board)

    print("\n########## AI TURN ##########\n")
    best_move, eval = engine_handler.predict_move(board=board)
    board.push_uci(best_move)
    print(f'Best move: {best_move} | Eval: {eval}')
    print(board)

## DOES ENGINE PREDICT WRONG BEST MOVE??? WHITE INSTEAD BLACK?
