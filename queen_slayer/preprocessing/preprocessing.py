import chess

class Preprocessing():
    '''
    Takes care of encodig FENs.
    '''

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
