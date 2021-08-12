import numpy as np
from scipy import stats
import pandas as pd
import io
def compute_correlation(score_path, metrics, output_path):
    df = pd.read_csv(score_path)
    n = len(metrics)

    output = io.open(output_path, 'w', encoding="utf-8")

    for i in range(n - 1):
        for j in range(i + 1, n):
            output.write("("+metrics[j]+", "+metrics[i]+")\n")
            scores1 = df[metrics[i]]
            scores2 = df[metrics[j]]

            r, p = stats.spearmanr(scores1, scores2)
            if p<=0.05:
                output.write('significant !\n')
            output.write('('+str(r)+','+str(p)+')'+'\n'*2)

    output.close()




if __name__ == '__main__':
    score_path = 'Files/scores.csv'
    output_path = 'Files/Correlation Scores.txt'
    metrics = ['BLEU','NIST','METEOR','ROUGE_L','CIDEr','cover.','non-redun','semant.','gramm']
    compute_correlation(score_path, metrics, output_path)
