import math

import pandas as pd
from numpy import mean


def read_file(file):
    return pd.read_csv(file, delimiter=",")


def write_file(df, filename):
    df.to_csv(filename, sep=',', encoding='utf-8', index=False, header=None)

def get_system_name(number):
    systems = {
        1: "Reference",
        2: "T2T+pg",
        3: "T2T+pg+cv",
        4: "C2T",
        5: "C2T_char",
        6: "C2T+pg",
        7: "C2T+pg+cv"}
    return systems[number]


def get_system_number(system):
    systems = {
        "Reference": 1,
        "T2T+pg": 2,
        "T2T+pg+cv": 3,
        "C2T": 4,
        "C2T_char": 5,
        "C2T+pg": 6,
        "C2T+pg+cv": 7}
    return systems[system]

def compute_scores(data_frame):
    print(data_frame)
    # "Reference", "T2T+pg", "T2T+pg+cv", "C2T", "C2T_char", "C2T+pg" ,"C2T+pg+cv",
    scores = [[[], [], [], [], [], [], []],  # cover
              [[], [], [], [], [], [], []],  # redun
              [[], [], [], [], [], [], []],  # seman
              [[], [], [], [], [], [], []]]  # gram

    for entries in range(len(data_frame)):  # (number_entries * number_abstracts * 4):
        scores[data_frame.iloc[entries]['question'] - 1][
            get_system_number(data_frame.iloc[entries]['system']) - 1].append(
            data_frame.iloc[entries]['score'])

    return [[mean(sys) for sys in metric] for metric in scores]


def reformat(df):
    ref = [["", "cover.", "non-redun", "semant.", "gramm"]]
    for i in range(len(df[0])):
        sys = [get_system_name(i + 1), df[0][i], df[1][i], df[2][i], df[3][i]]
        ref.append(sys)
    return pd.DataFrame(ref)


if __name__ == '__main__':
    filepath = r"./"
    filename_input = "Human Evaluation Reformated.csv"
    filename_output = "Human Evaluation Results.csv"
    data_frame = read_file(filepath + "\\" + filename_input)
    data_frame = compute_scores(data_frame)
    df = reformat(data_frame)
    write_file(df, filepath + "\\" + filename_output)
