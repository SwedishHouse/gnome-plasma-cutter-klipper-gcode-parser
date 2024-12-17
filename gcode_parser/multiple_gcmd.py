import re


# class Gcode:
#
#     def __init__(self, name: str, params: dict[str, float] | None) -> None:
#         self.name = name
#         self.params = params
#
#     @property
#     def get_param(self) -> str:
#         if self.params:
#             return ' '.join(key + str(val) for key, val in self.params.items())
#         return ''
#
#     @property
#     def get_name(self) -> str:
#         return self.name
#
#     def get_cmd(self):
#         return self.name + ' ' * bool(self.get_param) + self.get_param

class GCode:

    def __init__(self, line: str) -> None:
        gcode = line.split()
        self.cmd = gcode[0]
        self.params = self.convert_to_dict(gcode[1::])

    def get(self):
        return {"cmd": self.cmd, "params": self.params}

    @staticmethod
    def convert_to_dict(coordinate_list):
        result = {}
        for item in coordinate_list:
            match = re.match(r"([A-Z]+)([-+]?\d*\.?\d+)", item)
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

    def __init__(self) -> None:
        self.pattern = r'([GMSFTDH]\d+\.?\d*)|([F]\d+\.?\d*)'

    def parse_gcode_line(self, line):
        # Регулярное выражение для поиска команд и их параметров
        pattern = r'([GMSFTDH]\d+\.?\d*)|([XYZIJKR]\d+\.?\d*)'
        matches = re.findall(pattern, line)

        # Объединяем команды и параметры в один список
        commands = []
        current_command = None

        for match in matches:
            command = match[0] if match[0] else match[1]

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
            commands.append(current_command)

        return commands


if __name__ == '__main__':
    gcode = GCode("G00 X15.2")
