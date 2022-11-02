import chess.pgn

class PGNConverter():
    '''
    Converter that takes .pgn and converts it into FEN.
    '''
    def __init__(self) -> None:
        self.games = {}


    def read_pgn(self, filename=str, games_to_read=None, encoding=str):
        '''
        Reads pgn file and creates FENs for each position in a game.\n
        Stored in self.games
        Each run will reset prior games.
        Encodings: string, binary, square_list
        '''

        print("-------------------\nPGN CONVERTER\n-------------------\nClearing previous games.\nReading PGN...")
        self.games = {}

        def convert_game_to_fens(pgn, game_number, encoding=encoding):
            game = chess.pgn.read_game(pgn)
            try:
                board = game.board()

            # RETURN FALSE IF NO GAME AVAILABLE
            except AttributeError:
                return False

            # PLAY THROUGH EACH GAME AND SAVE MOVES AS FEN
            current_game = f'game_{str(game_number)}'
            self.games[current_game] = []

            for move in game.mainline_moves():
                board.push(move)

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

                self.games[current_game].append(fen)

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


            # IF VALUE IS GIVEN FOR GAMES TO READ, READ N GAMES
            else:
                for game_number in range (1, games_to_read + 1):
                    convert_game_to_fens(pgn, game_number)

        print(f"Added {len(self.games)} games.\n")
