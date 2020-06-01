class FunctionInstruction:

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

    def invoke(self, func_name, arg_amount, code_len):
        code = []
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

    # 根据index获取保存的环境信息，并缓存到D，以便恢复
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
        # 保存参考点return_segment=LCL
        code.append('//保存参考点return_segment，=LCL')
        code.append('@LCL')
        code.append('D=M')
        code.append('@return_segment')
        code.append('M=D')
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

        # ================执行顺序1：
        # 恢复return address
        # 如果callee的ARG没有值，则ARG0和return address地址重合，故先恢复return address，避免被return值覆盖
        code.append('//恢复return address')
        code.extend(self.return_segment(5))
        # 将return address，缓存到R5
        code.append('//将return address，缓存到R5')
        code.append('@R5')
        code.append('M=D')

        # ===============执行顺序2
        # 获取callee返回值
        code.append('//获取callee返回值')
        code.append('@SP')
        code.append('A=M-1')
        code.append('D=M')
        # 把callee返回值保存到R6
        code.append('//把callee返回值保存到R6')
        code.append('@R6')
        code.append('M=D')
        # 恢复caller的SP
        code.append('//恢复caller的SP')
        code.append('@ARG')
        code.append('D=M')
        code.append('@SP')
        code.append('M=D+1')
        # callee返回
        code.append('//callee返回')
        code.append('@R6')
        code.append('D=M')
        code.append('@ARG')
        code.append('A=M')
        code.append('M=D')

        # ===============执行顺序3
        # 恢复ARG
        code.append('//恢复ARG')
        code.extend(self.return_segment(3))
        code.append('@ARG')
        code.append('M=D')

        # ===============执行顺序4
        # 跳转到caller执行环境
        # code.append('//跳转到caller执行环境')
        # code.append('@R5')
        # code.append('0;JMP')
        return code

