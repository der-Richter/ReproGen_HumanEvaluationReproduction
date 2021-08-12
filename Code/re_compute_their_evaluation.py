import pandas as pd
from numpy import mean
from scipy import stats


def read_file(file):
    return pd.read_csv(file, delimiter=",")


def write_file(df, filename):
    df.to_csv(filename, sep=',', encoding='utf-8', index=False, header=None)


def get_system_name(number):
    systems = {
        1: "reference",
        2: "C2T",
        3: "C2T_char",
        4: "C2T+pg",
        5: "C2T+pg+cv",
        6: "T2T+pg",
        7: "T2T+pg+cv"
    }
    return systems[number]


def get_system_number(system):
    systems = {
        "reference": 1,
        "C2T": 2,
        "C2T_char": 3,
        "C2T+pg": 4,
        "C2T+pg+cv": 5,
        "T2T+pg": 6,
        "T2T+pg+cv": 7
    }
    return systems[system]


def compute_scores(data_frame):
    # print(data_frame)
    # "Reference", "T2T+pg", "T2T+pg+cv", "C2T", "C2T_char", "C2T+pg" ,"C2T+pg+cv",
    scores = [[[], [], [], [], [], [], []],  # cover
              [[], [], [], [], [], [], []],  # redun
              [[], [], [], [], [], [], []],  # seman
              [[], [], [], [], [], [], []]]  # gram

    for entries in range(len(data_frame)):  # (number_entries * number_abstracts * 4):
        scores[data_frame.iloc[entries]['question'] - 1][
            get_system_number(data_frame.iloc[entries]['system']) - 1].append(
            data_frame.iloc[entries]['score'])

    return [["{:.1f}".format(mean(sys)) for sys in metric] for metric in scores]


def reformat(df):
    ref = [["", "cover.", "non-redun", "semant.", "gramm"]]
    for i in range(len(df[0])):
        sys = [get_system_name(i + 1), df[0][i], df[1][i], df[2][i], df[3][i]]
        ref.append(sys)
    return pd.DataFrame(ref)


def correlate(data):
    # made this complex in order to check in each step if the ordering of the data is still right.
    scores = [[], [], [], []]  # each list will contain all ratings for one question, sorted by the system and the index

    for sys_index in range(1, 8):  # for each system
        sys = get_system_name(sys_index)
        res_sys = data.loc[data['system'] == sys]  # get all data of that system
        for question_index in range(1, 5):  # for every question
            # here we have all entries of one question for one particular system
            res_sys_question = res_sys.loc[data['question'] == question_index]

            # here i combine the resulst but also integrate some information to check for the right ordering
            sys = [x for x in res_sys_question['system']]
            ind = [x for x in res_sys_question['index']]
            score = [x for x in res_sys_question['score']]
            q = [x for x in res_sys_question['question']]
            scores[question_index - 1].append(list(zip(sys, ind, q, score)))

    # here i start recombining the list scores, which has this structure:
    # List<Questions>(List<Systems>(Tuples<sys, index, question, score>))
    scores_combined = [[], [], [], []]
    for question_index in range(len(scores)):
        tmp = []
        for i in scores[question_index]:
            tmp.extend(i)
        scores_combined[question_index] = tmp

    print(
        f"cov:red {stats.spearmanr([entry[3] for entry in scores_combined[0]], [entry[3] for entry in scores_combined[1]])}")
    print(
        f"cov:sem {stats.spearmanr([entry[3] for entry in scores_combined[0]], [entry[3] for entry in scores_combined[2]])}")
    print(
        f"cov:gram {stats.spearmanr([entry[3] for entry in scores_combined[0]], [entry[3] for entry in scores_combined[3]])}")
    print(
        f"red:sem {stats.spearmanr([entry[3] for entry in scores_combined[1]], [entry[3] for entry in scores_combined[2]])}")
    print(
        f"red:gram {stats.spearmanr([entry[3] for entry in scores_combined[1]], [entry[3] for entry in scores_combined[3]])}")
    print(
        f"sem:gram {stats.spearmanr([entry[3] for entry in scores_combined[2]], [entry[3] for entry in scores_combined[3]])}")

    return


if __name__ == '__main__':
    filepath_input = r"./"
    filename_input = ""  # TODO their evaluation data
    filename_output = "Human Evaluation Results Qader.csv"
    filepath_output = r"./"
    data_frame = read_file(filepath_input + "\\" + filename_input)
    data_frame = compute_scores(data_frame)
    df = reformat(data_frame)
    write_file(df, filepath_output + "\\" + filename_output)

    filepath_input_second = r"./"
    ours = r"./Human Evaluation Reformated.csv"
    theirs = r"./"  # TODO their original database of the results
    correlate(read_file(theirs))
