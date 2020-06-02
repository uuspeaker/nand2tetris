class FunctionInstruction:

    ret_no = 0

    # SP指向下一个地址
    def sp_next(self):
        code = []
        code.append('@SP')
        code.append('M=M+1')
        return code

    def set_d_to_sp(self):
        code = []
        code.append('@SP')
        code.append('A=M')
        code.append('M=D')
        return code

    def execute(self, func_name, arg_amount):
        code = []
        # 增加子程序调用标签
        code.append('({})'.format(func_name))
        # 初始化local变量为0，并将SP推进arg_amount个单位
        code.append('//初始化local变量为0，并将SP推进arg_amount个单位')
        for index in range(int(arg_amount)):
            code.append('//初始化local{}'.format(index))
            code.append('@{}'.format(index))
            code.append('D=A')
            code.append('@LCL')
            code.append('A=M+D')
            code.append('M=0')
            code.extend(self.sp_next())
        return code

    def call(self, func_name, arg_amount, code_len):
        code = []
        self.ret_no += 1
        return_label = func_name + '$ret.' + str(self.ret_no)
        # ==========保存caller调用环境
        code.append('//保存caller调用环境')
        # 保存return addr
        code.append('//保存return addr')
        code.append('@{}'.format(return_label))
        # print('return address is ', len(code) + code_len)
        code.append('D=A')
        code.extend(self.set_d_to_sp())
        code.extend(self.sp_next())
        # 保存LCL
        code.append('//保存LCL')
        code.append('@LCL')
        code.append('D=M')
        code.extend(self.set_d_to_sp())
        code.extend(self.sp_next())
        # 保存ARG
        code.append('//保存ARG')
        code.append('@ARG')
        code.append('D=M')
        code.extend(self.set_d_to_sp())
        code.extend(self.sp_next())
        # 保存THIS
        code.append('//保存THIS')
        code.append('@THIS')
        code.append('D=M')
        code.extend(self.set_d_to_sp())
        code.extend(self.sp_next())
        # 保存THAT
        code.append('//保存THAT')
        code.append('@THAT')
        code.append('D=M')
        code.extend(self.set_d_to_sp())
        code.extend(self.sp_next())

        # ==========更新LCL,ARG,THIS,THAT为calle对应值
        code.append('//初始化callee调用环境，更新LCL,ARG')
        # 更新LCL，LCL和SP相同
        code.append('//更新LCL')
        code.append('@SP')
        code.append('D=M')
        code.append('@LCL')
        code.append('M=D')
        # code.extend(self.sp_next())
        # 更新ARG
        code.append('//更新ARG')
        # ARG地址为SP-5-arg_amount
        distance = int(arg_amount) + 5
        code.append('@SP')
        code.append('A=M-1')
        for index in range(distance-1):
            code.append('A=A-1')
        code.append('D=A')
        code.append('@ARG')
        code.append('M=D')
        # 跳转到子程序

        code.append('@{}'.format(func_name))
        code.append('0;JMP')
        code.append('({})'.format(return_label))
        return code

    # 获取return_segment上第index个缓存值（从下往上），保存到D寄存器
    def return_segment(self, index):
        code = []
        code.append('//获取return_segment上第{}个缓存值'.format(index))
        code.append('@return_segment')
        code.append('A=M-1')
        for i in range(index-1):
            code.append('A=A-1')
        code.append('D=M')
        return code

    def return_code(self):
        code = []

        # =============恢复环境信息============
        # 保存参考点地址return_segment
        code.append('//保存参考点地址return_segment')
        code.append('@LCL')
        code.append('D=M')
        code.append('@return_segment')
        code.append('M=D')

        # =============恢复环境：处理和执行顺序无关的THAT, THIS, LCL============
        # 恢复THAT
        code.append('//恢复THAT')
        code.extend(self.return_segment(1))
        code.append('@THAT')
        code.append('M=D')
        # 恢复THIS
        code.append('//恢复THIS')
        code.extend(self.return_segment(2))
        code.append('@THIS')
        code.append('M=D')

        # 恢复LCL
        code.append('//恢复LCL')
        code.extend(self.return_segment(4))
        code.append('@LCL')
        code.append('M=D')

        # =============恢复环境：处理和执行顺序有关的return address, ARG, ============
        # 1，获取return address，保存到临时变量R13
        # 2，获取callee返回值，保存到临时变量R10
        # 3，恢复SP地址，使处于callee环境中ARG的下一个位置
        # 4，把callee返回值R10保存到ARG所在地址
        # 5，恢复ARG
        # 6，代码跳转到R13保存的地址（return address）

        code.append('//获取return address，保存到临时变量R13')
        code.extend(self.return_segment(5))
        # 将return address，缓存到R13
        code.append('@R13')
        code.append('M=D')

        # 获取callee返回值
        code.append('//获取callee返回值，保存到临时变量R10')
        code.append('@SP')
        code.append('A=M-1')
        code.append('D=M')
        # 把callee返回值保存到R10
        code.append('@R10')
        code.append('M=D')
        # 恢复SP
        code.append('//恢复SP地址，使处于callee环境中ARG的下一个位置')
        code.append('@ARG')
        code.append('D=M')
        code.append('@SP')
        code.append('M=D+1')
        # 把callee返回值R10保存到ARG所在地址
        code.append('//把callee返回值R10保存到ARG所在地址')
        code.append('@R10')
        code.append('D=M')
        code.append('@ARG')
        code.append('A=M')
        code.append('M=D')

        # 恢复ARG
        code.append('//恢复ARG')
        code.extend(self.return_segment(3))
        code.append('@ARG')
        code.append('M=D')

        # 代码跳转到R13保存的地址（return address）
        code.append('//代码跳转到R13保存的地址（return address）')
        code.append('@R13')
        code.append('A=M')
        code.append('0;JMP')
        return code

