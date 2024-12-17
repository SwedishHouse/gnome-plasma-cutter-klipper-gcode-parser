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
PATH_TO_MULTIPLE_CMD_ON_LINE = os.path.join(os.path.dirname(__file__), DIR_TEST_DATA, SINGLE_LINE_CMDS)  # + "\\" + "..\\tests-data\\test_gcode_data.json"
PATH_TO_CMDS_WITHOUT_PARSED_PARAMS = os.path.join(os.path.dirname(__file__), DIR_TEST_DATA, NO_PARSED_PARAMS_FILE)

def test_file_opens_successfully():
    # Предположим, что файл существует и доступен для чтения
    filename = "example.txt"
    for num, i in enumerate([PATH_TO_MULTIPLE_CMD_ON_LINE, PATH_TO_CMDS_WITHOUT_PARSED_PARAMS]):
        try:
            with open(i, mode="r") as file:
                content = json.load(file)

            assert True, f"Файл {num} успешно открыт."
        except IOError as e:
            pytest.fail(f"Не удалось открыть файл {num}: {e}")

def test_splitter():
    splitter = GCodeSplitter()
    # res = [GCode(i) for i in ['G40', 'G01 X100 Y52.4', 'G54', 'F100']]
    assert ['G40', 'G01 X100 Y52.4', 'G54', 'F100'] == splitter.parse_gcode_line('G40 G01 X100 Y52.4 G54 F100'.split('\n'))

