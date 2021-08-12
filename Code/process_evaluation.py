import math

import pandas as pd


def read_file(file):
    return pd.read_csv(file, delimiter=",")


def write_file(df, filename):
    df.to_csv(filename, sep=',', encoding='utf-8', index=False, header=None)


def get_samples():
    return [[101, 325, 618, 712, 329, 127, 408, 229, 218, 405],
            [107, 225, 703, 209, 604, 727, 720, 103, 115, 406],
            [522, 418, 729, 730, 214, 113, 421, 324, 509, 511],
            [428, 617, 412, 129, 713, 224, 706, 226, 510, 321],
            [230, 311, 717, 416, 328, 211, 422, 322, 724, 119],
            [629, 710, 407, 715, 306, 417, 512, 217, 413, 123],
            [104, 409, 516, 121, 118, 725, 202, 722, 714, 502],
            [610, 206, 425, 317, 401, 307, 308, 607, 728, 126],
            [602, 507, 303, 220, 125, 124, 319, 527, 205, 525],
            [403, 122, 216, 210, 701, 702, 313, 711, 613, 611],
            [519, 514, 207, 314, 304, 223, 521, 228, 117, 623],
            [621, 523, 323, 615, 625, 330, 404, 204, 520, 419],
            [628, 630, 212, 619, 718, 120, 616, 111, 201, 726],
            [603, 624, 410, 524, 213, 608, 501, 215, 208, 506],
            [316, 626, 423, 708, 114, 112, 312, 612, 605, 222],
            [305, 518, 106, 721, 203, 709, 723, 326, 128, 109],
            [309, 526, 302, 705, 517, 116, 105, 327, 108, 528],
            [219, 402, 110, 620, 320, 505, 318, 414, 310, 513],
            [530, 315, 606, 515, 503, 529, 430, 508, 609, 415]]


def get_participant_from_all(file_index):
    participants = {
        1: "WR",
        2: "CR",
        3: "SR",
        4: "EH",
        5: "VK",
        6: "SL",
        7: "KM",
        8: "TE",
        9: "BS",
        10: "ZYY",
        11: "YZY",
        12: "JN",
        13: "WL",
        14: "ZY",
        15: "CY",
        16: "TRC",
        17: "JBY",
        18: "CYY",
        19: "ZTY"}
    return participants[file_index]


def get_participant_from_all_reversed(part):
    participants = {
        1: "WR",
        2: "CR",
        3: "SR",
        4: "EH",
        5: "VK",
        6: "SL",
        7: "KM",
        8: "TE",
        9: "BS",
        10: "ZYY",
        11: "YZY",
        12: "JN",
        13: "WL",
        14: "ZY",
        15: "CY",
        16: "TRC",
        17: "JBY",
        18: "CYY",
        19: "ZTY"}
    new_sys = {v: k for k, v in participants.items()}
    return new_sys[part]


def get_system(question_number, file, part):
    systems = {
        1: "Reference",
        2: "T2T+pg",
        3: "T2T+pg+cv",
        4: "C2T",
        5: "C2T_char",
        6: "C2T+pg",
        7: "C2T+pg+cv"}

    samples = get_samples()[get_participant_from_all_reversed(part) - 1]
    return systems[int(str(samples[math.ceil((question_number + 1) / 4) - 1])[0])]


def get_reverse_system(number):
    systems = {
        1: "Reference",
        2: "T2T+pg",
        3: "T2T+pg+cv",
        4: "C2T",
        5: "C2T_char",
        6: "C2T+pg",
        7: "C2T+pg+cv"}
    new_sys = {v: k for k, v in systems.items()}
    return new_sys[number]


def convert_number_to_question():
    return {0: "covererage",
            1: "redundancy",
            2: "semantic",
            3: "grammar"}


def get_index(question_number, file, part):
    samples = get_samples()[get_participant_from_all_reversed(part) - 1]
    ind = str(samples[math.ceil((question_number + 1) / 4) - 1])[1:]

    # cut leading  0's
    if len(ind) > 1:
        if ind[0] == "0":
            return ind[1:]
    return ind


def reformat_file(data_frame, number_entries):
    columns = ["participant", "date", "score", "index", "system", "question", "name"]
    new_data = [columns]
    all_scores = []

    for file in range(number_entries):

        data_row = data_frame.iloc[file]
        file_index = data_row[1]
        ratings = [data_row[j] for j in range(2, len(data_row))]
        # participant, date
        part, date = get_participant_from_all(file_index), data_row[0]

        scores = [part]
        for q in range(len(ratings)):
            # participant, date, score, index, question, system, name
            row = [part, date, ratings[q], get_index(q, file, part), get_system(q, file, part), (q % 4) + 1,
                   convert_number_to_question()[q % 4]]
            new_data.append(row)
            scores.append(int(get_reverse_system(get_system(q, file, part))) * 100 + int(get_index(q, file, part)))
        all_scores.append(scores)

    for i in all_scores:
        print(list(dict.fromkeys(i)))
    new_data_frame = pd.DataFrame(new_data)

    return new_data_frame


if __name__ == '__main__':
    filepath = r"./"
    filename_input = "Human Evaluation Export.csv"
    filename_output = "Human Evaluation Reformated.csv"
    number_participants = 19
    data_frame = read_file(filepath + "\\" + filename_input)
    data_frame = reformat_file(data_frame, number_participants)
    write_file(data_frame, filepath + "\\" + filename_output)
