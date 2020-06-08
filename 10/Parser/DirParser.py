import os
import re
from FileParser import  FileParser

def extracte_token(dir):
    for root, dirs, files in os.walk(dir):
        for name in files:
            if re.match(r'.*jack$', name):
                file_src = os.path.join(root, name)
                parser = FileParser(file_src)
                parser.generate_token()

def extracte_grammer(dir):
    for root, dirs, files in os.walk(dir):
        for name in files:
            if re.match(r'.*jack$', name):
                file_src = os.path.join(root, name)
                parser = FileParser(file_src)
                parser.generate_grammer()


# extracte_token('D:/program/nand2tetris/10/ArrayTest/')
# extracte_token('D:/program/nand2tetris/10/ExpressionLessSquare/')
# extracte_token('D:/program/nand2tetris/10/Square/')


extracte_grammer('D:/program/nand2tetris/10/ArrayTest/')