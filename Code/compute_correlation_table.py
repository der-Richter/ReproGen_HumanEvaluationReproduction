from scipy import stats
import pandas as pd
import io


def compute(path_ori, path_rep, output_path):
    df_ori = pd.read_csv(path_ori, index_col=0, header=0)
    df_rep = pd.read_csv(path_rep, index_col=0, header=0)
    #print(df_rep)
    output = io.open(output_path, 'w', encoding="utf-8")


    for c in df_ori.columns:
         output.write(c+'\n')
         output.write('spearman: '+'----'+str(stats.spearmanr(df_rep[c],df_ori[c]))+'\n')
         output.write('pearson: '+'----'+str(stats.pearsonr(df_rep[c],df_ori[c]))+'\n')
         output.write('kendall: '+'----'+str(stats.kendalltau(df_rep[c],df_ori[c]))+'\n'*2)

    for i in range(df_rep.shape[0]):
        raw_name = df_rep.index[i]
        output.write(raw_name+'\n')
        output.write('spearman: '+'----'+str(stats.spearmanr(df_rep.iloc[i],df_ori.iloc[i]))+'\n')
        output.write('pearson: '+'----'+str(stats.pearsonr(df_rep.iloc[i],df_ori.iloc[i]))+'\n')
        output.write('kendall: '+'----'+str(stats.kendalltau(df_rep.iloc[i],df_ori.iloc[i]))+'\n'*2)

    output.write('all'+'\n')
    output.write('spearman: '+'----'+str(stats.spearmanr(df_ori.values.flatten(),df_rep.values.flatten()))+'\n')
    output.write('pearson: '+'----'+str(stats.pearsonr(df_ori.values.flatten(),df_rep.values.flatten()))+'\n')
    output.write('kendall: '+'----'+str(stats.kendalltau(df_ori.values.flatten(),df_rep.values.flatten()))+'\n'*2)







if __name__ == '__main__':
    path_rep = 'Files/Human Evaluation Results.csv'
    path_ori = 'Files/db_table.csv'
    output_path = 'Files/correlation_tables.txt'
    compute(path_ori,path_rep,output_path)
