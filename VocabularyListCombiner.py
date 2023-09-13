# coding=utf-8
import copy

FILE_1 = r'/THE/PATH/file_1.txt'
FILE_2 = r'/THE/PATH/file_2.txt'
SAVE_DIR = r'/THE/PATH/result.txt'

def read_file(file_dir):
    """Read the English of a vocabulary file."""
    # Input:
    #   file_dir: the directory of a file
    # Output:
    #   content: [[word, whole line]]
    content = []
    with open(file_dir, "r") as file:
        read_line = file.read().split('\n')
        for i, line in enumerate(read_line):
            vocabulary = line.rsplit('\t', 1)
            if line == '\n':
                continue
            elif len(content) > 0 and read_line[i-1] != '':
                content[-1][1] = content[-1][1] + ';' + line
            else:
                content.append([vocabulary[0], line])
        # for line in file:
        #     vocabulary = line.rsplit('\t', 1)
        #     if line == '\n':
        #         continue
        #     elif vocabulary[0][0] in ['\\', '[']:
        #         continue
        #     elif ',' in vocabulary[0]:
        #         continue
        #     elif '.' in vocabulary[0]:
        #         continue
        #     elif ';' in vocabulary[0]:
        #         continue
        #     elif '\n' in vocabulary[0]:
        #         continue
        #     else:
        #         # content.append([vocabulary[0], vocabulary[1].decode('utf-8')])
        #         content.append([vocabulary[0], line.decode('utf-8')])
    return content

def save_file(content, wa='a'):
    """Save something to files."""
    # Input:
    #   content: list or string

    with open(SAVE_DIR, wa) as file:
        for c in content:
            file.write(c + '\n')
            file.write('\n')

def compare(list_1, list_2):
    """Compare the content of two lists and
    returns the word that does not exists in the shorter list."""
    # Input:
    #   list_1: [word, meaning]
    #   list_2: [word, meaning]
    # Output:
    #   diff_voc: [[prev string, target string]]

    if len(list_1) > len(list_2):
        larger_list = list_1
        smaller_list = copy.deepcopy(list_2)
    else:
        larger_list = list_2
        smaller_list = copy.deepcopy(list_1)

    # all_voc = [x[1] for x in smaller_list] # [string]
    diff_voc = [] # [string]
    for i, voc in enumerate(larger_list):
        exist = False
        for j, exist_voc in enumerate(smaller_list):
            if voc[0].lower() == exist_voc[0].lower():
                exist = True
                break
            else:
                continue

        if exist is False:
            diff_voc.append([larger_list[i-1][0], voc[1]])
        else:
            del smaller_list[j]
    return diff_voc

def arrange(list_1, list_2, extra):
    """Insert extra words in to the smaller word list."""
    # Input:
    #   list_1: [[word, whole line]]
    #   list_2: [[word, whole line]]
    #   extra: [[prev word, target word]]
    # Output:
    #   all_voc: [whole line]

    if len(list_1) > len(list_2):
        larger_list = list_1
        smaller_list = list_2
    else:
        larger_list = list_2
        smaller_list = list_1

    all_voc = [x[1] for x in smaller_list]
    idx = 0
    while extra != []: #  and len(extra) > 461
        for i in range(idx, len(all_voc)):
            if all_voc[i].rsplit('\t')[0].lower() == extra[0][0].lower():
                all_voc.insert(i+1, extra[0][1])
                idx = i - 2
                break
        if len(all_voc) == i + 1:
            idx = 0
            continue
        elif  extra[0][1] == all_voc[i+1]:
            del extra[0]
    return all_voc

def show_result(result):
    """Print the result one by one."""
    # Input:
    #   result: [[prev string, target string]]
    for words in result:
        print(words)

if __name__ == '__main__':
    save_file('', 'w')
    word_lists_1 = read_file(FILE_1)
    word_lists_2 = read_file(FILE_2)
    print(len(word_lists_1), len(word_lists_2))
    compare_result = compare(word_lists_1, word_lists_2)
    print(len(compare_result))
    # show_result(compare_result)
    whole_vocabulary = arrange(word_lists_1, word_lists_2, compare_result)
    print(len(whole_vocabulary))
    save_file(whole_vocabulary)
