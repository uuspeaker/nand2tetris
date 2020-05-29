import os
import re
from CodeExtractor import CodeExtractor
from ArithmeticInstruction import ArithmeticInstruction


class CodeFile:

    def __init__(self, src_value):
        self.src = src_value
        self.codes = []

    def push_param(self, param_type, offset):
        return 1

    def append_code(self, code):
        self.codes.extend(code)

    def extract_instruction(self):
        extractor = CodeExtractor(self.src)
        instructions = extractor.get_instruction()
        arithmetic_ins = ArithmeticInstruction()
        lines = []
        print('instructions', instructions)
        for instruction in instructions:
            # print('translate', line)
            if instruction[0] == 'push':
                if instruction[1] == 'constant':
                    code = arithmetic_ins.push_stack(instruction[2])
                    self.append_code(code)
                else:
                    code = arithmetic_ins.push_param(instruction[1], instruction[2])
                    self.append_code(code)
                    code = arithmetic_ins.push_stack(instruction[2])
                    self.append_code(code)

            elif instruction[0] == 'pop':
                continue
            else:
                code = arithmetic_ins.push_cal(instruction[0])
                self.append_code(code)

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

# code_file = CodeFile('D:/program/nand2tetris/07/StackArithmetic/SimpleAdd/SimpleAdd.vm')
code_file = CodeFile('D:/program/nand2tetris/07/StackArithmetic/StackTest/StackTest.vm')
code_file.generate_code_file()