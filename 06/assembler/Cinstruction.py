import re


class Cinstruction:

    calculateMapping = {
        '0': '101010',
        '1': '111111',
        '-1': '111010',
        'D': '001100',
        'A': '110000',
        'M': '110000',
        '!D': '001101',
        '!A': '110001',
        '!M': '110001',
        '-D': '001111',
        '-A': '110011',
        '-M': '110011',
        'D+1': '011111',
        'A+1': '110111',
        'M+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'D+A': '000010',
        'D+M': '000010',
        'D-A': '010011',
        'D-M': '010011',
        'A-D': '000111',
        'M-D': '000111',
        'D&A': '000000',
        'D&M': '000000',
        'D|A': '010101',
        'D|M': '010101',
    }

    desMapping = {
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111',
    }

    jumpMapping = {
        'D;JGT': '001',
        'D;JEQ': '010',
        'D;JGE': '011',
        'D;JLT': '100',
        'D;JNE': '101',
        'D;JLE': '110',
        '0;JMP': '111',
    }

    def __init__(self, value):
        self.instruction = value.replace(' ', '')

    def get_aflag(self):
        is_match = re.search(r'=.*M', self.instruction)
        if is_match:
            return '1'
        else:
            return '0'

    def get_calculate_flag(self):
        match_value1 = re.findall(r'=(.*)', self.instruction)
        match_value2 = re.findall(r'(.*);', self.instruction)
        # print('matchValue', matchValue)
        if len(match_value1) != 0:
            return self.calculateMapping.get(match_value1[0], '000000')
        elif len(match_value2) != 0:
            return self.calculateMapping.get(match_value2[0], '000000')
        else:
            return '000000'

    def get_destination(self):

        match_value = re.findall(r'(.*)=', self.instruction)
        # print('match_value', match_value)
        if len(match_value) == 0:
            return '000'
        else:
            return self.desMapping.get(match_value[0], '000')

    def get_jump(self):
        return self.jumpMapping.get(self.instruction, '000')

    def translate_cins(self):
        aflag = self.get_aflag()
        calculateFlag = self.get_calculate_flag()
        destination = self.get_destination()
        jump = self.get_jump()
        return '111' + aflag + calculateFlag + destination + jump