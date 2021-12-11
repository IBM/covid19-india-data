# Individual Cases Text Parser
# From Tamil Nadu Bulletins

from __future__ import annotations

import multiprocessing
import sys
import pathlib
import argparse
import os
import re
import json
import pdfplumber

if sys.version_info >= (3, 8):
    from typing import TypedDict, Dict, List, Optional
else:
    from typing_extensions import TypedDict

_path_this_dir = pathlib.Path(__file__).parent
_path_to_examples = _path_this_dir.joinpath("./case_examples")
_set_timeout = 10

_stop_words = [
    r".*24\*7.*",
    r".*Passengers entered.*",
    r".*Death\s+in.*"
]

_stop_splits = [
    r"24\*7",
    r"Passengers entered",
    r"Death\s+in"
]

def read_text(test_text: str, category: str = None, date: str = None) -> CaseInfo:

    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    p = multiprocessing.Process(target=CaseInfo.extract, args=(test_text, category, date, return_dict))
    p.start()
    p.join(_set_timeout)

    if p.is_alive():
        p.kill()

    return return_dict["result"]


def read_file(filename: str) -> List[CaseInfo]:

    result = list()

    if filename.endswith('.txt'):
        result.append(read_text(open(filename).read()))
    elif filename.endswith('.pdf'):

        with pdfplumber.open(filename) as pdf:
            last_match = ""
            category = None
            date = None

            for i, page in enumerate(pdf.pages):
                text = page.extract_text()

                template = re.compile(r".*Media\s+Bulletin\s+(?P<date>((?!\n).)+)\n.*$", re.DOTALL)
                matches = re.match(template, text)

                if matches:
                    date = matches.groupdict()["date"]

                if "death case" in text.lower():
                    text = last_match + text
                    last_match = ""

                    category_match = re.split(r"Death\s+in", text, flags=re.IGNORECASE)

                    for item in category_match:

                        new_category = re.split(r'death\scase', item, flags=re.IGNORECASE)[0]
                        new_category = " ".join(new_category.split())

                        if not new_category or "no." in new_category.lower():
                            new_category = category

                        case_match = re.split(r"Death\s+Case", item, flags=re.IGNORECASE)

                        for ii in case_match:

                            ii = " ".join(ii.split("  "))

                            if not any([re.match(s, ii, flags=re.IGNORECASE|re.DOTALL) for s in _stop_words]):
    
                                try: result.append(read_text(ii, category=new_category, date=date))
                                except: pass

                            else:

                                last_match = ii
                                for s in _stop_splits:
                                    last_match = re.split(s, last_match, flags=re.IGNORECASE)[0] 

                        category = new_category

                else: 

                    if last_match:
                        try: result.append(read_text(last_match, category=category, date=date))
                        except: pass

                        last_match = None

            return result



def process_data(cls, data: Dict):
    response = cls()

    for key in cls.__annotations__:

        custom_enforcer_function = getattr(eval(cls.__annotations__[key].__forward_arg__), "extract", None)
        response[key] = None

        if callable(custom_enforcer_function):
            response[key] = custom_enforcer_function(data[key])

        else:

            if data[key]:
                response[key] = eval("{}(\"{}\")".format(cls.__annotations__[key].__forward_arg__, data[key].strip()))

    return response


class TestInfo(TypedDict):
    date: str
    details: str


    @classmethod
    def process(cls, data: Dict) -> TestInfo:
        return process_data(cls, data)


    @classmethod
    def extract(cls, text: str) -> TestInfo:

        if not text:
            return None

        input_text = text.strip()
        regex = r'\D*(having|outcome of)\s*(?P<details>((?!\s+on\s+).)+)(\s*on\s+(?P<date>((?!\.$|\.\s+).)+))*.*$'

        template = re.compile(regex, re.IGNORECASE|re.DOTALL)
        matches = re.match(template, input_text)

        if matches:

            matches = matches.groupdict()
            return cls.process(data = matches)



class SymptomInfo(TypedDict):
    days: int
    details: str

    @classmethod
    def process(cls, data: Dict) -> SymptomInfo:
        return process_data(cls, data)


    @classmethod
    def extract(cls, text: str) -> SymptomInfo:

        if not text:
            return None

        input_text = text.strip()
        regex = r'(?P<details>((?!\s+for).)+)(\s*for\s+(?P<days>\d+)\s+day(s)*)*.*$'

        template = re.compile(regex, re.IGNORECASE|re.DOTALL)
        matches = re.match(template, input_text)

        if matches:
            matches = matches.groupdict()
            return cls.process(data = matches)


class AdmissionInfo(TypedDict):
    symptoms: SymptomInfo
    location: str
    date: str
    time: str

    @classmethod
    def process(cls, data: Dict) -> AdmissionInfo:
        return process_data(cls, data)

    @classmethod
    def extract(cls, text: str) -> AdmissionInfo:

        if not text:
            return None

        input_text = text.strip()
        regex = r'.*admitted\s+on\s+(?P<date>((?!\s).)+)(\s*at\s+(?P<time>((?!in|with).)+)\s+)*(\s*(in a|in|at a)\s+(?P<location_1>((?!with).)+)\s+)*(\s*with complaints of\s+(?P<symptoms>((?!in a\s+|at\s+|$).)+)\s*)*(\s*(in a|in|at a)\s+(?P<location_2>((?!\s+and|$).)+)\s*)*.*$'

        template = re.compile(regex, re.IGNORECASE|re.DOTALL)

        matches = re.match(template, input_text)

        if matches:
            matches = matches.groupdict()
            matches["location"] = matches["location_1"] or matches["location_2"]

            return cls.process(data = matches)


class DeathInfo(TypedDict):
    cause: str
    date: str
    time: str

    @classmethod
    def process(cls, data: Dict) -> DeathInfo:
        return process_data(cls, data)

    @classmethod
    def extract(cls, text: str) -> DeathInfo:

        if not text:
            return None

        input_text = text.strip()
        derived_dict = dict()

        regex = r'.*died\s+(on|in)\s+(?P<date>((?!\s).)+)(\s+at\s+(?P<time>((?!due|$).)+)\s+)*(\s*due\s+to(?P<cause>.+))*.*$'

        template = re.compile(regex, re.IGNORECASE|re.DOTALL)
        matches = re.match(template, input_text)

        if matches: 

            matches = matches.groupdict()
            derived_dict = {**derived_dict, **matches}

            return cls.process(data = derived_dict)


class CaseInfo(TypedDict):
    case_id: int
    category: str
    date: str
    age: int
    gender: str
    location: str
    comorbidity: str
    test: TestInfo
    admission: AdmissionInfo
    death: DeathInfo
    raw_data: str

    @classmethod
    def process(cls, data: Dict) -> CaseInfo:
        return process_data(cls, data)

    @classmethod
    def extract(cls, text: str, category: str, date: str, return_dict: Dict = None) -> CaseInfo:

        input_text = text.strip()

        if not input_text.endswith("."):
            input_text += "."

        derived_dict = {
            "category" : category,
            "date": date,
        }

        regex = r'\D*((?P<case_id>\d+)*\D*\n+)*(?P<raw_data>.*)$'
        template = re.compile(regex, re.IGNORECASE|re.DOTALL)
        matches = re.match(template, input_text)

        if matches:

            matches = matches.groupdict()
            matches["raw_data"] = " ".join(matches["raw_data"].split())

            derived_dict = {**derived_dict, **matches}

            regex = r'\D*(?P<age>\d+) year[s]* old (?P<gender>\D+) from (?P<location>((?!having|with|admitted).)*)(?P<test_info_1>having((?!with|admitted).)*)*(?P<comorbidity>with((?!admitted).)*)*(?P<admission>admitted((?!died|\.\s+|\.$).)*)*(?P<test_info_2>((?!died).)+)*(?P<death>died\s*(on|in).*)*\..*$'

            template = re.compile(regex, re.IGNORECASE)
            matches = re.match(template, derived_dict["raw_data"])

            if matches:
                matches = matches.groupdict()

                matches["test"] = matches["test_info_1"] or matches["test_info_2"]
                derived_dict = {**derived_dict, **matches}

                return_dict["result"] = cls.process(data = derived_dict)

        return return_dict


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parser for Tamil Nadu case data.')
    parser.add_argument('--file', type=str, help='File containing data.')
    parser.add_argument('--dir', type=str, help='Directory containing files containing data.')

    args = parser.parse_args()
    data = None

    if args.file:
        data = read_file(args.file)

    elif args.dir:

        _path_to_examples = args.dir
        data = list()

        list_of_test_files = [f.path for f in os.scandir(_path_to_examples)]
        for test_file in list_of_test_files:
            print(f'Reading file {test_file} {list_of_test_files.index(test_file)}/{len(list_of_test_files)}')

            try:
                new_data = read_file(test_file)

                if new_data:
                    data += new_data

            except Exception as e: 
                print(e)

    with open("data.json", "w") as out_file:
        out_file.write(json.dumps(data, indent=4))

