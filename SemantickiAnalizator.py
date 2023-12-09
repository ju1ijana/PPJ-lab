import sys
import copy

data = sys.stdin.read().split("\n")

data.pop()

for index, element in enumerate(data):
    data[index] = element.strip()

dictionary = {}
in_a_loop = 0

for i in range(1, len(data)):
    if data[i - 1] == '<za_petlja>':
        in_a_loop += 1
    if data[i - 1].find('KR_AZ') != -1:
        copy_dict = copy.deepcopy(dictionary)
        for key, value in copy_dict.items():
            for key2, value2 in value.items():
                if key2 == in_a_loop:
                    dictionary[key].pop(key2)
        in_a_loop -= 1
    if data[i - 1] == '<naredba_pridruzivanja>' or data[i - 1].find('KR_ZA') != -1:
        variable = data[i].split(' ')[2]
        row = data[i].split(' ')[1]
        if in_a_loop and data[i - 1].find('KR_ZA') == -1:
            if variable in dictionary:
                continue
        if variable not in dictionary:
            dictionary[variable] = {}
        if in_a_loop not in dictionary[variable]:
            dictionary[variable][in_a_loop] = row
    if data[i - 1] == '<P>' and data[i].find('IDN') != -1:
        var = data[i].split(' ')[2]
        row = data[i].split(' ')[1]
        if var in dictionary:
            if len(list(dictionary[var].keys())) == 0 or dictionary[var][list(dictionary[var].keys())[-1]] == row:
                print("err ", row, " ", var, sep='')
                exit(0)
            print(row, " ", dictionary[var][list(dictionary[var].keys())[-1]], " ", var, sep='')
        else:
            print("err ", row, " ", var, sep='')
            exit(0)


