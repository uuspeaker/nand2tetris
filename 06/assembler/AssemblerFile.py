import os
import re
from Ainstruction import Ainstruction
from Cinstruction import Cinstruction

def get_lines(src):
    with open(src, 'r') as file:
        lines = file.readlines()
        print('getLine line size is ',len(lines))
        # print(lines)
        return lines

def get_valid_lines(src):
    lines = get_lines(src)
    validLines = []
    for line in lines:
        #全为空白则无效
        if re.match(r'^\s*$', line):
            continue
        #//打头则无效
        if re.match(r'^\s*//', line):
            continue
        line = re.sub(r'//.*', '', line)
        line = line.strip()
        validLines.append(line.strip())
    print('get_valid_lines line size is ', len(validLines))
    print(validLines)
    return validLines

def get_instruction(src):
    validLines = get_valid_lines(src)
    lines = []
    index = 0
    var_index = 16
    for line in validLines:
        if re.match(r'^\s*@', line):
            ains = Ainstruction(line, var_index)
            lines.append({'index': index, 'type': 'A', 'value': ains.tranlate_aflag()})
            index = index + 1
            var_index = ains.get_next_index()
        elif re.match(r'^\(.+\)$', line):
            lines.append({'index': index, 'type': 'L', 'value': line})
        else:
            cins = Cinstruction(line)
            lines.append({'index': index, 'type': 'C', 'value': cins.translate_cins()})
            index = index + 1

    print('get_instruction line size is ', len(lines))
    print(lines)
    return lines

def generate_bin_file(src):
    path = os.path.dirname(src)
    print('path', path)
    fileName = os.path.basename(src)
    fileName = re.findall(r'(.*)\.', fileName)[0]

    print('fileName', fileName)
    newFileName = fileName + '.hack'
    lines = get_instruction(src)
    with open(path + '/' + newFileName, 'w+') as file:
        for line in lines:
            file.write(line['value'] + '\n')


fileSrc = 'D:/program/nand2tetris/06/add/Add.asm'
# get_valid_lines(fileSrc)
# generate_bin_file('D:/program/nand2tetris/06/add/Add.asm')
generate_bin_file('D:/program/nand2tetris/06/max/Max.asm')