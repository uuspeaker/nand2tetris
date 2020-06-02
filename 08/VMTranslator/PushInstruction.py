
class PushInstruction:
    param_dic = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
    }

    def push_D_to_stack(self):
        code = []
        code.append('@SP')
        code.append('A=M')
        code.append('M=D')
        code.append('@SP')
        code.append('M=M+1')
        return code

    def push_other(self, param_type, offset):
        code = []
        address_name = self.param_dic.get(param_type, '')
        # code.append('//push {} {}'.format(param_type, offset))
        if param_type == 'temp':
            address = int(offset) + 5
            code.append('@{}'.format(address))
            code.append('D=M')
        elif param_type == 'static':
            code.append('@Foo.{}'.format(offset))
            code.append('D=M')
        elif param_type == 'constant':
            code.append('@' + offset)
            code.append('D=A')
        elif param_type == 'pointer' and offset == '0':
            code.append('@R3')
            code.append('D=M')
        elif param_type == 'pointer' and offset == '1':
            code.append('@R4')
            code.append('D=M')
        else:
            code.append('@{}'.format(offset))
            code.append('D=A')
            code.append('@{}'.format(address_name))
            code.append('A=D+M')
            code.append('D=M')
        code.extend(self.push_D_to_stack())
        return code

    def pop(self, param_type, offset):
        code = []
        address_name = self.param_dic.get(param_type, '')
        # code.append('//pop {} {}'.format(param_type, offset))
        # 获取当前stack顶端的值
        code.append('@SP')
        code.append('A=M-1')
        code.append('D=M')
        # 把值存储到临时地址R11
        code.append('@R11')
        code.append('M=D')
        # 找到要存储区段的地址，将地址存到临时地址R12
        if param_type == 'temp':
            address = int(offset) + 5
            code.append('@{}'.format(address))
            code.append('D=A')
        elif param_type == 'static':
            code.append('@Foo.{}'.format(offset))
            code.append('D=A')
        elif param_type == 'pointer' and offset == '0':
            code.append('@R3')
            code.append('D=A')
        elif param_type == 'pointer' and offset == '1':
            code.append('@R4')
            code.append('D=A')
        else:
            code.append('@{}'.format(offset))
            code.append('D=A')
            code.append('@{}'.format(address_name))
            code.append('D=D+M')
        code.append('@R12')
        code.append('M=D')
        # 将此临时值R11存到区段地址R12
        code.append('@R11')
        code.append('D=M')
        code.append('@R12')
        code.append('A=M')
        code.append('M=D')
        # 当前stack指向前一个地址
        code.append('@SP')
        code.append('M=M-1')
        return code