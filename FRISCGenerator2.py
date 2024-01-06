import re
import sys
import copy

sys.stdout = open('a.frisc', 'w')

content = ['MD_SGN\tMOVE 0, R6', '\tXOR R0, 0, R0', '\tJP_P MD_TST1', '\tXOR R0, -1, R0', '\tADD R0, 1, R0', '\tMOVE 1, R6', 'MD_TST1 XOR R1, 0, R1', '\tJP_P MD_SGNR', '\tXOR R1, -1, R1', '\tADD R1, 1, R1', '\tXOR R6, 1, R6', 'MD_SGNR RET', 'MD_INIT POP R4 ; MD_INIT ret addr', '\tPOP R3 ; M/D ret addr', '\tPOP R1 ; op2', '\tPOP R0 ; op1', '\tCALL MD_SGN', '\tMOVE 0, R2 ; init rezultata', '\tPUSH R4 ; MD_INIT ret addr', '\tRET', 'MD_RET  XOR R6, 0, R6 ; predznak?', '\tJP_Z MD_RET1', '\tXOR R2, -1, R2 ; promijeni predznak', '\tADD R2, 1, R2', 'MD_RET1 POP R4 ; MD_RET ret addr', '\tPUSH R2 ; rezultat', '\tPUSH R3 ; M/D ret addr', '\tPUSH R4 ; MD_RET ret addr', '\tRET', 'MUL \tCALL MD_INIT', '\tXOR R1, 0, R1', '\tJP_Z MUL_RET ; op2 == 0', '\tSUB R1, 1, R1', 'MUL_1 \tADD R2, R0, R2', '\tSUB R1, 1, R1', '\tJP_NN MUL_1 ; >= 0?', 'MUL_RET CALL MD_RET', '\tRET', 'DIV \tCALL MD_INIT', '\tXOR R1, 0, R1', '\tJP_Z DIV_RET ; op2 == 0', 'DIV_1 \tADD R2, 1, R2', '\tSUB R0, R1, R0', '\tJP_NN DIV_1', '\tSUB R2, 1, R2', 'DIV_RET CALL MD_RET', '\tRET']

print("\tMOVE 40000, R7 ; init stog\n")

print_variables = []

data = sys.stdin.read().split("\n")
#data = ['<program>', ' <lista_naredbi>', '  <naredba>', '   <naredba_pridruzivanja>', '    IDN 1 x', '    OP_PRIDRUZI 1 =', '    <E>', '     <T>', '      <P>', '       BROJ 1 13', '      <T_lista>', '       $', '     <E_lista>', '      $', '  <lista_naredbi>', '   <naredba>', '    <naredba_pridruzivanja>', '     IDN 2 y', '     OP_PRIDRUZI 2 =', '     <E>', '      <T>', '       <P>', '        BROJ 2 14', '       <T_lista>', '        $', '      <E_lista>', '       $', '   <lista_naredbi>', '    <naredba>', '     <naredba_pridruzivanja>', '      IDN 3 z', '      OP_PRIDRUZI 3 =', '      <E>', '       <T>', '        <P>', '         IDN 3 x', '        <T_lista>', '         $', '       <E_lista>', '        OP_PLUS 3 +', '        <E>', '         <T>', '          <P>', '           IDN 3 y', '          <T_lista>', '           $', '         <E_lista>', '          OP_MINUS 3 -', '          <E>', '           <T>', '            <P>', '             BROJ 3 13', '            <T_lista>', '             $', '           <E_lista>', '            $', '    <lista_naredbi>', '     <naredba>', '      <naredba_pridruzivanja>', '       IDN 4 w', '       OP_PRIDRUZI 4 =', '       <E>', '        <T>', '         <P>', '          IDN 4 x', '         <T_lista>', '          $', '        <E_lista>', '         OP_PLUS 4 +', '         <E>', '          <T>', '           <P>', '            IDN 4 y', '           <T_lista>', '            $', '          <E_lista>', '           OP_PLUS 4 +', '           <E>', '            <T>', '             <P>', '              IDN 4 z', '             <T_lista>', '              $', '            <E_lista>', '             $', '     <lista_naredbi>', '      <naredba>', '       <naredba_pridruzivanja>', '        IDN 5 rez', '        OP_PRIDRUZI 5 =', '        <E>', '         <T>', '          <P>', '           BROJ 5 2', '          <T_lista>', '           OP_PUTA 5 *', '           <T>', '            <P>', '             IDN 5 x', '            <T_lista>', '             $', '         <E_lista>', '          OP_PLUS 5 +', '          <E>', '           <T>', '            <P>', '             IDN 5 y', '            <T_lista>', '             $', '           <E_lista>', '            OP_PLUS 5 +', '            <E>', '             <T>', '              <P>', '               IDN 5 z', '              <T_lista>', '               $', '             <E_lista>', '              OP_PLUS 5 +', '              <E>', '               <T>', '                <P>', '                 IDN 5 w', '                <T_lista>', '                 $', '               <E_lista>', '                $', '      <lista_naredbi>', '       <naredba>', '        <naredba_pridruzivanja>', '         IDN 6 rez', '         OP_PRIDRUZI 6 =', '         <E>', '          <T>', '           <P>', '            IDN 6 rez', '           <T_lista>', '            $', '          <E_lista>', '           OP_MINUS 6 -', '           <E>', '            <T>', '             <P>', '              BROJ 6 2', '             <T_lista>', '              OP_PUTA 6 *', '              <T>', '               <P>', '                IDN 6 x', '               <T_lista>', '                $', '            <E_lista>', '             $', '       <lista_naredbi>', '        <naredba>', '         <naredba_pridruzivanja>', '          IDN 7 rez', '          OP_PRIDRUZI 7 =', '          <E>', '           <T>', '            <P>', '             IDN 7 rez', '            <T_lista>', '             $', '           <E_lista>', '            OP_MINUS 7 -', '            <E>', '             <T>', '              <P>', '               IDN 7 y', '              <T_lista>', '               $', '             <E_lista>', '              $', '        <lista_naredbi>', '         <naredba>', '          <naredba_pridruzivanja>', '           IDN 8 rez', '           OP_PRIDRUZI 8 =', '           <E>', '            <T>', '             <P>', '              IDN 8 rez', '             <T_lista>', '              $', '            <E_lista>', '             OP_MINUS 8 -', '             <E>', '              <T>', '               <P>', '                IDN 8 z', '               <T_lista>', '                $', '              <E_lista>', '               $', '         <lista_naredbi>', '          <naredba>', '           <naredba_pridruzivanja>', '            IDN 9 rez', '            OP_PRIDRUZI 9 =', '            <E>', '             <T>', '              <P>', '               IDN 9 rez', '              <T_lista>', '               $', '             <E_lista>', '              OP_PLUS 9 +', '              <E>', '               <T>', '                <P>', '                 IDN 9 w', '                <T_lista>', '                 $', '               <E_lista>', '                $', '          <lista_naredbi>', '           $']

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
        #print(stack)
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
                #print("left:", left, "right:", right)
                print('\tPOP R0')
                print('\tPOP R1')
                if right == 'result':
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

dictionary = {}

dos = {} # dict za spremanje do vrijednosti petlje -> ključ je do_ (_ je in_a_loop), a vrijednost je string npr i * i (za j od 0 do i*i)

variables = []

for i, line in enumerate(pj):
    if line.find('za') != -1:
        in_a_loop += 1
    if line.find('az') != -1:
        in_a_loop -= 1
    if line.find('=') != -1:
        var = line.split('=')[0].strip()
        if var + str(in_a_loop) not in variables:   # deklaracija varijable
            variables.append(var + str(in_a_loop))
            print_variables.append(var + str(in_a_loop) + ' DW 0')
            if bool(re.match(r'^-\d+$', line.split('=')[1].strip())):   # varijabla se deklarira samo kao npr. -2
                print('\tMOVE %D ' + line.split('=')[1].strip()[1:] + ', R0', sep='')
                print('\tPUSH R0')
                print('\tPOP R0')
                print('\tMOVE %D 0, R1')
                print('\tSUB R1, R0, R2')
                print('\tPUSH R2')
                print('\tPOP R0')
                print('\tSTORE R0, (' + var + str(in_a_loop) + ')', sep='')
            else:   # deklaracija varijable
                rpn = toRpn(line.split('=')[1].strip())
                declare(rpn)
        else: # varijabla deklarirana, dodajemo joj novu vrijednost
            rpn = toRpn(line.split('=')[1].strip())
            evaluate(rpn)
            print('\tPOP R0')
            print('\tSTORE R0, (' + var + str(in_a_loop) + ')', sep='')

print('\tLOAD R6, (rez0)')
print('\tHALT\n')

for v in print_variables:
    print(v)

print('\n')
for c in content:
    print(c)

sys.stdout.close()

