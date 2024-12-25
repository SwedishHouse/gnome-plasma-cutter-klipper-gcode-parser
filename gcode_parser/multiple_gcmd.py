import re


class GCode:

    PATTERN = r"([A-Z]+)([-+]?\d*\.?\d+)"

    def __init__(self, line: str) -> None:
        cmd = line.split()
        self.cmd = cmd[0]
        self.params = self.convert_to_dict(cmd[1::])

    def get(self):
        return {"cmd": self.cmd, "params": self.params}

    def convert_to_dict(self, coordinate_list):
        result = {}
        for item in coordinate_list:
            match = re.match(self.PATTERN, item)
            if match:
                key = match.group(1)
                try:
                    value = int(match.group(2))
                except ValueError:
                    value = float(match.group(2))

                result[key] = value
        return result

    def get_cmd(self):
        return self.cmd + ' ' * bool(self.get_param) + self.get_param

    @property
    def get_param(self) -> str:
        if self.params:
            return ' '.join(key + str(val) for key, val in self.params.items())
        return ''

    @property
    def get_name(self) -> str:
        return self.cmd


class GCodeSplitter:

    MOVE_CMDS = ('G0', 'G00', 'G1', 'G01', 'G2', 'G02', 'G3', 'G03')

    def __init__(self) -> None:
        self.last_command = "G0"
        self.PATTERN = r'([GMSFTDH]-?\d+\.?\d*)|([XYZABCIJKR]-?\d+\.?\d*)|\(.*?\)'

    @staticmethod
    def replace_decimal_point(command):
        # Регулярное выражение для замены точки на нижнее подчеркивание в вещественных числах
        return re.sub(r'(\d+)\.(\d+)', r'\1_\2', command)

    @staticmethod
    def remove_comments(command):
        # Регулярное выражение для удаления комментариев внутри скобок
        return re.sub(r'\(.*?\)', '', command).strip()

    @staticmethod
    def has_multiple_commands(command):
        # Регулярное выражение для проверки наличия нескольких команд в строке
        pattern = r'^[GMSF]\d+(\.\d+)?(\s+[GMSF]\d+(\.\d+)?)+$'
        return re.match(pattern, command) is not None

    def is_coordinate_only(self, command):
        pattern = r'^[XYZABCIJ]\s*-?\d+(\.\d+)?(\s+[XYZABCIJ]\s*-?\d+(\.\d+)?)*$'
        return re.match(pattern, command) is not None

    def split_grouped_commands(self, commands: list):
        processed_commands = []
        for command in commands:
            command = self.remove_comments(command)
            # Проверка на наличие нескольких команд в строке
            if self.has_multiple_commands(command):
                # Разделение сгруппированных команд
                # split_commands = re.findall(r'[GMSF]\d+(\.\d+)?', command)
                split_commands = command.split()
                split_commands = [self.replace_decimal_point(cmd) for cmd in split_commands]
                processed_commands.extend(split_commands)
            elif self.is_coordinate_only(command):
                if self.last_command:
                    command = self.last_command + ' ' + command
                processed_commands.append(command)
            else:
                # command = self.replace_decimal_point(command)
                processed_commands.append(command)
                if len(command) > 0:
                    cmd_identifier = command.split()[0]
                    if cmd_identifier in self.MOVE_CMDS:
                        self.last_command = cmd_identifier
        return processed_commands



    # @staticmethod
    # def is_dots_in_cmd(cmd):
    #     return re.match(r'^[GMS][0-9]+(\.[0-9]+)?$', cmd)
    # #                 command = command.replace('.', '_')

    def parse_gcode_line(self, line: list) -> list:
        # Регулярное выражение для поиска команд и их параметров
        result = []
        for item in line:
            matches = re.findall(self.PATTERN, item)

            # Объединяем команды и параметры в один список
            commands = []
            current_command = None

            for match in matches:
                command = match[0] if match[0] else match[1]
                if re.match(r'^[GMS][0-9]+(\.[0-9]+)?$', command):
                    command = command.replace('.', '_')
                # Если это новая команда, добавляем ее в список
                if re.match(r'[GMSFTDH]', command):
                    if current_command:
                        commands.append(current_command)
                    current_command = command
                else:
                    # Если это параметр, добавляем его к текущей команде
                    if current_command:
                        current_command += ' ' + command

            # Добавляем последнюю команду
            if current_command:
                commands.append(current_command.strip())

            result.extend(commands)
        return result


if __name__ == '__main__':
    gcode = GCode("G00 X15.2")
    splitter = GCodeSplitter()
    # data = "QUERY_ENDSTOP".split('\n')
    # res = splitter.parse_gcode_line(data)
    res = splitter.split_grouped_commands(["G0 X10 Y20", "G40 G54 G92.1"])
    # print(splitter.is_coordinate_command("X-100 Y+152.2 Z32"))
