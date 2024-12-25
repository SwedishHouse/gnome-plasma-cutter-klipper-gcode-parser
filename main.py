import re


# def classify_command(command):
#     pattern_m_with_s = r'M\d+ S\d+$'
#     pattern_s_only = r'S\d+$'
#
#     if re.match(pattern_m_with_s, command):
#         return "Type M with S"
#     elif re.match(pattern_s_only, command):
#         return "Type S"
#     else:
#         return "Unknown Command"
#
#
# # Примеры использования функции
# commands = [
#     'S123',
#     'M456 S789',
#     'Sabc',  # не подходит, так как содержит буквы
#     'Mxyz Sdef',  # не подходит, так как Mxyz начинается с букв
#     'M999 S0000',
# ]


import re

# Регулярное выражение для поиска команд


# Функция для разбора строки на отдельные команды
def parse_commands(command_string):
    pattern = r'(M\d+ S\d+)|([GSFM]\d+)'
    matches = re.findall(pattern, command_string)
    commands = []
    for match in matches:
        if match[0]:
            commands.append(match[0])  # Команда типа Mxxx Sxxx
        else:
            commands.append(match[1])  # Другие команды (Gxxx, Fxxx, Sxxx, Mxxx)
    return commands

# Тестовые данные
test_strings = [
    "M100 S200",
    "G300",
    "F400 M500 S600",
    "M700 S800 G900",
    "M1000 S1100 F1200",
    "G300 S500 M30",  # Новый тестовый случай
]

# Список для хранения всех команд
all_commands = []

# Обрабатываем каждую строку
for test_string in test_strings:
    parsed_commands = parse_commands(test_string)
    all_commands.extend(parsed_commands)

# Выводим все команды с индексами
print("All Commands:")
for index, cmd in enumerate(all_commands, start=1):
    print(f"{index}. {cmd}")

# if __name__ == '__main__':
#     # for command in commands:
#     #     result = classify_command(command)
#     #     print(f"{command}: {result}")
#
#     all_commands = []
#
#     # Обрабатываем каждую строку
#     for test_string in test_strings:
#         parsed_commands = parse_commands(test_string)
#         all_commands.extend(parsed_commands)
#
#     # Выводим все команды
#     print("All Commands:")
#     for index, cmd in enumerate(all_commands):
#         print(index, cmd)
#
