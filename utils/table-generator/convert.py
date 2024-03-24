#!/bin/python3

import sys

# magic values
NO   = 0
AUTO = 1
YES  = 2

def convert_generic_v1(data):
    split_raw_lines = [i.strip().split("|") for i in data.split("\n") if i]
    
    return generate_table(split_raw_lines)

def convert_usecase_v1(filename, data):
    split_raw_lines_from_file = [i.split(" | ") for i in data.split("\n") if i]

    if '/' in filename:
        use_case_name = filename.rsplit("/", 1)[1].upper()
    elif '\\' in filename:
        use_case_name = filename.rsplit("\\", 1)[1].upper()
    else:
        use_case_name = filename.upper()

    split_raw_lines = [["ID", use_case_name]] + split_raw_lines_from_file

    merged_lines = []
    for i in split_raw_lines:
        if i[0] == "":
            merged_lines[-1][1] += "<br>" + i[1]
        else:
            merged_lines.append(i)

    return generate_table(merged_lines)

def generate_table(raw_table_data):
    table_lines = raw_table_data
    transposed_table = list(zip(*table_lines))

    field_sizes = [max([max([len(k)+2 for k in j.split("\n")]) for j in i]) for i in transposed_table]

    formatted_table_lines = []

    l = "|"
    for i, field in enumerate(table_lines[0]):
        l += field.center(field_sizes[i])
        l += "|"

    formatted_table_lines.append(l)
    formatted_table_lines.append(f"|{'|'.join([':'+'-'*(i-2)+':' for i in field_sizes])}|")

    for line in table_lines[1:]:
        l = "|"
        for i, field in enumerate(line):
            l += field.center(field_sizes[i])
            l += "|"

        formatted_table_lines.append(l)

    return "\n".join(formatted_table_lines)


if __name__=="__main__":
    # parse args
    files = []
    write_to_file = AUTO
    write_to_stdout = AUTO
    usecase_formatting = AUTO
    verbose = AUTO

    for i in sys.argv[1:]:
        if i.startswith("-"):
            # записувати таблицю в файл
            if i in ["-f", "--file"]:
                write_to_file = YES
            elif i in ["-nf", "--no-file"]:
                write_to_file = NO

            # виводити таблицю у стандартний вивід
            elif i in ["-o", "--stdout"]:
                write_to_stdout = YES
            elif i in ["-no", "--no-stdout"]:
                write_to_stdout = NO

            # форматувати таблицю як use-case
            elif i in ["-u", "--usecase", "--use-case"]:
                usecase_formatting = YES
            elif i in ["-nu", "--no-usecase", "--no-use-case"]:
                usecase_formatting = NO

            # виводити на екран додаткову інформацію
            elif i in ["-v", "--verbose"]:
                verbose = YES
            elif i in ["-nv", "--no-verbose"]:
                verbose = NO

        else:
            files.append(i)

    if len(files) < 1:
        print("You need to pass at least one file as CLI argument", file=sys.stderr)
        print("Exiting...", file=sys.stderr)
        exit(1)

    if len(files) == 1:
        name = files[0]
        data = open(name, encoding = "utf-8").read()

        if usecase_formatting == YES:
            if verbose == YES:
                print(f"Force-formatting {name} as a use-case\n")
            formatted_table_data = convert_usecase_v1(name.rsplit(".", 1)[0], data)
        elif (name.endswith(".usecase") or name.endswith(".uc")) and usecase_formatting >= AUTO:
            if verbose == YES:
                print(f"Auto-detected use-case in file {name}\n")
            formatted_table_data = convert_usecase_v1(name.rsplit(".", 1)[0], data)
        else:
            formatted_table_data = convert_generic_v1(data)

        if write_to_stdout >= AUTO:
            print(formatted_table_data)
        
        if write_to_file > AUTO:
            open(name + ".table", 'w', encoding = "utf-8").write(data+"\n")

        exit(0)

    for no, name in enumerate(sys.argv[1:]):
        print(f"Converting {no+1}/{len(sys.argv)}")

        data = open(name, encoding = "utf-8").read()

        if usecase_formatting == YES:
            if verbose >= AUTO:
                print(f"Force-formatting {name} as a use-case")
            formatted_table_data = convert_usecase_v1(name.rsplit(".", 1)[0], data)
        elif (name.endswith(".usecase") or name.endswith(".uc")) and usecase_formatting >= AUTO:
            if verbose >= AUTO:
                print(f"Auto-detected use-case in file {name}")
            formatted_table_data = convert_usecase_v1(name.rsplit(".", 1)[0], data)
        else:
            formatted_table_data = convert_generic_v1(data)

        if write_to_stdout > AUTO:
            print(formatted_table_data)
        
        if write_to_file >= AUTO:
            open(name + ".table", 'w', encoding = "utf-8").write(data+"\n")
