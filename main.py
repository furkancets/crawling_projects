from utils import src_list, input_selection
import os

def script_selection():
    return input_selection(some_list=src_list())


if __name__ == "__main__":
    os.system(f"""python src/{script_selection()}""")
