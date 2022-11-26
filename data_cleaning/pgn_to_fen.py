import chess.pgn
import datetime as dt
import regex as re

class PGNConverter():
    '''
    Converter that takes .pgn and converts it into FEN.
    '''
    def __init__(self) -> None:
        self.games = {}


    def read_pgn(self, filename=str,
                 games_to_read=None,
                 encoding=str,
                 qcm_to_flag=1,
                 log=True):
        '''
        Reads pgn file and creates FENs for each position in a game.\n
        Stored in self.games
        Each run will reset prior games.\n
        Encodings: string, binary, square_list.\n
        qcm_to_flag: Number of positions previous to queen capture position
        that need to be flagged.
        '''

        print("-------------------\nPGN CONVERTER\n-------------------\nClearing previous games.")
        self.games = {}


        def is_queen_capture_move(fens):
            '''
            Function to identify a queen capture move.
            Takes as input a list of two FENs.
            Returns True and False.
            '''

            queen_capture_move = False

            # CHECK IF BLACK QUEEN EXISTS IN PRIOR POSITION
            if 'q' in fens[0]:
                # CHECK IF BLACK QUEEN EXISTS AFTER MOVE
                if 'q' not in fens[1]:
                    queen_capture_move = True

            # CHECK IF WIHTE QUEEN EXISTS IN PRIOR POSITION
            if 'Q' in fens[0]:
                # CHECK IF WHITE QUEEN EXISTS AFTER MOVE
                if 'Q' not in fens[1]:
                    queen_capture_move = True

            return queen_capture_move


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
                # ENCODE PAWNS
                board_str = board_str.replace('p', '-1')
                board_str = board_str.replace('P', '1')
                # ENCODE KNIGHTS
                board_str = board_str.replace('n', '-2')
                board_str = board_str.replace('N', '2')
                # ENCODE BISHOPS
                board_str = board_str.replace('b', '-3')
                board_str = board_str.replace('B', '3')
                # ENCODE ROOKS
                board_str = board_str.replace('r', '-4')
                board_str = board_str.replace('R', '4')
                # ENCODE QUEENS
                board_str = board_str.replace('q', '-5')
                board_str = board_str.replace('Q', '5')
                # ENCODE KINGS
                board_str = board_str.replace('k', '-6')
                board_str = board_str.replace('K', '6')
                # REMOVE LINEBREAKS
                board_str = board_str.replace('\n', ' ')

                board_list = board_str.split(' ')
                fen = [float(i) for i in board_list]

            return fen


        def convert_game_to_fens(pgn, game_number, encoding=encoding):
            '''
            Converts games in PGN file into FENs.
            '''
            game = chess.pgn.read_game(pgn)
            try:
                board = game.board()

            # RETURN FALSE IF NO GAME AVAILABLE
            except AttributeError:
                return False

            # PLAY THROUGH EACH GAME AND SAVE MOVES AS FEN
            current_game = f'game_{str(game_number)}'
            fens = []
            fen_counter = 0
            move_counter = 1
            for move in game.mainline_moves():

                # DETERMINE QUEEN CAPTURE MOVE & MAKE MOVE
                fen_before = board.fen()
                board.push(move)
                fen_after = board.fen()
                queen_capture_move = is_queen_capture_move([fen_before, fen_after])

                # DETERMINE SIDE TO PLAY
                if board.turn == True:
                    side_to_play = 1
                else:
                    side_to_play = -1

                # ENCODE FEN AND ADD SIDE TO PLAY
                fen = encode_fen(board=board, encoding=encoding)
                fen.insert(0, side_to_play)

                # ADD MOVE COUNTER
                fen.insert(0, move_counter)
                move_counter += 1

                # ADD POINT TRACKER
                fen_points = re.findall('(.*)(b|w)', fen_after)[0][0]

                # WHITE POINTS
                w_pawn = fen_points.count('P')
                w_rook = fen_points.count('R') * 4
                w_bishop = fen_points.count('B') * 3
                w_knight = fen_points.count('N') * 2
                w_queen = fen_points.count('Q') * 5
                w_points = w_pawn + w_rook + w_bishop + w_knight + w_queen

                # BLACK POINTS
                b_pawn = fen_points.count('p')
                b_rook = fen_points.count('r') * 4
                b_bishop = fen_points.count('b') * 3
                b_knight = fen_points.count('n') * 2
                b_queen = fen_points.count('q') * 5
                b_points = b_pawn + b_rook + b_bishop + b_knight + b_queen

                # CALCULATE POINT TRACKER
                if side_to_play == 1:
                    point_tracker = w_points - b_points
                else:
                    point_tracker = b_points - w_points

                fen.insert(0, point_tracker)

                ####### APPEND FEN #######
                fens.append(fen)

                # FLAG FEN IF QUEEN CAPTURED
                if fen_counter > 0:
                    fens[fen_counter - 1].insert(0, queen_capture_move)

                # FLAG PREVIOUS FEN WITH QUEEN CAPTURE POSSIBILITY
                if queen_capture_move:
                    # FLAG EVERY SECOND POSITION
                    for i in range(2, qcm_to_flag * 2 + 2, 2):
                        try:
                            fens[fen_counter - i - 1][0] = -i / 2
                        except KeyError:
                            pass

                fen_counter += 1

            # LABEL THE LAST GAME POSITION WITH QUEEN CAPTURE POSSIBILITY
            try:
                fens[-1].insert(0, False)
            except:
                pass
            self.games[current_game] = fens

            # RETURN TRUE IF GAME AVAILABLE
            return True


        with open(filename) as pgn:
            # IF NO VALUE IS GIVEN FOR GAMES TO READ, READ ALL GAMES
            if games_to_read == None:
                if log:
                    print('Reading all games...')
                game_counter = 1
                games_available = True
                while games_available:
                    games_available = convert_game_to_fens(pgn, game_counter)
                    game_counter += 1

                    if log:
                        if game_counter % 1000 == 0:
                            now = dt.datetime.now().strftime("%H:%M:%S")
                            print(f'{now} | processed {game_counter} games...')


            # IF VALUE IS GIVEN FOR GAMES TO READ, READ N GAMES
            else:
                if log:
                    print(f'Reading {games_to_read} games...')
                game_counter = 1

                for game_number in range (1, games_to_read + 1):
                    convert_game_to_fens(pgn, game_number)
                    game_counter += 1

                    # LOG EVERY THOUSAND GAMES
                    if log:
                        if game_counter % 1000 == 0:
                            now = dt.datetime.now().strftime("%H:%M:%S")
                            print(f'{now} | processed {game_counter} games...')

        print(f"Added {len(self.games)} games.\n")
