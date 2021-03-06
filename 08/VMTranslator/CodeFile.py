import os
import re
from CodeExtractor import CodeExtractor
from ArithmeticInstruction import ArithmeticInstruction
from PushInstruction import PushInstruction
from Instruction import Instruction
from GotoInstruction import GotoInstruction
from FunctionInstruction import FunctionInstruction


class CodeFile:

    def __init__(self, src_value):
        self.src = src_value
        self.codes = []

    def append_code(self, code):
        self.codes.extend(code)

    def get_label_name(self, func_name, label):
        if func_name != '':
            label_name = func_name + '$' + label
        else:
            label_name = label
        return label_name

    def extract_instruction(self):
        extractor = CodeExtractor(self.src)
        instructions = extractor.get_instruction()
        arithmetic_ins = ArithmeticInstruction()
        ins = Instruction()
        push_ins = PushInstruction()
        goto_ins = GotoInstruction()
        func_ins = FunctionInstruction()
        lines = []
        func_name = ''
        file_name = 'default'
        for instruction in instructions:
            # print('translate', instruction)
            self.append_code(ins.comment(instruction))
            if instruction[0] == 'push':
                code = push_ins.push_other(instruction[1], instruction[2], file_name)
            elif instruction[0] == 'pop':
                code = push_ins.pop(instruction[1], instruction[2], file_name)
            elif instruction[0] == 'if-goto':
                label_name = self.get_label_name(func_name, instruction[1])
                code = goto_ins.if_goto(label_name)
            elif instruction[0] == 'goto':
                label_name = self.get_label_name(func_name, instruction[1])
                code = goto_ins.goto(label_name)
            elif instruction[0] == 'label':
                label_name = self.get_label_name(func_name, instruction[1])
                code = goto_ins.label(label_name)
            elif instruction[0] == 'function':
                func_name = instruction[1]
                file_name = func_name.split('.')[0]
                code = func_ins.execute(instruction[1], instruction[2])
            elif instruction[0] == 'call':
                code = func_ins.call(instruction[1], instruction[2], len(self.codes))
            elif instruction[0] == 'return':
                code = func_ins.return_code()
            else:
                code = arithmetic_ins.push_cal(instruction[0])
            self.append_code(code)

        print('翻译后汇编代码行数 ', len(self.codes))

    def generate_code_file(self):
        path = os.path.dirname(self.src)
        print('path', path)
        fileName = os.path.basename(self.src)
        fileName = re.findall(r'(.*)\.', fileName)[0]


        newFileName = fileName + '.asm'
        print('newFileName: ', newFileName)
        self.extract_instruction()
        # print('汇编代码', self.codes)
        with open(path + '/' + newFileName, 'a+') as file:
            for line in self.codes:
                file.write(line + '\n')

# code_file = CodeFile('D:/program/nand2tetris/07/StackArithmetic/SimpleAdd/SimpleAdd.vm')
# code_file = CodeFile('D:/program/nand2tetris/07/StackArithmetic/StackTest/StackTest.vm')
# code_file = CodeFile('D:/program/nand2tetris/07/MemoryAccess/BasicTest/BasicTest.vm')
# code_file = CodeFile('D:/program/nand2tetris/07/MemoryAccess/StaticTest/StaticTest.vm')
# code_file = CodeFile('D:/program/nand2tetris/07/MemoryAccess/PointerTest/PointerTest.vm')
# code_file = CodeFile('D:/program/nand2tetris/08/ProgramFlow/BasicLoop/BasicLoop.vm')
# code_file = CodeFile('D:/program/nand2tetris/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm')
# code_file = CodeFile('D:/program/nand2tetris/08/FunctionCalls/SimpleFunction/SimpleFunction.vm')
# code_file.generate_code_file()