import chess
from preprocessing.preprocessing import Preprocessing

class EngineHandler():
    '''
    Handles the engines' moves.
    '''

    def __init__(self, model):
        self.model = model


    def make_move(self, move):
        '''
        Pushes move on self.board.
        '''
        self.board.push(move)


    def predict_move(self, board, depth=1):
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

        # PLAY BEST MOVE
        self.make_move(ranked_moves[0])

        # RETURN MOVE TO VISUALIZE ON BOARD
        return ranked_moves[0]
