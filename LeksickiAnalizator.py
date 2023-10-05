import sys
import re

data = sys.stdin.read().split("\n")

dictionary = {'za': 'KR_ZA', 'az': 'KR_AZ', 'od': 'KR_OD', 'do': 'KR_DO', '(': 'L_ZAGRADA', ')': 'D_ZAGRADA',
              '=': 'OP_PRIDRUZI', '+': 'OP_PLUS', '-': 'OP_MINUS', '*': 'OP_PUTA', '/': 'OP_DIJELI'}
line_count = 0

def read_line(line, line_count):
    for read in line.strip().split(' '):
        if read != '':
            used = False
            if read == '//':
                return
            if len(read) >= 2:
                if read[0:2] == '//':
                    return
            if read.strip().isnumeric():
                print('BROJ ' + str(line_count) + ' ' + read.strip())
                continue
            for read_d in dictionary:
                if read == read_d and not used:
                    print(dictionary[read_d] + ' ' + str(line_count) + ' ' + read_d)
                    used = True

            if not used:
                new_string = ''
                for i in range(len(read)):
                    if read[i] in dictionary:
                        new_string += ' ' + read[i] + ' '
                    else:
                        new_string += read[i]
                new_string = re.sub(r'\s+', ' ', new_string)
                if read[0].isnumeric() and len(new_string) == len(read):
                    read_line(read[0] + ' ' + read[1:], line_count)
                elif len(new_string) == len(read):
                    print('IDN ' + str(line_count) + ' ' + read.strip())
                else:
                    read_line(new_string, line_count)


for line in data:
    line_count += 1
    read_line(line, line_count)
