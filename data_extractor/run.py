import argparse
import os
import sys
import json

from tqdm import tqdm
from bulletin_download import main as bulletin_downloader
from db.main import DBMain
from local_extractor import main as extractor_main


COMPLETE_STATES = ['TG', 'WB', 'DL']
INCOMPLETE_STATES = ['HR', 'KA']


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--datadir', type=str, required=True, help="Data directory path to store bulletins and database")

    return parser


def run(args):

    BULLETIN_PATH_STR = 'bulletin-paths'
    PROCESSED_DATES_STR = 'processed-dates'

    
    # Download bulletins
    bulletin_links = bulletin_downloader.run(args.datadir)

    # Setup tables
    db_obj = DBMain(args.datadir)
    db_obj.record_bulletin_links(bulletin_links)
    db_obj.record_db_metadata()

    # Start extraction
    STATES = COMPLETE_STATES + INCOMPLETE_STATES

    state_pbar = tqdm(STATES, desc="States")
    for state in state_pbar:

        state_pbar.set_description(f'State: {state}')

        metadata_path = os.path.join(args.datadir, 'metadata', 'bulletins', f'{state}.json')
        with open(metadata_path, 'r') as f:
            data = json.load(f)

        if PROCESSED_DATES_STR not in data:
            data[PROCESSED_DATES_STR] = []

        date_pbar = tqdm(data[BULLETIN_PATH_STR].items(), desc="Dates", leave=False)
        for date, fpath in date_pbar:

            date_pbar.set_description(f'Date: {date}')

            if date in data[PROCESSED_DATES_STR]:
                continue
            
            try:
                stateinfo = extractor_main.extract_info(state, date, fpath)
                db_obj.insert_for_state(state, stateinfo)
            except Exception as err:
                print(f'Error in parsing date: {date}. Error: {err}')
            else:
                if state not in INCOMPLETE_STATES:
                    data[PROCESSED_DATES_STR].append(date)
        
        with open(metadata_path, 'w') as f:
            json.dump(data, f)


if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()
    run(args)