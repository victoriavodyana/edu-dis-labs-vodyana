#!/bin/python3

import sys
import os

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
        if i[0].replace(" ", "") == "":
            merged_lines[-1][1] += "<br>" + i[1]
        else:
            merged_lines.append(i)

    return generate_table(merged_lines)

def convert_activity_v1(filename, data):
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
        if i[0].replace(" ", "") == "":
            merged_lines[-1][1] += "<br>" + i[1]
        else:
            merged_lines.append(i)

    return generate_table_with_activity_diagram(merged_lines)

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

def convert_line_to_activity_diagram(line):
    split_line = line[1].split("<br>")

    result = "@startuml\n    %PLACEHOLDER%\nstop\n@enduml"

    last_swimline_name = ""
    initiator_name = ""

    for i in split_line:
        clear_line = i.lstrip("1234567890. ")
        swimline_label, combined_action = clear_line.split(" ", 1)

        action_and_exceptions = combined_action.split(" (")

        if len(action_and_exceptions) > 1:
            action = action_and_exceptions[0].strip().capitalize()
            exceptions = action_and_exceptions[1].strip(") ").capitalize()
        else:
            action = action_and_exceptions[0].strip().capitalize()
            exceptions = ""

        # запам'ятовуємо назву користувача системи
        # (він завжди починає взаємодію, а, отже,
        # перша дія завжди належить йому)
        if not initiator_name:
            initiator_name = swimline_label

        # змінюємо swinline, якщо керування перейшло до іншого актора
        if last_swimline_name != swimline_label:
            result = result.replace("%PLACEHOLDER%", f"|{swimline_label}|\n    %PLACEHOLDER%")

            # якщо це перша дія, то вказуємо start
            if not last_swimline_name:
                result = result.replace("%PLACEHOLDER%", f"start\n    %PLACEHOLDER%")

            # зберігаємо нове ім'я актора
            last_swimline_name = swimline_label

        # прописуємо поточну дію актора
        result = result.replace("%PLACEHOLDER%", f": {action};\n    %PLACEHOLDER%")

        # якщо є виключні ситуації, додаємо інформацію про них
        if exceptions:
            result = result.replace("%PLACEHOLDER%", f"note right #lightpink\n        <b>{exceptions}</b>\n    end note\n    %PLACEHOLDER%")

    # впенюємося, що взаємодія закінчується на swinline користувача
    if last_swimline_name != initiator_name:
        result = result.replace("%PLACEHOLDER%", f"|{initiator_name}|\n    %PLACEHOLDER%")

    # видаляємо мітку %PLACEHOLDER%
    result = result.replace("%PLACEHOLDER%\n", "")
    return result


def generate_table_with_activity_diagram(raw_table_data):
    table_lines = raw_table_data[:-1]
    activity_line = raw_table_data[-1]

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

    activity_diagram = convert_line_to_activity_diagram(activity_line)

    return "\n".join(formatted_table_lines) + "\n" + activity_diagram


if __name__=="__main__":
    # parse args
    files = []

    write_to_file = AUTO
    write_to_stdout = AUTO
    usecase_formatting = AUTO
    verbose = AUTO
    process_table_files = AUTO
    convert_to_activity_diagram = AUTO
    file_output_path = None

    # 1 pass (argument harvest)
    for n, i in enumerate(sys.argv[1:]):
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

            # дозволити обробку файлів .table
            elif i in ["-t", "--process-table"]:
                process_table_files = YES
            elif i in ["-nt", "--no-process-table"]:
                process_table_files = NO

            # перетворює останню клітинку таблиці в діаграму активностей
            if i in ["-a", "--convert-to-activity-diagram"]:
                convert_to_activity_diagram = YES
            elif i in ["-na", "--no-convert-to-activity-diagram"]:
                convert_to_activity_diagram = NO

            # задає папку, в яку необхідно зберігати конвертовані таблиці
            elif i in ["-d", "--destination"]:
                file_output_path = sys.argv[n+2]
                sys.argv.remove(sys.argv[n+2])

    # 2 pass (filename harvest)
    for i in sys.argv[1:]:
        if not i.startswith("-"):
            if i.endswith(".table") and process_table_files <= AUTO:
                print(f"[Warning]: Excluding {i} to prevent processing of an already processed file (pass --process-table to override this behaviour)")
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

            if convert_to_activity_diagram == YES:
                if verbose == YES:
                    print(f"Converting file {name} to activity diagram\n")

                formatted_table_data = convert_activity_v1(name.rsplit(".", 1)[0], data)
            else:
                formatted_table_data = convert_usecase_v1(name.rsplit(".", 1)[0], data)
        else:
            formatted_table_data = convert_generic_v1(data)

        if write_to_stdout >= AUTO:
            print(formatted_table_data)
        
        if write_to_file > AUTO:
            if file_output_path:
                open(os.path.join(file_output_path, os.path.basename(name)) \
                        + ".table", 'w', encoding = "utf-8") \
                        .write(formatted_table_data+"\n")
            else:
                open(name + ".table", 'w', encoding = "utf-8").write(formatted_table_data+"\n")

        exit(0)

    for no, name in enumerate(files):
        print(f"Converting {no+1:02d}/{len(files)}: {name}")

        data = open(name, encoding = "utf-8").read()

        if usecase_formatting == YES:
            if verbose >= AUTO:
                print(f"Force-formatting {name} as a use-case")
            formatted_table_data = convert_usecase_v1(name.rsplit(".", 1)[0], data)
        elif (name.endswith(".usecase") or name.endswith(".uc")) and usecase_formatting >= AUTO:
            if verbose >= AUTO:
                print(f"Auto-detected use-case in file {name}")

            if convert_to_activity_diagram == YES:
                if verbose == YES:
                    print(f"Converting file {name} to activity diagram\n")

                formatted_table_data = convert_activity_v1(name.rsplit(".", 1)[0], data)
            else:
                formatted_table_data = convert_usecase_v1(name.rsplit(".", 1)[0], data)
        else:
            formatted_table_data = convert_generic_v1(data)

        if write_to_stdout > AUTO:
            print(formatted_table_data)
        
        if write_to_file >= AUTO:
            if file_output_path:
                open(os.path.join(file_output_path, os.path.basename(name)) \
                        + ".table", 'w', encoding = "utf-8") \
                        .write(formatted_table_data+"\n")
            else:
                open(name + ".table", 'w', encoding = "utf-8").write(formatted_table_data+"\n")
