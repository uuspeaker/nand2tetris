
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

    def generate_label(self, label):
        self.lable_index += 1
        return label + str(self.lable_index)

    def generate_logic(self, param):
        code = []
        jump_flag = self.jump_dic.get(param)
        label_true = self.generate_label('sys.label_true')
        label_end = self.generate_label('sys.label_end')

        code.append('//获取b值')
        code.append('@SP')
        code.append('A=M-1')
        code.append('D=M')
        code.append('//计算a-b的值')
        code.append('A=A-1')
        code.append('D=M-D')
        code.append('//若a-b {} 0, 则跳转到{}'.format(param, label_true))
        code.append('@{}'.format(label_true))
        code.append('D;{}'.format(jump_flag))
        code.append('//否则继续执行下面代码')
        code.append('@SP')
        code.append('A=M-1')
        code.append('A=A-1')
        code.append('M=0')
        code.append('@{}'.format(label_end))
        code.append('0;JMP')

        code.append('({})'.format(label_true))
        code.append('@SP')
        code.append('A=M-1')
        code.append('A=A-1')
        code.append('M=-1')

        code.append('({})'.format(label_end))
        code.append('@SP')
        code.append('M=M-1')
        return code

    def push_cal(self, cal):
        code = []
        # code.append('//=========={}=========='.format(cal))
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
        code.append('//运算结束')
        return code