# Individual Cases Text Parser
# From Tamil Nadu Bulletins

from __future__ import annotations

import sys
import pathlib
import argparse
import os
import re
import json

if sys.version_info >= (3, 8):
    from typing import TypedDict, Dict, Optional
else:
    from typing_extensions import TypedDict

_path_this_dir = pathlib.Path(__file__).parent
_path_to_examples = _path_this_dir.joinpath("./case_examples")


def read_text(test_text: str, category: str = None) -> CaseInfo:
    return CaseInfo.extract(test_text, category)


def read_test_file(filename: str) -> CaseInfo:
    return read_text(open(filename).read())


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
    def process(cls, data: Dict) -> DeathInfo:
        return process_data(cls, data)


    @classmethod
    def extract(cls, text: str) -> DeathInfo:

        if not text:
            return None

        input_text = text.strip()
        regex = r'\D*(having|outcome of)\s*(?P<details>((?!\s+on\s+).)+)(\s*on\s+(?P<date>((?!\.$|\.\s+).)+))*.*$'

        template = re.compile(regex, re.IGNORECASE|re.DOTALL)
        matches = re.match(template, input_text).groupdict()

        return cls.process(data = matches)



class SymptomInfo(TypedDict):
    days: int
    details: str

    @classmethod
    def process(cls, data: Dict) -> DeathInfo:
        return process_data(cls, data)


    @classmethod
    def extract(cls, text: str) -> DeathInfo:

        if not text:
            return None

        input_text = text.strip()
        regex = r'(?P<details>((?!\s+for).)+)(\s*for\s+(?P<days>\d+)\s+days)*.*$'

        template = re.compile(regex, re.IGNORECASE|re.DOTALL)
        matches = re.match(template, input_text).groupdict()

        return cls.process(data = matches)


class AdmissionInfo(TypedDict):
    symptoms: SymptomInfo
    location: str
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
        regex = r'.*admitted\s+on\s+(?P<date>((?!\s).)+)(\s*at\s+(?P<time>((?!in|with).)+)\s+)*(\s*(in a|in|at a)\s+(?P<location_1>((?!with).)+)\s+)*(\s*with complaints of\s+(?P<symptoms>((?!in a\s+|at\s+|$).)+)\s*)*(\s*(in a|in|at a)\s+(?P<location_2>((?!\s+and|$).)+)\s*)*.*$'

        template = re.compile(regex, re.IGNORECASE|re.DOTALL)

        matches = re.match(template, input_text).groupdict()
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

        input_text = text.strip()
        derived_dict = dict()
        regex = r'.*died\s+on\s+(?P<date>((?!\s).)+)(\s+at\s+(?P<time>((?!due|$).)+)\s+)*(due\s+to(?P<cause>.+))*.*$'

        template = re.compile(regex, re.IGNORECASE|re.DOTALL)
        matches = re.match(template, input_text).groupdict()
        derived_dict = {**derived_dict, **matches}

        return cls.process(data = derived_dict)


class CaseInfo(TypedDict):
    case_id: int
    category: str
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
    def extract(cls, text: str, category: str) -> CaseInfo:

        input_text = text.strip()
        derived_dict = {
            "category" : category,
        }

        regex = r'\D*((?P<case_id>\d+)*\D*\n+)*(?P<raw_data>.*)$'
        template = re.compile(regex, re.IGNORECASE|re.DOTALL)
        matches = re.match(template, input_text).groupdict()

        matches["raw_data"] = " ".join(matches["raw_data"].split())

        derived_dict = {**derived_dict, **matches}

        regex = r'\D*(?P<age>\d+) year[s]* old (?P<gender>\D+) from (?P<location>((?!having|with|admitted).)*)(?P<test_info_1>having((?!with|admitted).)*)*(?P<comorbidity>with((?!admitted).)*)*(?P<admission>admitted((?!died|\.\s+|\.$).)*)*(?P<test_info_2>((?!died).)+)*(?P<death>died on.*)*\..*$'

        template = re.compile(regex, re.IGNORECASE)
        matches = re.match(template, derived_dict["raw_data"])
        matches = matches.groupdict()

        matches["test"] = matches["test_info_1"] or matches["test_info_2"]
        derived_dict = {**derived_dict, **matches}

        return cls.process(data = derived_dict)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parser for Tamil Nadu case data.')
    parser.add_argument('--file', type=str, help='File containing text.')

    args = parser.parse_args()

    if args.file: print(json.dumps(read_test_file(args.file), indent=4))
    else:

        list_of_test_files = [f.path for f in os.scandir(_path_to_examples) if f.path.endswith('.txt')]
        for test_file in list_of_test_files:
            print('Reading file', test_file)
            print(json.dumps(read_test_file(test_file), indent=4))

