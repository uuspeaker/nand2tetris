import os
import re
from CodeFile import CodeFile

def extracte_code_dir(dir):
    for root, dirs, files in os.walk(dir):
        # print(root, dirs, files)
        for name in files:
            if re.match(r'.*vm$', name):
                file_src = os.path.join(root, name)
                print('file_src', file_src)
                code_file = CodeFile(file_src)
                code_file.generate_code_file()

extracte_code_dir('D:/program/nand2tetris/08/ProgramFlow/BasicLoop/')