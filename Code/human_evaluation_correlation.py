import pandas as pd
from scipy import stats


def read_file(file):
    return pd.read_csv(file, delimiter=",", index_col=0)


def write_file(df, filename):
    df.to_csv(filename, sep=',', encoding='utf-8', index=False, header=None)


def compute_cortrelation_overall(df_us, df_their):
    systems = ["reference",
               "C2T",
               "C2T_char",
               "C2T+pg",
               "C2T+pg+cv",
               "T2T+pg",
               "T2T+pg+cv"]
    metrics = ["cover.", "non-redun", "semant.", "gramm"]
    us = []
    their = []

    for sys in systems:
        for metric in metrics:
            us.append(df_us.loc[sys].loc[metric])
            their.append(df_their.loc[sys].loc[metric])

    return stats.spearmanr(us, their)


if __name__ == '__main__':
    filepath = r"./"
    filename_input_ours = "Human Evaluation Results.csv"
    filename_input_theirs = "qader_human_evaluation_results.csv"  # TODO: you need the original socres here
    filename_output = "human_evaluation_correlation.csv"
    df_us = read_file(filepath + "\\" + filename_input_ours)
    df_their = read_file(filepath + "\\" + filename_input_theirs)
    correlation = compute_cortrelation_overall(df_us, df_their)
    print(correlation)
