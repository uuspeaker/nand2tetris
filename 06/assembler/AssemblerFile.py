import os
import re
from Ainstruction import Ainstruction
from Cinstruction import Cinstruction
from CodeExtractor import CodeExtractor

def get_instruction(src):
    extractor = CodeExtractor(src)
    validLines = extractor.get_instruction()
    lines = []
    var_index = 16
    print('validLines', validLines)
    for line in validLines:
        # print('translate', line)
        if line['type'] == 'A':
            ains = Ainstruction(line['value'], var_index)
            lines.append(ains.tranlate_ins())
            var_index = ains.get_next_index()
        elif line['type'] == 'C':
            cins = Cinstruction(line['value'])
            lines.append(cins.translate_ins())

    print('get_instruction line size is ', len(lines))
    print(lines)
    return lines

def generate_bin_file(src):
    path = os.path.dirname(src)
    print('path', path)
    fileName = os.path.basename(src)
    fileName = re.findall(r'(.*)\.', fileName)[0]


    newFileName = fileName + '.hack'
    print('newFileName: ', newFileName)
    lines = get_instruction(src)
    with open(path + '/' + newFileName, 'w+') as file:
        for line in lines:
            file.write(line + '\n')


fileSrc = 'D:/program/nand2tetris/06/add/Add.asm'
# get_valid_lines(fileSrc)
# generate_bin_file('D:/program/nand2tetris/06/add/Add.asm')
# generate_bin_file('D:/program/nand2tetris/06/max/MaxL.asm')
# generate_bin_file('D:/program/nand2tetris/06/max/Max.asm')
# generate_bin_file('D:/program/nand2tetris/06/pong/PongL.asm')
# generate_bin_file('D:/program/nand2tetris/06/pong/Pong.asm')
# generate_bin_file('D:/program/nand2tetris/06/rect/RectL.asm')
generate_bin_file('D:/program/nand2tetris/06/rect/Rect.asm')