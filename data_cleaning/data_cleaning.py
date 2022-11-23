from eval_extractor import EvalExtractor
from pgn_to_fen import PGNConverter
from fen_eval_matcher import DatasetCreator
from os import listdir
from os.path import isfile, join

path = 'data/splitted/'
pgns = [f for f in listdir(path) if isfile(join(path, f))]
GAMES_TO_READ = None

############# VERSION 3.0 #############
pgn_counter = 1
for pgn in pgns:
    filepath = f'{path}{pgn}'

    # CREATE FENS FROM GAMES
    converter = PGNConverter()
    converter.read_pgn(filepath,
                    encoding='square_list',
                    games_to_read=GAMES_TO_READ,
                    qcm_to_flag=3,
                    log=True)

    # GET EVALUATIONS
    eval_extractor = EvalExtractor()
    eval_extractor.read_pgn(filepath, games_to_read=GAMES_TO_READ, log=True)

    # MATCH EVALS TO FENS
    dataset_creator = DatasetCreator()
    dataset_creator.match_fen_to_eval(fens=converter.games, evals=eval_extractor.evals)

    # CREATE DATASET
    dataset_creator.create_dataset(dropna=True, drop_duplicates=True)

    # EMPOWER QUEEN CAPTURE POSITIONS
    amplifiers = {
        'main': 0,
        '-1': 0,
        '-2': 0,
        '-3': 0
    }
    df = dataset_creator.amplify_queen_capture_positions(amplifiers=amplifiers,
                                                        amplifier_type='addition',
                                                        keep_qcm=False,
                                                        evals_cap=[-15, 15])

    # WRITE TRAIN SET TO CSV
    print('Exporting to csv.')
    if pgn_counter == 1:
        df.to_csv('train_data.csv', index=False)
    else:
        df.to_csv('train_data.csv', index=False, mode='a', header=False)

    print(f'\n####### {int(pgn_counter / len(pgns) * 100)}% #######\n')
    pgn_counter += 1
