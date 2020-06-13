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

def extracte_vm(dir):
    for root, dirs, files in os.walk(dir):
        for name in files:
            if re.match(r'.*xml$', name):
                file_src = os.path.join(root, name)
                print(file_src)
                parser = FileParser(file_src)
                parser.generate_vm()


# extracte_token('D:/program/nand2tetris/10/ArrayTest/')
# extracte_token('D:/program/nand2tetris/10/ExpressionLessSquare/')
# extracte_token('D:/program/nand2tetris/10/Square/')


# extracte_grammer('D:/program/nand2tetris/10/ArrayTest/')
# extracte_grammer('D:/program/nand2tetris/10/ExpressionLessSquare/')
# extracte_vm('D:/program/nand2tetris/11/Seven/')
# extracte_vm('D:/program/nand2tetris/11/ConvertToBin/')
# extracte_vm('D:/program/nand2tetris/11/Square/')
extracte_vm('D:/program/nand2tetris/11/Average/')