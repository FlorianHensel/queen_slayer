import chess
from preprocessing.preprocessing import Preprocessing
import tensorflow as tf

class EngineHandler():
    '''
    Handles the engines' moves.
    '''

    def __init__(self, model):
        self.model = model


    def predict_move(self, board=chess.Board, depth=1):
        '''
        Predicts best move.
        '''

        # GET LEGAL MOVES (AS UCI)
        legal_moves = [str(i) for i in list(board.legal_moves)]

        # PREDICT EVALS FOR EACH LEGAL MOVE
        evaluated_moves = {}
        for move in legal_moves:

            # CREATE COPY OF BOARD AND PUSH MOVE
            board.push_uci(move)

            # CREATE AND ENCODE FEN
            fen_encoded = Preprocessing.encode_fen(board=board, encoding='square_list')
            eval = self.model.predict(fen_encoded)

            # STORE MOVE AND EVAL
            evaluated_moves[move] = eval

        # DETERMINE BEST MOVE
        ranked_moves = {move: eval for move, eval in sorted(evaluated_moves.items(),
                                                            key=lambda item: item[1])}

        # RETURN BEST MOVE
        return ranked_moves[0]


# LOAD MODEL
with open('model/model2.json', 'r') as file:
    model_json = file.read()

model = tf.keras.models.model_from_json(model_json)
model.load_weights('model/model2.h5')
engine_handler = EngineHandler(model)
board = chess.Board()
best_move = engine_handler.predict_move(board=board)
