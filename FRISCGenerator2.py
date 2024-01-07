import re
import sys

sys.stdout = open('a.frisc', 'w')

content = ['MD_SGN\tMOVE 0, R6', '\tXOR R0, 0, R0', '\tJP_P MD_TST1', '\tXOR R0, -1, R0', '\tADD R0, 1, R0',
           '\tMOVE 1, R6', 'MD_TST1 XOR R1, 0, R1', '\tJP_P MD_SGNR', '\tXOR R1, -1, R1', '\tADD R1, 1, R1',
           '\tXOR R6, 1, R6', 'MD_SGNR RET', 'MD_INIT POP R4 ; MD_INIT ret addr', '\tPOP R3 ; M/D ret addr',
           '\tPOP R1 ; op2', '\tPOP R0 ; op1', '\tCALL MD_SGN', '\tMOVE 0, R2 ; init rezultata',
           '\tPUSH R4 ; MD_INIT ret addr', '\tRET', 'MD_RET  XOR R6, 0, R6 ; predznak?', '\tJP_Z MD_RET1',
           '\tXOR R2, -1, R2 ; promijeni predznak', '\tADD R2, 1, R2', 'MD_RET1 POP R4 ; MD_RET ret addr',
           '\tPUSH R2 ; rezultat', '\tPUSH R3 ; M/D ret addr', '\tPUSH R4 ; MD_RET ret addr', '\tRET',
           'MUL \tCALL MD_INIT', '\tXOR R1, 0, R1', '\tJP_Z MUL_RET ; op2 == 0', '\tSUB R1, 1, R1',
           'MUL_1 \tADD R2, R0, R2', '\tSUB R1, 1, R1', '\tJP_NN MUL_1 ; >= 0?', 'MUL_RET CALL MD_RET', '\tRET',
           'DIV \tCALL MD_INIT', '\tXOR R1, 0, R1', '\tJP_Z DIV_RET ; op2 == 0', 'DIV_1 \tADD R2, 1, R2',
           '\tSUB R0, R1, R0', '\tJP_NN DIV_1', '\tSUB R2, 1, R2', 'DIV_RET CALL MD_RET', '\tRET']

print("\tMOVE 40000, R7 ; init stog\n")

print_variables = []

data = sys.stdin.read().split("\n")
#data = ['<program>', ' <lista_naredbi>', '  <naredba>', '   <naredba_pridruzivanja>', '    IDN 1 n', '    OP_PRIDRUZI 1 =', '    <E>', '     <T>', '      <P>', '       BROJ 1 10', '      <T_lista>', '       $', '     <E_lista>', '      $', '  <lista_naredbi>', '   <naredba>', '    <naredba_pridruzivanja>', '     IDN 2 rez', '     OP_PRIDRUZI 2 =', '     <E>', '      <T>', '       <P>', '        BROJ 2 0', '       <T_lista>', '        $', '      <E_lista>', '       $', '   <lista_naredbi>', '    <naredba>', '     <za_petlja>', '      KR_ZA 3 za', '      IDN 3 n', '      KR_OD 3 od', '      <E>', '       <T>', '        <P>', '         BROJ 3 1', '        <T_lista>', '         $', '       <E_lista>', '        $', '      KR_DO 3 do', '      <E>', '       <T>', '        <P>', '         BROJ 3 5', '        <T_lista>', '         $', '       <E_lista>', '        $', '      <lista_naredbi>', '       <naredba>', '        <naredba_pridruzivanja>', '         IDN 4 rez', '         OP_PRIDRUZI 4 =', '         <E>', '          <T>', '           <P>', '            IDN 4 rez', '           <T_lista>', '            $', '          <E_lista>', '           OP_PLUS 4 +', '           <E>', '            <T>', '             <P>', '              IDN 4 n', '             <T_lista>', '              $', '            <E_lista>', '             $', '       <lista_naredbi>', '        $', '      KR_AZ 5 az', '    <lista_naredbi>', '     <naredba>', '      <naredba_pridruzivanja>', '       IDN 6 rez', '       OP_PRIDRUZI 6 =', '       <E>', '        <T>', '         <P>', '          IDN 6 rez', '         <T_lista>', '          $', '        <E_lista>', '         OP_PLUS 6 +', '         <E>', '          <T>', '           <P>', '            IDN 6 n', '           <T_lista>', '            $', '          <E_lista>', '           $', '     <lista_naredbi>', '      <naredba>', '       <za_petlja>', '        KR_ZA 7 za', '        IDN 7 n', '        KR_OD 7 od', '        <E>', '         <T>', '          <P>', '           BROJ 7 1', '          <T_lista>', '           $', '         <E_lista>', '          $', '        KR_DO 7 do', '        <E>', '         <T>', '          <P>', '           BROJ 7 5', '          <T_lista>', '           $', '         <E_lista>', '          $', '        <lista_naredbi>', '         <naredba>', '          <naredba_pridruzivanja>', '           IDN 8 rez', '           OP_PRIDRUZI 8 =', '           <E>', '            <T>', '             <P>', '              IDN 8 rez', '             <T_lista>', '              $', '            <E_lista>', '             OP_PLUS 8 +', '             <E>', '              <T>', '               <P>', '                IDN 8 n', '               <T_lista>', '                $', '              <E_lista>', '               $', '         <lista_naredbi>', '          $', '        KR_AZ 9 az', '      <lista_naredbi>', '       $']

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
        print('\tSTORE R0, (' + find_version_of_var(var) + ')', sep='')

    else:
        evaluate(rpn)
        print('\tPOP R0')
        print('\tSTORE R0, (' + find_version_of_var(var) + ')', sep='')


def prepare_param_num(param):
    print('\tMOVE %D ' + param + ', R0', sep='')
    print('\tPUSH R0')
    return


def prepare_param_num_neg(param):
    print('\tMOVE %D ' + param[1:] + ', R0', sep='')
    print('\tPUSH R0')
    print('\tPOP R0')
    print('\tMOVE %D 0, R1')
    print('\tSUB R1, R0, R2')
    print('\tPUSH R2')
    print('\tPOP R0')
    print('\tSTORE R0, (' + find_version_of_var(var) + ')', sep='')
    return


def prepare_param_var(var):
    print('\tLOAD R0, (' + find_version_of_var(var) + ')')
    print('\tPUSH R0')
    return

def find_version_of_var(var):
    versions = [element for element in variables if element.startswith(var)]
    return max(versions)

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
                if right == 'result' and not (left == right and right == 'result'):
                    print('\tSUB R0, R1, R2')
                else:
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

dos = {}  # dict za spremanje do vrijednosti petlje -> ključ je do_ (_ je in_a_loop), a vrijednost je string npr i * i (za j od 0 do i*i)

variables = []  # za spremanje varijabli koje su deklarirane

counters = []

used_loop_names = []

for i, line in enumerate(pj):
    if line.find('za') != -1:
        in_a_loop += 1
        var = line.split('od')[0].strip().split('za')[1].strip()
        variables.append(var + str(in_a_loop))
        counters.append(var + str(in_a_loop))
        print_variables.append(
            var + str(in_a_loop) + ' DW 0')  # ovo je brojač petlje, deklarira se (početna je vrijednost od)
        od = line.split('od')[1].strip().split('do')[0].strip()
        if bool(re.match(r'^-\d+$', od)):  # varijabla se deklarira samo kao npr. -2
            prepare_param_num_neg(od)
        else:  # deklaracija varijable
            rpn = toRpn(od)
            if len(rpn) == 1 and not rpn.isdigit():
                print('\tLOAD R0, (' + find_version_of_var(od) + ')')
                print('\tSTORE R0, (' + counters[-1] + ')')
            else:
                declare(rpn)

        i = 0
        while 'L' + str(in_a_loop + i) in used_loop_names:
            i += 1
        loop_name = 'L' + str(in_a_loop + i)
        used_loop_names.append(loop_name)
        print(loop_name, end='')
        dos['do' + str(in_a_loop)] = [line.split('do')[1].strip(), loop_name]  # spremamo za kasnije

    if line.find('az') != -1:
        # pronađi counter trenutne petlje i povećaj ga
        counter = [c for c in counters if c.endswith(str(in_a_loop))][0]
        print('\tLOAD R0, (' + counter + ')')
        print('\tADD R0, 1, R0')
        print('\tSTORE R0, (' + counter + ')')
        # računamo vrijednost do i računamo da se nalazi na stogu
        do, loop_name = dos['do' + str(in_a_loop)]
        if bool(re.match(r'^-\d+$', do)):  # imamo "do -1"
            print('\tMOVE %D ' + do[1:] + ', R0', sep='')
            print('\tPUSH R0')
            print('\tPOP R0')
            print('\tMOVE %D 0, R1')
            print('\tSUB R1, R0, R2')
            print('\tPUSH R2')
        else:
            rpn = toRpn(do)
            if len(rpn.split(' ')) == 1 and rpn.isdigit():
                print('\tMOVE %D ' + rpn + ', R0', sep='')
                print('\tPUSH R0')
            else:
                if len(rpn) == 1:
                    print('\tLOAD R0, (' + find_version_of_var(do) + ')')
                    print('\tPUSH R0')
                else:
                    evaluate(rpn)
        # na stog stavimo i brojač
        print('\tLOAD R0, (' + counter + ')')
        print('\tPOP R1')
        # uvjetni skok
        print('\tCMP R0, R1')
        print('\tJP_SLE ' + loop_name)

        variables = [item for item in variables if not item.endswith(str(in_a_loop))]
        in_a_loop -= 1
    if line.find('=') != -1:
        var = line.split('=')[0].strip()
        if not any(element.startswith(var) for element in variables):  # deklaracija varijable
            variables.append(var + str(in_a_loop))
            print_variables.append(var + str(in_a_loop) + ' DW 0')
            if bool(re.match(r'^-\d+$', line.split('=')[1].strip())):  # varijabla se deklarira samo kao npr. -2
                prepare_param_num_neg(line.split('=')[1].strip())
            else:  # deklaracija varijable
                rpn = toRpn(line.split('=')[1].strip())
                declare(rpn)
        else:  # varijabla deklarirana, dodajemo joj novu vrijednost
            rpn = toRpn(line.split('=')[1].strip())
            evaluate(rpn)
            print('\tPOP R0')
            print('\tSTORE R0, (' + [element for element in variables if element.startswith(var)][-1] + ')', sep='')

print('\tLOAD R6, (rez0)')
print('\tHALT\n')

for v in set(print_variables):
    print(v)

print('\n')
for c in content:
    print(c)

sys.stdout.close()
