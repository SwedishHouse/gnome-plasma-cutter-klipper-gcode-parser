

source_file = "leaf.gcode"
new_file = "new_" + source_file
result = []

with open(source_file, 'r') as f:
    for line in f:
        if line.startswith("N"):
            new_line = ' '.join(line.split()[1::])
            result.append(new_line)

with open(new_file, "w") as f:
    for line in result:
        f.writelines(line + '\n')

