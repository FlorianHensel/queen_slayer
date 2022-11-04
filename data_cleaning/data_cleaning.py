from eval_extractor import EvalExtractor
from pgn_to_fen import PGNConverter
from fen_eval_matcher import FEN_Eval_Matcher

GAMES_TO_READ = None
filepath = 'evals.pgn'

# GET EVALUATIONS
eval_extractor = EvalExtractor()
eval_extractor.read_pgn(filepath,
                        games_to_read=GAMES_TO_READ)

# CREATE FENS FROM GAMES
converter = PGNConverter()
converter.read_pgn(filepath,
                   encoding='square_list',
                   games_to_read=GAMES_TO_READ)

# MATCH EVALS TO FENS
fen_eval_matcher = FEN_Eval_Matcher(fens=converter.games,
                                    evals=eval_extractor.evals)
fen_eval_matcher.match_fen_to_eval()

# CREATE DATASET
fen_eval_matcher.create_dataset(dropna=True,
                                drop_duplicates=False)
df = fen_eval_matcher.amplify_queen_capture_positions(amplifier=100,
                                                      amplifier_type='addition')
df.to_csv('train_data.csv', index=False)
