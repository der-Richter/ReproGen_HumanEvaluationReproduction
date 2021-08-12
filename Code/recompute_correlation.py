import pandas as pd
from scipy import stats


def read_file(path):
    return pd.read_csv(path, index_col=0, header=0)


def compute_correlation(df):
    al = []
    for q in df.columns:
        al.append(q)
        for q2 in df.columns:
            if q2 not in al:
                scores1 = df[q][:]
                scores2 = df[q2][:]

                print(q, ' VS ', q2)

                print(stats.spearmanr(scores1, scores2))


if __name__ == '__main__':
    df = read_file(r'./Human Evaluation Results Qader.csv')
    compute_correlation(df)
