import os
import re
from xml.dom.minidom import Document
from CodeExtractor import CodeExtractor
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from JackCompiler import JackCompiler

class FileParser:

    def __init__(self, src_value):
        self.src = src_value
        self.codes = []


    def extract_instruction(self):
        extractor = CodeExtractor(self.src)
        instructions = extractor.get_instruction()
        self.codes.append('<tokens>')
        for instruction in instructions:
            tokenizer = JackTokenizer(instruction)
            # print(len(tokenizer.get_tokens()),instruction)
            self.codes.extend(tokenizer.get_tokens())
        self.codes.append('</tokens>')

    def generate_token(self):
        path = os.path.dirname(self.src)
        print('path', path)
        fileName = os.path.basename(self.src)
        fileName = re.findall(r'(.*)\.', fileName)[0]
        newFileName = fileName + '2.xml'
        # print('newFileName: ', newFileName)
        self.extract_instruction()
        # print('汇编代码', self.codes)
        with open(path + '/' + newFileName, 'w+') as file:
            for line in self.codes:
                file.write(line + '\n')

    def generate_grammer(self):
        path = os.path.dirname(self.src)

        fileName = os.path.basename(self.src)
        fileName = re.findall(r'(.*)\.', fileName)[0]
        print('翻译文件', path + '/' + fileName + '.xml')
        newFileName = fileName + '.xml'
        print('翻译后文件: ', newFileName)
        self.extract_instruction()
        codes = self.codes[1: len(self.codes) - 1]
        compiler = CompilationEngine(codes)
        xml_code = compiler.compile()
        # print('汇编代码', self.codes)
        with open(path + '/' + newFileName, 'w+') as file:
            for line in xml_code:
                file.write(line + '\n')

    def generate_vm(self):
        path = os.path.dirname(self.src)

        fileName = os.path.basename(self.src)
        fileName = re.findall(r'(.*)\.', fileName)[0]
        print('开始翻译文件', path + '/' + fileName + '.xml')
        newFileName = fileName + '.vm'

        compiler = JackCompiler(self.src)
        vm_code = compiler.compile()
        # print('汇编代码', self.codes)
        with open(path + '/' + newFileName, 'w+') as file:
            for line in vm_code:
                file.write(line + '\n')
        print('翻译完成，文件名称: ', newFileName)

    def test(self):
        for char in 'abc':
            print(ord(char))


# parser = FileParser('D:/program/nand2tetris/11/Seven/Main.xml')
# parser = FileParser('D:/program/nand2tetris/11/ConvertToBin/Main.xml')
# parser = FileParser('D:/program/nand2tetris/11/Square/Main.xml')
# parser = FileParser('D:/program/nand2tetris/11/Square/Square.xml')
# parser = FileParser('D:/program/nand2tetris/11/Square/SquareGame.xml')
# # parser.generate_vm()
# parser.test()



