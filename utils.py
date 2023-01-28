import os

def src_list():

    selection_list = []

    path = os.getcwd()

    sub_path = [i for i in os.walk(path) if "src" in i[0]]

    for i in sub_path:
        for j in i[2]:
            if (("__") or ("cpython")) not in j:
                selection_list.append(j)

    return selection_list

def input_selection(some_list):

    print(f"""Please keep in mind desired crawler number""")

    new_list = sorted(some_list)

    for i, j in enumerate(new_list):

        print(i, j)

    x = int(input())

    print(new_list[x])

    return new_list[x]
