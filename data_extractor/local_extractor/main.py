from local_extractor.states.DL import DelhiExtractor
from local_extractor.states.GA import GoaExtractor
from local_extractor.states.HR import HaryanaExtractor
from local_extractor.states.KA import KarnatakaExtractor
from local_extractor.states.KL import KeralaExtractor
from local_extractor.states.MH import MaharashtraExtractor
from local_extractor.states.MP import MadhyaPradeshExtractor
from local_extractor.states.PB import PunjabExtractor
from local_extractor.states.TG import TelanganaExtractor
from local_extractor.states.TN import TamilNaduExtractor
from local_extractor.states.UK import UttarakhandExtractor
from local_extractor.states.WB import WestBengalExtractor


STATE_LIST = {
    'DL': DelhiExtractor,
    'GA': GoaExtractor,
    'HR': HaryanaExtractor,
    'KA': KarnatakaExtractor,
    'KL': KeralaExtractor,
    'MH': MaharashtraExtractor,
    'MP': MadhyaPradeshExtractor,
    'PB': PunjabExtractor,
    'TG': TelanganaExtractor,
    'TN': TamilNaduExtractor,
    'UK': UttarakhandExtractor,
    'WB': WestBengalExtractor,
}


def extract_info(state, date, report_fpath):
    state_obj = STATE_LIST[state](date, report_fpath)
    vals = state_obj.extract()
    return vals
