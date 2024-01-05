import re
import sys
import copy

sys.stdout = open('a.frisc', 'w')

content = ['MD_SGN\tMOVE 0, R6', '\tXOR R0, 0, R0', '\tJP_P MD_TST1', '\tXOR R0, -1, R0', '\tADD R0, 1, R0', '\tMOVE 1, R6', 'MD_TST1 XOR R1, 0, R1', '\tJP_P MD_SGNR', '\tXOR R1, -1, R1', '\tADD R1, 1, R1', '\tXOR R6, 1, R6', 'MD_SGNR RET', 'MD_INIT POP R4 ; MD_INIT ret addr', '\tPOP R3 ; M/D ret addr', '\tPOP R1 ; op2', '\tPOP R0 ; op1', '\tCALL MD_SGN', '\tMOVE 0, R2 ; init rezultata', '\tPUSH R4 ; MD_INIT ret addr', '\tRET', 'MD_RET  XOR R6, 0, R6 ; predznak?', '\tJP_Z MD_RET1', '\tXOR R2, -1, R2 ; promijeni predznak', '\tADD R2, 1, R2', 'MD_RET1 POP R4 ; MD_RET ret addr', '\tPUSH R2 ; rezultat', '\tPUSH R3 ; M/D ret addr', '\tPUSH R4 ; MD_RET ret addr', '\tRET', 'MUL \tCALL MD_INIT', '\tXOR R1, 0, R1', '\tJP_Z MUL_RET ; op2 == 0', '\tSUB R1, 1, R1', 'MUL_1 \tADD R2, R0, R2', '\tSUB R1, 1, R1', '\tJP_NN MUL_1 ; >= 0?', 'MUL_RET CALL MD_RET', '\tRET', 'DIV \tCALL MD_INIT', '\tXOR R1, 0, R1', '\tJP_Z DIV_RET ; op2 == 0', 'DIV_1 \tADD R2, 1, R2', '\tSUB R0, R1, R0', '\tJP_NN DIV_1', '\tSUB R2, 1, R2', 'DIV_RET CALL MD_RET', '\tRET']

print("\tMOVE 40000, R7 ; init stog\n")

print_variables = []

data = sys.stdin.read().split("\n")
#data = ['<program>', ' <lista_naredbi>', '  <naredba>', '   <naredba_pridruzivanja>', '    IDN 1 n', '    OP_PRIDRUZI 1 =', '    <E>', '     <T>', '      <P>', '       BROJ 1 12', '      <T_lista>', '       $', '     <E_lista>', '      $', '  <lista_naredbi>', '   <naredba>', '    <naredba_pridruzivanja>', '     IDN 2 rez', '     OP_PRIDRUZI 2 =', '     <E>', '      <T>', '       <P>', '        BROJ 2 0', '       <T_lista>', '        $', '      <E_lista>', '       $', '   <lista_naredbi>', '    <naredba>', '     <za_petlja>', '      KR_ZA 3 za', '      IDN 3 i', '      KR_OD 3 od', '      <E>', '       <T>', '        <P>', '         BROJ 3 1', '        <T_lista>', '         $', '       <E_lista>', '        $', '      KR_DO 3 do', '      <E>', '       <T>', '        <P>', '         IDN 3 n', '        <T_lista>', '         $', '       <E_lista>', '        $', '      <lista_naredbi>', '       <naredba>', '        <naredba_pridruzivanja>', '         IDN 4 rez', '         OP_PRIDRUZI 4 =', '         <E>', '          <T>', '           <P>', '            IDN 4 rez', '           <T_lista>', '            $', '          <E_lista>', '           OP_PLUS 4 +', '           <E>', '            <T>', '             <P>', '              IDN 4 i', '             <T_lista>', '              $', '            <E_lista>', '             $', '       <lista_naredbi>', '        $', '      KR_AZ 5 az', '    <lista_naredbi>', '     $']

data.pop()

for index, element in enumerate(data):
    data[index] = element.strip()
in_a_loop = 0

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

# preuzeto sa https://stackoverflow.com/questions/41164797/method-to-convert-infix-to-reverse-polish-notationpostfix
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

def declare(rpn):
    if len(rpn.split(' ')) == 1:  # imamo samo slučaj pridruživanja konstante varijabli
        print('\tMOVE %D ' + rpn + ', R0', sep='')
        print('\tPUSH R0')
        print('\tPOP R0')
        print('\tSTORE R0, (' + var + str(in_a_loop) + ')', sep='')

    else:
        evaluate(rpn)
        print('\tPOP R0')
        print('\tSTORE R0, (' + var + str(in_a_loop) + ')', sep='')


def prepare_param_num(param):
    print('\tMOVE %D ' + param + ', R0', sep='')
    print('\tPUSH R0')
    return

def prepare_param_var(param):
    print('\tLOAD R0, (' + param + str(in_a_loop) + ')')
    print('\tPUSH R0')
    return

# preuzeto sa https://www.geeksforgeeks.org/evaluate-the-value-of-an-arithmetic-expression-in-reverse-polish-notation-in-python/
def evaluate(expression):
    expression = expression.split()
    stack = []

    for ele in expression:
        if ele not in '/*+-':
            stack.append(ele)
        else:
            right = stack.pop()
            left = stack.pop()

            if left.isdigit():
                prepare_param_num(left)
            else:
                if left != 'result':
                    prepare_param_var(left)

            if right.isdigit():
                prepare_param_num(right)
            else:
                if right != 'result':
                    prepare_param_var(right)

            if ele == '+':
                print('\tPOP R0')
                print('\tPOP R1')
                print('\tADD R0, R1, R2')
                print('\tPUSH R2')
                stack.append('result')
            elif ele == '-':
                print('\tPOP R0')
                print('\tPOP R1')
                print('\tSUB R1, R0, R2')
                print('\tPUSH R2')
                stack.append('result')
            elif ele == '*':
                print('\tCALL MUL')
                stack.append('result')
            elif ele == '/':
                print('\tCALL DIV')
                stack.append('result')


extract_pj()

dictionary = {}

dos = {} # dict za spremanje do vrijednosti petlje -> ključ je do_ (_ je in_a_loop), a vrijednost je string npr i * i (za j od 0 do i*i)


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
    if data[i - 1] == '<naredba_pridruzivanja>':
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
                declare(rpn)
            # fakat ne znam
            if in_a_loop > min(dictionary[var].keys()):
                print("koristenje varijable", var)

    if data[i - 1].find('KR_ZA') != -1:
        var = data[i].split(' ')[2]
        row = data[i].split(' ')[1]
        if in_a_loop and data[i - 1].find('KR_ZA') == -1:
            if var in dictionary:
                continue
        if var not in dictionary:
            dictionary[var] = {}
        if in_a_loop not in dictionary[var]:
            dictionary[var][in_a_loop] = row
            print_variables.append(var + str(in_a_loop) + ' DW 0')
            rpn = toRpn(pj[int(row) - 1].split('od')[1].strip().split('do')[0].strip())
            declare(rpn)

            print_variables.append('do' + str(in_a_loop) + ' DW 0')
            dos['do' + str(in_a_loop)] = pj[int(row) - 1].split('do')[1].strip() # spremamo do vrijednost za kasnije


print('\tLOAD R6, (rez0)')
print('\tHALT\n')

for v in print_variables:
    print(v)

print('\n')
for c in content:
    print(c)

sys.stdout.close()

