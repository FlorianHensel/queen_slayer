import chess.pgn
import regex as re

class Preprocessing():
    '''
    Takes care of encodig FENs.
    '''

    def encode_fen(board, encoding, move_counter):
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
            fen_string = board.fen()

            # ENCODE EMPTY FIELDS
            board_str = board_str.replace('.', '0')
            # ENCODE ROOKS
            board_str = board_str.replace('r', '-5')
            board_str = board_str.replace('R', '5')
            # ENCODE PAWNS
            board_str = board_str.replace('p', '-1')
            board_str = board_str.replace('P', '1')
            # ENCODE KNIGHTS
            board_str = board_str.replace('n', '-3')
            board_str = board_str.replace('N', '3')
            # ENCODE BISHOPS
            board_str = board_str.replace('b', '-4')
            board_str = board_str.replace('B', '4')
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

            # CHECKING WHICH SIDE NEEDS TO PLAY
            if board.turn == True:
                side_to_play = 1
            else:
                side_to_play = -1

            fen.insert(0, side_to_play)

            # ADD MOVE COUNTER
            fen.insert(0, move_counter)

            # ADD POINT TRACKER
            fen_points = re.findall('(.*)(b|w)', fen_string)[0][0]

            # WHITE POINTS
            w_pawn = fen_points.count('P')
            w_rook = fen_points.count('R') * 5
            w_bishop = fen_points.count('B') * 3
            w_knight = fen_points.count('N') * 3
            w_queen = fen_points.count('Q') * 9
            w_points = w_pawn + w_rook + w_bishop + w_knight + w_queen

            # BLACK POINTS
            b_pawn = fen_points.count('p')
            b_rook = fen_points.count('r') * 5
            b_bishop = fen_points.count('b') * 3
            b_knight = fen_points.count('n') * 3
            b_queen = fen_points.count('q') * 9
            b_points = b_pawn + b_rook + b_bishop + b_knight + b_queen

            # CALCULATE POINT TRACKER
            if side_to_play == 1:
                point_tracker = w_points - b_points
            else:
                point_tracker = b_points - w_points

            fen.insert(0, point_tracker)

        return fen
