import chess
import regex as re

class EngineHandler():
    '''
    Handles the engines' moves.
    '''

    def __init__(self, model):
        self.model = model
        self.board = chess.Board()


    def encode_fen(board, encoding=str):
        '''
        Returns encoded FEN
        '''
        # FEN AS BINARY
        if encoding == 'binary':
            fen_str = ''.join(format(ord(x), 'b') for x in board.fen())
            fen = [i for i in fen_str]

        # FEN AS STRING
        elif encoding == 'string':
            fen_str = board.fen()
            fen = [i for i in fen_str]

        # FEN AS SQUARE LIST
        elif encoding == 'square_list':
            board_str = str(board)

            # ENCODE EMPTY FIELDS
            board_str = board_str.replace('.', '0')
            # ENCODE ROOKS
            board_str = board_str.replace('r', '-5')
            board_str = board_str.replace('R', '5')
            # ENCODE PAWNS
            board_str = board_str.replace('p', '-1')
            board_str = board_str.replace('P', '1')
            # ENCODE KNIGHTS
            board_str = board_str.replace('n', '-2.9')
            board_str = board_str.replace('N', '2.9')
            # ENCODE BISHOPS
            board_str = board_str.replace('b', '-3')
            board_str = board_str.replace('B', '3')
            # ENCODE QUEENS
            board_str = board_str.replace('q', '-9')
            board_str = board_str.replace('Q', '9')
            # ENCODE KINGS
            board_str = board_str.replace('k', '-1.5')
            board_str = board_str.replace('K', '1.5')
            # REMOVE LINEBREAKS
            board_str = board_str.replace('\n', ' ')

            board_list = board_str.split(' ')
            fen = [float(i) for i in board_list]

        return fen


    def make_move(self, move):
        '''
        Pushes move on self.board.
        '''
        self.board.push(move)


    def predict_move(self, depth=1):
        '''
        Predicts best move.
        '''

        # GET LEGAL MOVES (AS UCI)
        legal_moves = [str(i) for i in list(self.board.legal_moves)]

        # PREDICT EVALS FOR EACH LEGAL MOVE
        evaluated_moves = {}
        for move in legal_moves:

            # CREATE COPY OF BOARD AND PUSH MOVE
            board = self.board
            board.push_uci(move)

            # CREATE AND ENCODE FEN
            fen = board.fen()
            fen_encoded = fen
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
