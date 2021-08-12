import numpy as np
from scipy import stats
import pandas as pd
import io


def compute_correlation(df, metrics, correlation, metric_scores, print_matrix=False):
    n = len(metrics)
    matrix = np.ones((n - 1, n - 1))
    matrix_p = np.ones((n - 1, n - 1))

    output = io.open('Results/correlation/' + metric_scores, 'w', encoding="utf-8")
    for i in range(n - 1):
        for j in range(i + 1, n):
            output.write("(" + metrics[j] + ", " + metrics[i] + ")\n")
            scores1 = df[metrics[i]]
            scores2 = df[metrics[j]]
            if correlation == 'spearman':
                r, p = stats.spearmanr(scores1, scores2)
                if p <= 0.05:
                    output.write('significant !\n')
                output.write('(' + str(r) + ',' + str(p) + ')' + '\n' * 2)
            elif correlation == 'pearson':
                r, p = stats.pearsonr(df[metrics[i]], df[metrics[j]])
            else:
                r, p = stats.kendalltau(df[metrics[i]], df[metrics[j]])
            matrix[j - 1][i] = r
            matrix_p[j - 1][i] = p
    output.close()
    if print_matrix:
        print(matrix)


if __name__ == '__main__':

    main_path = r'./'
    paths = ['excluding_ref.csv', 'including_ref.csv', 'E2E.csv']
    metrics_scores = ['excluding_ref', 'including_ref', 'E2E']
    metrics = ['BLEU', 'NIST', 'METEOR', 'ROUGE_L', 'CIDEr', 'cover.', 'non-redun', 'semant.', 'gramm']
    for p, s in zip(paths, metrics_scores):
        df = pd.read_csv(main_path + p)
        compute_correlation(df, metrics, 'spearman', s, False)
