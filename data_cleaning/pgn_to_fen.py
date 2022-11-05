import chess.pgn
import datetime as dt

class PGNConverter():
    '''
    Converter that takes .pgn and converts it into FEN.
    '''
    def __init__(self) -> None:
        self.games = {}


    def read_pgn(self, filename=str, games_to_read=None, encoding=str, qcm_to_flag=1):
        '''
        Reads pgn file and creates FENs for each position in a game.\n
        Stored in self.games
        Each run will reset prior games.\n
        Encodings: string, binary, square_list.\n
        qcm_to_flag: Number of positions previous to queen capture position
        that need to be flagged.
        '''

        print("-------------------\nPGN CONVERTER\n-------------------\nClearing previous games.\nReading PGN...")
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
            fens[-1].insert(0, False)

            self.games[current_game] = fens

            # RETURN TRUE IF GAME AVAILABLE
            return True


        with open(filename) as pgn:
            # IF NO VALUE IS GIVEN FOR GAMES TO READ, READ ALL GAMES
            if games_to_read == None:
                game_counter = 1
                games_available = True
                while games_available:
                    games_available = convert_game_to_fens(pgn, game_counter)
                    game_counter += 1

                    if game_counter == 1000:
                        now = dt.datetime.now().strftime("%H:%M:%S")
                        print(f'{now}: processed 1000 games...')
                        game_counter = 0


            # IF VALUE IS GIVEN FOR GAMES TO READ, READ N GAMES
            else:
                for game_number in range (1, games_to_read + 1):
                    convert_game_to_fens(pgn, game_number)

        print(f"Added {len(self.games)} games.\n")
