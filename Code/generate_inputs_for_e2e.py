import pandas as pd
import io
import json
import numpy as np


def generate_file_system(references_path, system_outputs_path, df, system):
    with io.open(references_path, 'w', encoding="utf-8") as r:
        with io.open(system_outputs_path, 'w', encoding="utf-8") as o:
            for summary, reference in zip(df[df['system'] == system]['summary'],
                                          df[df['system'] == system]['reference']):
                r.write(reference + '\n' * 2)
                o.write(summary + '\n')


def generate_files(ref_path, out_path, systems, df):
    for system in systems:
        generate_file_system(ref_path + system, out_path + system, df, system)
        print('files for ', system, ' were successfully generated')


def get_references(file_path, abstracts_path, isReference=False):
    corrected_company_names = {
        'Simulations Publications Inc.': 'Simulations Publications, Inc.',
        'Whitehaven Cleator and Egremont Railway': 'Whitehaven, Cleator and Egremont Railway',
        'Worcester Bosch Group': 'Worcester, Bosch Group',
        'National Lampoon Inc.': 'National Lampoon, Inc.',
        'Oakley Inc.': 'Oakley, Inc.',
        'Belgian Beer Caf': 'Belgian Beer Caf\u00e9',
        'Artis LLC': 'Artis, LLC'

    }
    # load company names to be used to extract their text
    with open(abstracts_path, 'r') as f:
        corpus = json.load(f)

    df = pd.read_csv(file_path)
    companies = df['company_name']

    abstracts = []

    for c_i, company in enumerate(companies):

        if company in corrected_company_names.keys():
            company = corrected_company_names[company]

        if company in corpus.keys():
            abstract = corpus[company].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            abstracts.append(abstract)

        else:
            abstracts.append(np.nan)
    if isReference:
        df['system'] = ['reference' for i in range(df.size // 2)]
        df['summary'] = abstracts
    df['reference'] = abstracts
    f.close()
    return df


def add_system(df, assignment):
    systems = {
        1: "Reference",
        2: "T2T+pg",
        3: "T2T+pg+cv",
        4: "C2T",
        5: "C2T_char",
        6: "C2T+pg",
        7: "C2T+pg+cv"}
    assignment = [i for line in assignment for i in line if i > 200]
    system = [systems[i // 100] for i in assignment]
    df['system'] = system


if __name__ == '__main__':
    main_path = 'EvaluationFiles/E2E/'
    df = get_references(main_path + 'summaries.csv', main_path + 'abstracts.json')
    assignment = [[101, 325, 618, 712, 329, 127, 408, 229, 218, 405],
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

    add_system(df, assignment)
    df.to_csv(main_path + 'resource_temp.csv', index=False, header=True)

    ref_path = main_path + 'ref_'
    out_path = main_path + 'out_'
    generate_files(ref_path, out_path, set(df['system']), df)

    # for references
    df_reference = get_references(main_path + 'References.csv', main_path + 'abstracts.json', isReference=True)
    print(df_reference)
    df_reference.to_csv(main_path + 'resource_reference_temp.csv', index=False, header=True)
    generate_files(ref_path, out_path, set(df_reference['system']), df_reference)
