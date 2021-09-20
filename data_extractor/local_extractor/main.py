from local_extractor.states.DL import DelhiExtractor
from local_extractor.states.WB import WestBengalExtractor


STATE_LIST = {
    'DL': DelhiExtractor,
    'WB': WestBengalExtractor,
    'TN': TamilNaduExtractor
}


def extract_info(state, date, report_fpath):
    state_obj = STATE_LIST[state](date, report_fpath)
    vals = state_obj.extract()
    return vals
