from local_extractor.states.DL import DelhiExtractor
from local_extractor.states.WB import WestBengalExtractor
from local_extractor.states.TG import TelanganaExtractor
from local_extractor.states.HR import HaryanaExtractor
from local_extractor.states.KA import KarnatakaExtractor


STATE_LIST = {
    'DL': DelhiExtractor,
    'WB': WestBengalExtractor,
    'TG': TelanganaExtractor,
    'HR': HaryanaExtractor,
    'KA': HaryanaExtractor
}


def extract_info(state, date, report_fpath):
    state_obj = STATE_LIST[state](date, report_fpath)
    vals = state_obj.extract()
    return vals