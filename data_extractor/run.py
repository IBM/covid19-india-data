import argparse
import os
import sys
import json

from tqdm import tqdm
from bulletin_download import main as bulletin_downloader
from db.main import DBMain
from local_extractor import main as extractor_main
from local_extractor.utils import custom_exceptions


STATES = [
    'MH', 'HR', 'TG', 
    'WB', 'DL', 'KA', 
    'UK'
]

DOWNLOADED_BULLETINS_STR = 'downloaded-bulletins'
BULLETIN_PATH_STR = 'bulletin-paths'
PROCESSED_DATES_STR = 'processed-dates'


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--datadir', type=str, required=True, help='Data directory path to store bulletins and database')
    parser.add_argument('--run_only', type=str, required=False, default=None, help='Comma-separated values of states to run data extraction for')
    parser.add_argument('--force_run_states', type=str, required=False, default=None, help='Comma-separated values of states to force re-run data extraction procedure for')

    return parser


def run(args):

    # Get list of states to execute extraction procedure for
    states_to_execute = None
    if args.run_only is not None:
        states_to_execute = [x.strip() for x in args.run_only.split(',')]

    # Get list of states to force a re-run
    force_rerun_states = []
    if args.force_run_states is not None:
        force_rerun_states = [x.strip() for x in args.force_run_states.split(',')]
    
    # Download bulletins
    bulletin_links = bulletin_downloader.run(args.datadir, state_to_execute=states_to_execute)

    # Setup tables
    db_obj = DBMain(args.datadir)
    db_obj.record_bulletin_links(bulletin_links)
    db_obj.record_db_metadata()

    # Start extraction
    state_pbar = tqdm(STATES, desc="States")
    for state in state_pbar:

        if states_to_execute is not None and state not in states_to_execute:
            continue

        state_pbar.set_description(f'State: {state}')

        metadata_path = os.path.join(args.datadir, 'metadata', 'bulletins', f'{state}.json')
        with open(metadata_path, 'r') as f:
            data = json.load(f)

        if PROCESSED_DATES_STR not in data:
            data[PROCESSED_DATES_STR] = []

        date_pbar = tqdm(data[BULLETIN_PATH_STR].items(), desc="Dates", leave=False)
        for date, fpath in date_pbar:

            date_pbar.set_description(f'Date: {date}')

            if state not in force_rerun_states and date in data[PROCESSED_DATES_STR]:
                continue
            
            try:
                stateinfo = extractor_main.extract_info(state, date, fpath)
                db_obj.insert_for_state(state, stateinfo)
            except custom_exceptions.UnprocessedBulletinException as err:
                # Bulletin failed validation checks. Remove from metadata
                print(f'{state} Bulletin for date {date} failed validation checks')

                if date in data[DOWNLOADED_BULLETINS_STR]:
                    data[DOWNLOADED_BULLETINS_STR].remove(date)
            except Exception as err:
                print(f'Error in parsing date: {date}. Error: {err}')
            else:
                data[PROCESSED_DATES_STR].append(date)
        
        with open(metadata_path, 'w') as f:
            json.dump(data, f)


if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()
    run(args)