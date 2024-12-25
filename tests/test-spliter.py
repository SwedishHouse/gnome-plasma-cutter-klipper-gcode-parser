import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gcode_parser.multiple_gcmd import GCode, GCodeSplitter
import json
import pytest
import random

DIR_TEST_DATA = "..\\tests-data"
DIR_LEVEL_UP = "../.."
SINGLE_LINE_CMDS = "test_gcode_for_split.json"
NO_PARSED_PARAMS_FILE = "test_gcode_split_into_string.json"
FILE_FOR_HAS_MULTIPLE_CMDS = "test_has_multiple_cmd.json"
PATH_TO = {}


def get_path(filename):
    return os.path.join(os.path.dirname(__file__), DIR_TEST_DATA, filename)


PATH_TO['MULTIPLE_CMD_ON_LINE'] = get_path(SINGLE_LINE_CMDS)
PATH_TO['CMDS_WITHOUT_PARSED_PARAMS'] = get_path(NO_PARSED_PARAMS_FILE)
PATH_TO['FILE_FOR_HAS_MULTIPLE_CMDS'] = get_path(FILE_FOR_HAS_MULTIPLE_CMDS)
PATH_TO['split_grouped_commands'] = get_path('test_' + 'split_grouped_commands' + '.json')
# PATH_TO_MULTIPLE_CMD_ON_LINE = os.path.join(os.path.dirname(__file__), DIR_TEST_DATA, SINGLE_LINE_CMDS)  # + "\\" + "..\\tests-data\\test_gcode_data.json"
# PATH_TO_CMDS_WITHOUT_PARSED_PARAMS = os.path.join(os.path.dirname(__file__), DIR_TEST_DATA, NO_PARSED_PARAMS_FILE)
# PATH_TO_FILE_FOR_HAS_MULTIPLE_CMDS = os.path.join(os.path.dirname(__file__), DIR_TEST_DATA, FILE_FOR_HAS_MULTIPLE_CMDS)

splitter = GCodeSplitter()


def test_file_opens_successfully():
    # Предположим, что файл существует и доступен для чтения
    filename = "example.txt"
    # for num, i in enumerate([PATH_TO_MULTIPLE_CMD_ON_LINE, PATH_TO_CMDS_WITHOUT_PARSED_PARAMS, PATH_TO_FILE_FOR_HAS_MULTIPLE_CMDS]):
    for num, (key, val) in enumerate(PATH_TO.items()):
        try:
            with open(val, mode="r") as file:
                content = json.load(file)

            assert True, f"Файл {num} успешно открыт."
        except IOError as e:
            pytest.fail(f"Не удалось открыть файл {num}: {e}")


def test_splitter():
    splitter = GCodeSplitter()
    # res = [GCode(i) for i in ['G40', 'G01 X100 Y52.4', 'G54', 'F100']]
    assert ['G40', 'G01 X100 Y52.4', 'G54', 'F100'] == splitter.parse_gcode_line('G40 G01 X100 Y52.4 G54 F100'.split('\n'))


@pytest.fixture
def test_data_has_multiple_commands():
    # data_file_path = "D:\\GitHub\\stepper-parser\\gcode-files\\test_gcode_data.json"
    data_file_path = PATH_TO['FILE_FOR_HAS_MULTIPLE_CMDS']
    with open(data_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_has_multiple_commands(test_data_has_multiple_commands):

    for index, case in enumerate(test_data_has_multiple_commands):
        input_data = case['input']
        expected_result = case['expected']
        assert splitter.has_multiple_commands(input_data) == expected_result, f"{index}: data = {input_data} expected = {expected_result}"


@pytest.fixture
def test_data_split_grouped_commands():
    data_file_path = PATH_TO['split_grouped_commands']
    with open(data_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_split_grouped_commands(test_data_split_grouped_commands):
    for index, case in enumerate(test_data_split_grouped_commands):
        input_data = case['input']
        expected_result = case['expected']
        assert splitter.split_grouped_commands(input_data) == expected_result, f'{index}: data = {input_data} expected = {expected_result}'


# @pytest.fixture
# def test_data():
#     # data_file_path = "D:\\GitHub\\stepper-parser\\gcode-files\\test_gcode_data.json"
#     data_file_path = PATH_TO_CMDS_WITHOUT_PARSED_PARAMS
#     with open(data_file_path, 'r', encoding='utf-8') as f:
#         return json.load(f)
#
#
# def test_string_cmd(test_data):
#
#     for index, case in enumerate(test_data):
#         input_data = case['input'].split('\n')
#         expected_result = case['expected']
#         assert splitter.parse_gcode_line(input_data) == expected_result, f"{index}: data = {input_data}"
