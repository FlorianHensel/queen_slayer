import regex as re

class EvalExtractor():
    '''
    Takes .pgn and extracts eval%.
    '''

    def read_pgn(self, filename=str, games_to_read=None):
        '''
        Reads pgn file and creates EVAL% for each position in a game.\n
        Stored in self.games\n
        Each run will reset prior games.
        '''

        print("-------------------\nEVAL EXTRACTOR\n-------------------\nClearing previous games.\nReading PGN...")
        self.evals = {}

        def find_evals(games):
            '''
            Take as input list of PGN games.
            '''
            # CREATE LIST OF EVALS FOR EACH GAME
            game_counter = 1
            for game in games:

                # ISOLATE EVAL STRINGS
                evals_string = [i[0] for i in re.findall("(%\w{4} (|#-|-|#)\d{1,2}.(\d{1,2}|))", game)]

                # ISOLATE EVAL (INCLUDING HASH NOTATION FOR FORCED CHECKMATE)
                evals_hash = [re.findall("((#|#-|-|)\d{1,2}(.\d{1,2}|))", i)[0][0]
                              for i in evals_string if 'eval' in i]

                # ADJUST EVALS FOR CHECKMATE POSITIONS:
                evals = []
                for eval in evals_hash:
                    # CHECKMATE POSSIBILITY FOR BLACK
                    if '#-' in eval:
                        evals.append(-15)
                    # CHECKMATE POSSIBILITY FOR WHITE
                    elif '#' in eval:
                        evals.append(15)
                    else:
                        evals.append(float(eval))

                # ADD EVALS TO SELF
                self.evals[f'game_{game_counter}'] = evals
                game_counter += 1

        # OPEN PGN AND READ CONTENTS
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            # ISOLATE ALL GAMES
            games = re.findall("(\d{1,2}. .*)", content)

        # EXTRACT EVALS
        if games_to_read == None:
            find_evals(games)
        else:
            find_evals(games[:games_to_read])

        print(f"Added {len(self.evals)} games.\n")
