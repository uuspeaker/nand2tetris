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

    def __init__(self, ins_value, ins_index):
        self.instruction = ins_value
        self.index = ins_index

    def tranlate_aflag(self):
        ins = self.instruction.replace('@', '')
        isInt = re.match('^\d+$', ins)
        if isInt:
            return self.get_bin_value(ins)
        else:
            return self.translate_var()



    def translate_var(self):
        ins_value = self.sys_ins.get(self.instruction, '')
        # print('ins', ins)
        # 未找到地址则添加进去
        if ins_value == '':
            dic_pair = {self.instruction: self.index}
            # print('dicPair', dicPair)
            self.sys_ins.update(dic_pair)
            self.index = self.index + 1
            return self.get_bin_value(self.index)
        else:
            return self.get_bin_value(ins_value)

    def get_next_index(self):
        return self.index

    def get_bin_value(self, int_value):
        value = bin(int_value)
        value = value.replace('b', '')
        return value.zfill(16)

