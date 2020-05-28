import os
import re
from CodeExtractor import CodeExtractor

class CodeFile:

    start_address = {
        'local': 0,
        'argument': 1
    }

    cal_type = {
        'add': 0,
        'argument': 1
    }

    sp = 256

    def __init__(self, src_value):
        self.src = src_value
        self.codes = []

    def push_param(self, param_type, offset):
        return 1

    def append_code(self, code):
        self.codes.append(code)

    def push_stack(self, value):
        self.sp += 1
        self.append_code('//push constant ' + value)
        self.append_code('@' + value)
        self.append_code('D=A')
        self.append_code('@SP')
        self.append_code('A=M')
        self.append_code('M=D')
        self.append_code('@SP')
        self.append_code('M=M+1')

    def push_cal(self, cal):
        if cal == 'add':
            self.append_code('//add')
            self.append_code('@SP')
            self.append_code('A=M-1')
            self.append_code('D=M')
            self.append_code('A=A-1')
            self.append_code('M=D+M')
            self.append_code('@SP')
            self.append_code('M=M-1')

    def extract_instruction(self):
        extractor = CodeExtractor(self.src)
        instructions = extractor.get_instruction()
        lines = []
        print('instructions', instructions)
        for instruction in instructions:
            # print('translate', line)
            if instruction[0] == 'push':
                if instruction[1] == 'constant':
                    self.push_stack(instruction[2])
                else:
                    self.push_param(instruction[1], instruction[2])
                    self.push_stack(instruction[2])

            elif instruction[0] == 'pop':
                continue
            else:
                self.push_cal(instruction[0])

        print('get_instruction line size is ', len(lines))
        print(lines)
        return lines

    def generate_code_file(self):
        path = os.path.dirname(self.src)
        print('path', path)
        fileName = os.path.basename(self.src)
        fileName = re.findall(r'(.*)\.', fileName)[0]


        newFileName = fileName + '.asm'
        print('newFileName: ', newFileName)
        self.extract_instruction()
        print('self.codes', self.codes)
        with open(path + '/' + newFileName, 'w+') as file:
            for line in self.codes:
                file.write(line + '\n')

code_file = CodeFile('D:/program/nand2tetris/07/StackArithmetic/SimpleAdd/SimpleAdd.vm')
code_file.generate_code_file()