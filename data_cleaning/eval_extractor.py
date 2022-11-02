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
            # games = re.findall("(\n\d{1,2}. .*}){1,2000}", content)
            # print(games)
            search_result = re.findall("(\W\w{4} (|-)\d{1,2}.\d{1,2})", content)
            evals = [float(re.findall("((-|)\d{1,2}.\d{1,2})", i[0])[0][0]) for i in search_result if 'eval' in i[0]]
            self.evals = evals

        print(f"Done.\n")
