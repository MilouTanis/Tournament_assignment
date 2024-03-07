'''
Module that creates a commandline argument for input, output and overwrite. 
Input data is loaded and checked for the following two assumptions:
Assumption 1: The countries.csv, poule_phase_games.csv and final_phase_games.csv 
must be present in the input directory.
Assumption 2: The countries.csv, poule_phase_games.csv and final_phase_games.csv 
must be readable and must contain the right columns;
'''

from pathlib import Path
import argparse
import os
import pandas as pd

def load_data():
    '''
    Reading the data and check assumption 1 and 2
    '''
    # Input directory (--input): specifies the directory where the input files are input.
    parser = argparse.ArgumentParser()

    # Create input argument
    parser.add_argument("--input", required=True)
    # Create output argument
    parser.add_argument("--output", default=Path.cwd())
    # Create overwrite argument
    parser.add_argument("--overwrite", default=False, type=bool)
    # Run the parser and place the extracted data in an argparse.Namespace object:
    args = parser.parse_args()

    # Create output directory if it does not exist (create parents if needed and if it exists, don't create directory)
    output_dir = Path(args.output)
    Path(args.output).mkdir(parents=True, exist_ok=True)

    # Assumption 1:

    # Create a path to the input data map
    input_dir = Path(args.input)

    # Create a path to the three files in the input data map
    file_countries = Path(input_dir / 'countries.csv')
    file_poule_phase_games = Path(input_dir / 'poule_phase_games.csv')
    file_final_phase_games = Path(input_dir / 'final_phase_games.csv')

    # Print true if file exists in input directory, otherwise print false
    error = 0

    if not file_countries.exists():
        error += 1
        print('countries.csv exists:' + str(file_countries.exists()))
    if not file_poule_phase_games.exists():
        error += 1
        print('poule_phase_games.csv exists:' + str(file_poule_phase_games.exists()))
    if not file_final_phase_games.exists():
        error += 1
        print('final_phase_games.csv exists:' + str(file_final_phase_games.exists()))

    # Assumption 2:

    # Check if the files are readable (check whether they are a .csv file)
    _, read_countries = os.path.splitext(file_countries)
    _, read_poule_phase_games = os.path.splitext(file_poule_phase_games)
    _, read_final_phase_games = os.path.splitext(file_final_phase_games)

    error_1 = 0
    if read_countries != ".csv":
        error_1 += 1
        print("countries is not a .csv")
    if read_poule_phase_games != ".csv":
        error_1 += 1
        print("poule_phase_games is not a .csv")
    if read_final_phase_games != ".csv":
        error_1 += 1
        print("final_phase_games is not a .csv")

    # Check if the files contain the right columns
    countries = pd.read_csv(file_countries)
    poule_phase = pd.read_csv(file_poule_phase_games)
    final_phase = pd.read_csv(file_final_phase_games)

    if not countries.columns.isin(['id', 'countries', 'ranking']).any():
        error_1 += 1
        print("countries.csv does not contain the right columns")
    if not poule_phase.columns.isin(['country_a', 'country_b', 'scores']).any():
        error_1 += 1
        print("poule_phase_games.csv does not contain the right columns")
    if not final_phase.columns.isin(['stage', 'match', 'score']).any():
        error_1 += 1
        print("final_phase_games.csv does not contain the right columns")

    df_assumptions = pd.DataFrame(columns = ['Assumptions'])

    if error > 0:
        new_assumption = pd.Series({'Assumptions' :
                        'Assumption 1: Not the right files are present in the input directory.'})
        df_assumptions = pd.concat([df_assumptions, new_assumption.to_frame().T],
                                                     ignore_index=True)

    if error_1 > 0:
        new_assumption = pd.Series({'Assumptions' :
                        'Assumption 2: Files are not readable and/or do not contain the right columns.'})
        df_assumptions = pd.concat([df_assumptions, new_assumption.to_frame().T],
                                                     ignore_index=True)
    return countries, poule_phase, final_phase, output_dir, df_assumptions

#if __name__ == '__main__':
#    _, _, _, output_dir, _ = load_data()
