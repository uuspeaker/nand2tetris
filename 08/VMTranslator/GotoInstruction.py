

class GotoInstruction:
    # stack上最后的值a，a>0则goto到label
    def if_goto(self, label_name):
        code = []
        # 获取a值，存到D
        code.append('@SP')
        code.append('M=M-1')
        code.append('A=M')
        code.append('D=M')
        # 判断a>0则跳转
        code.append('@{}'.format(label_name))
        code.append('D;JGT')
        # 若a=-1则跳转（逻辑运算结果TRUE保存-1，FALSE保存0）
        code.append('D=D+1')
        code.append('@{}'.format(label_name))
        code.append('D;JEQ')
        return code

    def goto(self, label_name):
        code = []
        code.append('@{}'.format(label_name))
        code.append('0;JMP')
        return code

    def label(self, label_name):
        code = []
        code.append('({})'.format(label_name))
        return code