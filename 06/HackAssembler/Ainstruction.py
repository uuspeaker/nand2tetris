import re


class Ainstruction:

    sys_ins = {
        'R0': 0,
        'R1': 1,
        'R2': 2,
        'R3': 3,
        'R4': 4,
        'R5': 5,
        'R6': 6,
        'R7': 7,
        'R8': 8,
        'R9': 9,
        'R10': 10,
        'R11': 11,
        'R12': 12,
        'R13': 13,
        'R14': 14,
        'R15': 15,
        'Screen': 16384,
        'KBD': 24576,
    }

    def __init__(self, value):
        self.instruction = value

    def tranlate_aflag(self, instruction):
        ins = instruction.replace('@', '')
        isInt = re.match('^\d+$', ins)
        if isInt:
            return self.get_bin_value(ins)
        else:
            return self.translateVar(ins)

    varAddress = 16

    def translateVar(self, ins):
        global varAddress
        ins_value = self.sys_ins.get(ins, '')
        # print('ins', ins)
        # 未找到地址则添加进去
        if ins_value == '':
            dic_pair = {ins: varAddress}
            # print('dicPair', dicPair)
            self.sys_ins.update(dic_pair)
            varAddress = varAddress + 1
            return self.get_bin_value(varAddress)
        else:
            return self.get_bin_value(ins_value)

    def get_bin_value(self, int_value):
        value = bin(int_value)
        value = value.replace('b', '')
        return value.zfill(16)

