#!/usr/bin/python3

import shutil
import sys
import os

PYTHON_INTERPRETER = sys.executable

def process(target_folder, converter_args):
    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)

    os.mkdir(target_folder)
    os.system(f"{PYTHON_INTERPRETER} convert.py use-cases/* {converter_args} -d {target_folder}/")

    result_file = open(f"{target_folder}.md", "w")

    try:
        for i in os.listdir(target_folder):
            with open(os.path.abspath(f"{target_folder}/{i}")) as f:
                result_file.write(f.read())
                result_file.write("\n")
    except Exception as e:
        print(f"File {target_folder}/{i} has raised exception {e}")

    result_file.close()
