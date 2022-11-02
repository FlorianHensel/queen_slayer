import regex as re

class EvalExtractor():
    '''
    Takes .pgn and extracts eval%.
    '''

    def read_pgn(self, filename=str, games_to_read=None):
        '''
        Reads pgn file and creates EVAL% for each position in a game.\n
        Stored in self.games
        Each run will reset prior games.
        '''

        print("-------------------\nEVAL EXTRACTOR\n-------------------\nClearing previous games.\nReading PGN...")
        self.evals = {}

        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

            # ISOLATE ALL GAMES
            games = re.findall("(\n1. .*\n(\d.*\n){1,200})", content)

            # CREATE LIST OF EVALS FOR EACH GAME
            game_counter = 1
            for game in games:

                # ISOLATE EVALS
                search_result = re.findall("(\W\w{4} (|-)\d{1,2}.\d{1,2})", game[0])

                # CONVERT EVALS TO FLOAT
                evals = [float(re.findall("((-|)\d{1,2}.\d{1,2})", i[0])[0][0]) for i in search_result if 'eval' in i[0]]

                # ADD EVALS
                self.evals[f'game_{game_counter}'] = evals
                game_counter += 1

        print(f"Added {len(self.evals)} games.\n")
