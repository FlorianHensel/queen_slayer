from eval_extractor import EvalExtractor
from pgn_to_fen import PGNConverter
from fen_eval_matcher import DatasetCreator

GAMES_TO_READ = None
filepath = 'evals.pgn'

# CREATE FENS FROM GAMES
converter = PGNConverter()
converter.read_pgn(filepath,
                   encoding='square_list',
                   games_to_read=GAMES_TO_READ,
                   qcm_to_flag=3)

# GET EVALUATIONS
eval_extractor = EvalExtractor()
eval_extractor.read_pgn(filepath, games_to_read=GAMES_TO_READ)

# MATCH EVALS TO FENS
dataset_creator = DatasetCreator(fens=converter.games, evals=eval_extractor.evals)
dataset_creator.match_fen_to_eval()

# CREATE DATASET
dataset_creator.create_dataset(dropna=False, drop_duplicates=False)

# EMPOWER QUEEN CAPTURE POSITIONS
amplifiers = {
    'main': 10,
    '-1': 5,
    '-2': 3,
    '-3': 1.5
}
df = dataset_creator.amplify_queen_capture_positions(amplifiers=amplifiers,
                                                     amplifier_type='addition',
                                                     keep_qcm=False)
df.to_csv('train_data.csv', index=False)
