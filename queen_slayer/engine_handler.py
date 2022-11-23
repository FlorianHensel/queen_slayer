import chess
from preprocessing import Preprocessing
import tensorflow as tf

class EngineHandler():
    '''
    Handles the engines' moves.
    '''

    def __init__(self, model_path, weights_path):

        # LOAD MODEL
        with open(model_path, 'r') as file:
            model_json = file.read()
            model = tf.keras.models.model_from_json(model_json)

        # LOAD WEIGHTS
        model.load_weights(weights_path)

        # COMPILE
        model.compile(loss='RMSE', optimizer='adam', metrics=['accuracy'])
        self.model = model


    def predict_move(self, board=chess.Board, move_counter=int):
        '''
        Returns pest move in UCI format.
        '''

        # GET LEGAL MOVES (AS UCI)
        legal_moves = [str(i) for i in list(board.legal_moves)]

        # DETERMINE SIDE TO PLAY
        if board.turn == True:
            side_to_play = 1
        else:
            side_to_play = -1

        # PREDICT EVALS FOR EACH LEGAL MOVE
        evaluated_moves = {}
        for move in legal_moves:

            try:
                # CREATE COPY OF BOARD AND PUSH MOVE
                board.push_uci(move)

                # CREATE AND ENCODE FEN
                fen_encoded = [Preprocessing.encode_fen(board=board,
                                                        encoding='square_list',
                                                        move_counter=move_counter)]
                eval = self.model.predict(fen_encoded, verbose=0)[0][0]

                # STORE MOVE AND EVAL
                evaluated_moves[move] = round(eval, 2)

                # RESTORE INITIAL POSITION
                board.pop()

            except:
                print(f'{move} | not possible')

        # SORT MOVES BASED ON THEIR EVALS
        ranked_moves = {move: eval for move, eval in sorted(evaluated_moves.items(),
                                                            key=lambda item: item[1])}

        # RETURN BEST MOVE IF AI IS WHITE
        if side_to_play == 1:
            best_move = list(ranked_moves.keys())[-1]
            return best_move, ranked_moves[best_move]

        # RETURN BEST MOVE IF AI IS BLACK
        else:
            best_move = list(ranked_moves.keys())[0]
            return best_move, ranked_moves[best_move]
