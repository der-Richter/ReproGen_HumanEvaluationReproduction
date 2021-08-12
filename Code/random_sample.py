import random


def list_generation(number_of_systems=7, number_of_abstarcts=30):
    list_of_all_abstarcts = []
    for sys in range(1, number_of_systems + 1):
        for abst in range(1, number_of_abstarcts + 1):
            list_of_all_abstarcts.append(sys * 100 + abst)
    return list_of_all_abstarcts


def sort_in(list_of_all_abstracts, number_of_lists=19, items_per_list=10):
    resuling_lists = []

    for i in range(1, number_of_lists):
        single_list = []
        for j in range(0, items_per_list):
            element = random.choice(list_of_all_abstracts)
            single_list.append(element)
            list_of_all_abstracts.remove(element)
        resuling_lists.append(single_list)

    return resuling_lists


if __name__ == '__main__':
    all_abstracts = list_generation()
    results = sort_in(all_abstracts)

    for i in results:
        print(i)
