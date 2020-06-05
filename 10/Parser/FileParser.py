import os
import re
from xml.dom.minidom import Document
from CodeExtractor import CodeExtractor
from JackTokenizer import JackTokenizer

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

    def generate_xml(self):
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

parser = FileParser('D:/program/nand2tetris/10/ArrayTest/Main.jack')
parser.generate_xml()
# parser.test()

