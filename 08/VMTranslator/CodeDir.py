import os
import re
from CodeFile import CodeFile

def set_param(file, param, value):
    file.write('@{}\n'.format(value))
    file.write('D=A\n')
    file.write('@{}\n'.format(param))
    file.write('M=D\n')

def append_boot_strap(src,sp):
    with open(src, 'w+') as file:
        set_param(file, 'SP', sp)
        # set_param(file, 'LCL', 300)
        # set_param(file, 'ARG', 400)
        file.write('@Sys.init\n')
        file.write('0;JMP\n')


def extracte_code_dir(dir, file_name, sp):
    vm_file_src = dir + file_name + '.vm'
    asm_file_src = dir + file_name + '.asm'
    append_boot_strap(asm_file_src, sp)
    print('target_file_src', vm_file_src)
    with open(vm_file_src, 'w+') as file_target:

        for root, dirs, files in os.walk(dir):
            # print(root, dirs, files)
            for name in files:
                if re.match(r'.*vm$', name):
                    file_src = os.path.join(root, name)
                    # print('file_src', file_src)
                    with open(file_src, 'r') as file_source:
                        for line in file_source:
                            file_target.write(line)

    code_file = CodeFile(vm_file_src)
    code_file.generate_code_file()
    # os.remove(vm_file_src)


extracte_code_dir('D:/program/nand2tetris/08/FunctionCalls/FibonacciElement/', 'FibonacciElement', 261)
# extracte_code_dir('D:/program/nand2tetris/08/FunctionCalls/NestedCall/', 'NestedCall', 261)
# extracte_code_dir('D:/program/nand2tetris/08/FunctionCalls/StaticsTest/', 'StaticsTest', 261)