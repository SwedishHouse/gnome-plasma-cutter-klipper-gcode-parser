import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gcode_parser.multiple_gcmd import GCode, GCodeSplitter
import json
import pytest
import random


DIR_TEST_DATA = "..\\tests-data"
DIR_LEVEL_UP = ".."
SINGLE_LINE_CMDS = "test_gcode_data.json"
PATH_TO_SINGLE_LINE_CMDS = os.path.join(os.path.dirname(__file__), DIR_TEST_DATA, SINGLE_LINE_CMDS)  # + "\\" + "..\\tests-data\\test_gcode_data.json"


def test_g0():
    x_coord = 15.2
    gcode = GCode(f'G00 X{x_coord}')

    assert f'G00 X{x_coord}' == gcode.get_cmd()


def test_g1():
    x_coord = 15.2
    y_coord = 42.3
    z_coord = 12.4
    gcode = GCode(f'G01 X{x_coord} Y{y_coord} Z{z_coord}')

    assert f'G01 X{x_coord} Y{y_coord} Z{z_coord}' == gcode.get_cmd()


def test_g1_loop():
    for i in range(-3000, 3000):
        x_coord = random.random() + i
        y_coord = random.random() + i
        z_coord = random.random() + i
        gcode = GCode(f'G01 X{x_coord} Y{y_coord} Z{z_coord}')

        assert f'G01 X{x_coord} Y{y_coord} Z{z_coord}' == gcode.get_cmd()


def test_g40():
    gcode = GCode('G40')

    assert f'G40' == gcode.get_cmd()


def test_gcode_parsed_single_string():
    gcode = GCode("G1 X5 Y15")
    res = {"cmd": "G1", "params": {"X": 5, "Y": 15}}
    assert res == gcode.get()

# Загрузка тестовых данных из файла
@pytest.fixture
def test_data():
    # data_file_path = "D:\\GitHub\\stepper-parser\\gcode-files\\test_gcode_data.json"
    data_file_path = PATH_TO_SINGLE_LINE_CMDS
    with open(data_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_process_data(test_data):
    for case in test_data:

        input_data = case['input']
        expected_result = case['expected']
        gcode = GCode(input_data)
        assert gcode.get() == expected_result


if __name__ == "__main__":
    # splitter = GCodeSplitter()
    # splitter.parse_gcode_line('G40 G01 X100 G54')
    print(os.path.join(os.path.dirname(__file__)))
