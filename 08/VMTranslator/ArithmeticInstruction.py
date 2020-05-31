
class ArithmeticInstruction:

    lable_index = 0

    jump_dic = {
        'eq': 'JEQ',
        'lt': 'JLT',
        'le': 'JLE',
        'ne': 'JNE',
        'gt': 'JGT',
        'ge': 'JGE',
    }

    def append_code(self, code):
        self.codes.append(code)

    def generate_label(self):
        self.lable_index += 1
        return 'lable' + str(self.lable_index)

    def generate_logic(self, param):
        code = []
        jump_flag = self.jump_dic.get(param)
        lable1 = self.generate_label()
        lable2 = self.generate_label()

        code.append('@SP')
        code.append('A=M-1')
        code.append('D=M')
        code.append('A=A-1')
        code.append('D=M-D')

        code.append('@{}'.format(lable1))
        code.append('D;{}'.format(jump_flag))

        code.append('@SP')
        code.append('A=M-1')
        code.append('A=A-1')
        code.append('M=0')
        code.append('@{}'.format(lable2))
        code.append('0;JMP')

        code.append('({})'.format(lable1))
        code.append('@SP')
        code.append('A=M-1')
        code.append('A=A-1')
        code.append('M=-1')

        code.append('({})'.format(lable2))
        code.append('@SP')
        code.append('M=M-1')
        return code

    def push_cal(self, cal):
        code = []
        code.append('//=========={}=========='.format(cal))
        if cal == 'add':
            code.append('@SP')
            code.append('A=M-1')
            code.append('D=M')
            code.append('A=A-1')
            code.append('M=D+M')
            code.append('@SP')
            code.append('M=M-1')
        elif cal == 'sub':
            code.append('@SP')
            code.append('A=M-1')
            code.append('D=M')
            code.append('A=A-1')
            code.append('M=M-D')
            code.append('@SP')
            code.append('M=M-1')
        elif cal == 'and':
            code.append('@SP')
            code.append('A=M-1')
            code.append('D=M')
            code.append('A=A-1')
            code.append('M=D&M')
            code.append('@SP')
            code.append('M=M-1')
        elif cal == 'or':
            code.append('@SP')
            code.append('A=M-1')
            code.append('D=M')
            code.append('A=A-1')
            code.append('M=D|M')
            code.append('@SP')
            code.append('M=M-1')
        elif cal == 'not':
            code.append('@SP')
            code.append('A=M-1')
            code.append('M=!M')
        elif cal == 'neg':
            code.append('@SP')
            code.append('A=M-1')
            code.append('M=-M')
        elif self.jump_dic.get(cal, 'not_found') != 'not_found':
            code.extend(self.generate_logic(cal))

        return code