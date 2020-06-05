import os
import re
from FileParser import  FileParser

def extracte_code_dir(dir):
    for root, dirs, files in os.walk(dir):
        for name in files:
            if re.match(r'.*jack$', name):
                file_src = os.path.join(root, name)
                parser = FileParser(file_src)
                parser.generate_xml()


extracte_code_dir('D:/program/nand2tetris/10/ArrayTest/')
