import re
import sys
import copy

sys.stdout = open('a.frisc', 'w')

with open('helper.txt', 'r') as functions:
    content = functions.read()

print("\tMOVE 40000, R7 ; init stog\n")



print_variables = []

data = ['<program>', ' <lista_naredbi>', '  <naredba>', '   <naredba_pridruzivanja>', '    IDN 1 rez', '    OP_PRIDRUZI 1 =', '    <E>', '     <T>', '      <P>', '       BROJ 1 17', '      <T_lista>', '       OP_DIJELI 1 /', '       <T>', '        <P>', '         BROJ 1 8', '        <T_lista>', '         $', '     <E_lista>', '      $', '  <lista_naredbi>', '   $']

data.pop()

for index, element in enumerate(data):
    data[index] = element.strip()

# izdvajanje pj kôda iz sintaksnog stabla
pj = ['']
def extract_pj():
    global pj, data
    prev = 1
    for line in data:
        if line.find('<') == -1 and line != '$':
            if int(line.split(' ')[1]) != prev:
                prev = int(line.split(' ')[1])
                pj.append('')
            pj[-1] += line.split(' ')[2]

def toRpn(infixStr):
    tokens = re.split(r' *([\+\-\*\^/]) *', infixStr)
    tokens = [t for t in reversed(tokens) if t != '']
    precs = {'+': 0, '-': 0, '/': 1, '*': 1, '^': 2}

    def toRpn2(tokens, minprec):
        rpn = tokens.pop()
        while len(tokens) > 0:
            prec = precs[tokens[-1]]
            if prec < minprec:
                break
            op = tokens.pop()
            arg2 = toRpn2(tokens, prec + 1)
            rpn += " " + arg2 + " " + op
        return rpn

    return toRpn2(tokens, 0)

def evaluate(expression):
    expression = expression.split()
    stack = []

    for ele in expression:
        if ele not in '/*+-':
            stack.append(int(ele))
        else:
            right = stack.pop()
            left = stack.pop()

            print('\tMOVE %D ' + str(left) + ', R0', sep='')
            print('\tPUSH R0')
            print('\tMOVE %D ' + str(right) + ', R0', sep='')
            print('\tPUSH R0')

            if ele == '+':
                print('\tPOP R0')
                print('\tPOP R1')
                print('\tADD R0, R1, R2')
                print('\tPUSH R2')
                stack.append(left + right)
            elif ele == '-':
                print('\tPOP R0')
                print('\tPOP R1')
                print('\tSUB R1, R0, R2')
                print('\tPUSH R2')
                stack.append(left - right)
            elif ele == '*':
                print('\tCALL MUL')
                stack.append(left * right)
            elif ele == '/':
                print('\tCALL DIV')
                stack.append(int(left / right))
    return stack.pop()


extract_pj()

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
        var = data[i].split(' ')[2]
        row = data[i].split(' ')[1]
        if in_a_loop and data[i - 1].find('KR_ZA') == -1:
            if var in dictionary:
                continue
        if var not in dictionary:
            dictionary[var] = {}
        if in_a_loop not in dictionary[var]:
            dictionary[var][in_a_loop] = row
            # prepoznaje se da se u ovom trenu deklarira varijabla
            print_variables.append(var + str(in_a_loop) + ' DW 0')
            if bool(re.match(r'^-\d+$', pj[int(row) - 1].split('=')[1].strip())):
                print('\tMOVE %D ' + pj[int(row) - 1].split('=')[1].strip()[1:] + ', R0', sep='')
                print('\tPUSH R0')
                print('\tPOP R0')
                print('\tMOVE %D 0, R1')
                print('\tSUB R1, R0, R2')
                print('\tPUSH R2')
                print('\tPOP R0')
                print('\tSTORE R0, (' + var + str(in_a_loop) + ')', sep='')

            else:
                rpn = toRpn(pj[int(row) - 1].split('=')[1].strip())

                if len(rpn.split(' ')) == 1:   # imamo samo slučaj pridruživanja konstante varijabli
                    # MOVE %D 3, R0
                    # PUSH R0
                    print('\tMOVE %D ' + rpn + ', R0', sep='')
                    print('\tPUSH R0')
                    # POP R0
                    # STORE R0, (V0)
                    print('\tPOP R0')
                    print('\tSTORE R0, (' + var + str(in_a_loop) + ')', sep='')

                else:
                    evaluate(rpn)
                    print('\tPOP R0')
                    print('\tSTORE R0, (' + var + str(in_a_loop) + ')', sep='')

#LOAD R6, (V1)
print('\tLOAD R6, (rez0)')

print('\tHALT\n')

for v in print_variables:
    print(v)

print('\n' + content)

sys.stdout.close()


