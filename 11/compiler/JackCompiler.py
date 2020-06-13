from bs4 import BeautifulSoup
from SymbolTable import SymbolTable
from ExpressionCompiler import ExpressionCompiler
from Log import logger
import re



class JackCompiler:

    while_label_index = 0
    if_label_index = 0

    def __init__(self, src):
        self.src = src
        self.vm_code = []
        with open(self.src, 'r') as file:
            self.soup = BeautifulSoup(file, 'xml')
            # 原文档树中内容前后各加了一个空格，去掉
            for element in self.soup.find_all():
                if element.string and len(element.string) > 2:
                    element.string = element.text[1: len(element.string) - 1]
        # print('self.soup',self.soup)
        self.st = SymbolTable(self.soup)

    def compile(self):
        logger.debug('start to compile')
        subroutine_decs = self.soup.find_all('subroutineDec')
        # print('subroutines', subroutines)
        index = 0

        for subroutine_dec in subroutine_decs:
            index += 1
            logger.info('处理第{}个方法'.format(index))
            if subroutine_dec.find().text == 'function':
                self.compile_function_define(subroutine_dec)
            elif subroutine_dec.find().text == 'constructor':
                self.compile_constructor_define(subroutine_dec)
            elif subroutine_dec.find().text == 'method':
                self.compile_method_define(subroutine_dec)
            else:
                raise Exception('未知的结构：{}'.format(subroutine_dec))
            logger.info('第{}个方法处理完成'.format(index))
        return self.vm_code

    def compile_constructor_define(self, subroutine_dec):
        function_id = self.get_class_name() + '.' + subroutine_dec.find_all()[2].text
        # 进行子程序头部定义。格式为 function func_name local_var_amount
        local_vars_amount = self.st.get_local_vars_amount(function_id)
        logger.debug('function_id:{}, local_vars_amount:{}'.format(function_id, local_vars_amount))
        code = 'function {} {}'.format(function_id, local_vars_amount)
        self.vm_code.append(code)
        logger.info(code)
        # 分配内存空间
        class_vars_amount = self.st.get_class_vars_amount(self.get_class_name())
        self.vm_code.append('push constant {}'.format(class_vars_amount))
        self.vm_code.append('call Memory.alloc 1')
        # 设置当前对象的this地址
        self.vm_code.append('pop pointer 0')
        # 处理方法体部分
        statements = subroutine_dec.find('subroutineBody').find_all('statements', recursive=False)
        self.compile_statements(function_id, statements)

    def compile_method_define(self, subroutine_dec):
        function_id = self.get_class_name() + '.' + subroutine_dec.find_all()[2].text
        # 进行子程序头部定义。格式为 function func_name local_var_amount
        local_vars_amount = self.st.get_local_vars_amount(function_id)
        logger.debug('function_id:{}, local_vars_amount:{}'.format(function_id, local_vars_amount))
        code = 'function {} {}'.format(function_id, local_vars_amount)
        self.vm_code.append(code)
        logger.info(code)
        # 设置this
        self.vm_code.append('push argument 0')
        self.vm_code.append('pop pointer 0')
        # 处理方法体部分
        statements = subroutine_dec.find('subroutineBody').find_all('statements', recursive=False)
        self.compile_statements(function_id, statements)

    # 进行子程序头部定义。格式为 function func_name local_var_amount+方法体部分
    def compile_function_define(self, subroutine_dec):
        function_id = self.get_class_name() + '.' + subroutine_dec.find_all()[2].text
        # 进行子程序头部定义。格式为 function func_name local_var_amount
        local_vars_amount = self.st.get_local_vars_amount(function_id)
        logger.debug('function_id:{}, local_vars_amount:{}'.format(function_id, local_vars_amount))
        code = 'function {} {}'.format(function_id, local_vars_amount)
        self.vm_code.append(code)
        logger.info(code)
        # 处理方法体部分
        statements = subroutine_dec.find('subroutineBody').find_all('statements', recursive=False)
        self.compile_statements(function_id, statements)

    def compile_statements(self, function_id, statements):
        for statement in statements:
            do_while_if_statements = statement.find_all(re.compile('.*Statement'),
                                                        recursive=False)
            for curr_statement in do_while_if_statements:
                self.print_source_code(curr_statement)
                if curr_statement.name == 'doStatement':
                    self.compile_do_statement(function_id, curr_statement)
                elif curr_statement.name == 'whileStatement':
                    self.compile_while_statement(function_id, curr_statement)
                elif curr_statement.name == 'ifStatement':
                    self.compile_if_statement(function_id, curr_statement)
                elif curr_statement.name == 'letStatement':
                    self.compile_let_statement(function_id, curr_statement)
                elif curr_statement.name == 'returnStatement':
                    self.compile_return_statement(function_id, curr_statement)
                else:
                    raise Exception('{无法识别的statement}'.format(curr_statement))


    def print_source_code(self, expression):
        head_nodes = expression.find_all()[:3]
        code = self.get_code(head_nodes)
        code = code.replace('\n', '').replace('\r', '')
        logger.info('开始解析:{}'.format(code))

    def get_code(self, head_nodes):
        code = ''
        for item in head_nodes:
            if type(item.text) == str:
                code = code + ' ' + item.text
            else:
                code + code + ' ' + self.get_code(item)
        return code


    def compile_do_statement(self, function_id, statement):
        # expression_xml = statement.contents()
        statement.find().decompose()
        # logger.info('==============================')
        # logger.info(statement)
        expression_compiler = ExpressionCompiler(function_id, self.st)
        expression_compiler.compile_term(statement)
        self.vm_code.extend(expression_compiler.get_vm_code())
        # do语句没有变量接受返回值，故把值丢到临时区域
        self.vm_code.append('pop temp 0')

    def compile_while_statement(self, function_id, statement):
        current_label_index = self.while_label_index
        self.while_label_index += 1
        logger.info('==========into while==========')
        # 方式while。start标签，以便重复执行
        while_start = 'WHILE_EXP{}'.format(current_label_index)
        self.vm_code.append('label {}'.format(while_start))
        # 计算while表达式的值，放入堆栈中
        expression = statement.find('expression', recursive=False)
        expression_compiler = ExpressionCompiler(function_id, self.st)
        expression_compiler.compile_expression(expression)
        self.vm_code.extend(expression_compiler.get_vm_code())
        # 构造while判断体
        # not 表达式为真则退出
        while_end = 'WHILE_END{}'.format(current_label_index)
        self.vm_code.append('not')
        self.vm_code.append('if-goto {}'.format(while_end))
        # 判断这个值大于0则进入程序块WHILE_START.while_label_index
        while_true = 'WHILE_TRUE{}'.format(current_label_index)
        # while程序体
        expression_bodys = statement.find_all('statements', recursive=False)
        self.compile_statements(function_id, expression_bodys)
        # 程序体跳转回去继续判断
        self.vm_code.append('goto {}'.format(while_start))
        self.vm_code.append('label {}'.format(while_end))

    def compile_if_statement(self, function_id, statement):
        current_label_index = self.if_label_index
        self.if_label_index += 1
        # 计算if表达式的值，放入堆栈中
        expression = statement.find('expression', recursive=False)
        expression_compiler = ExpressionCompiler(function_id, self.st)
        expression_compiler.compile_expression(expression)
        self.vm_code.extend(expression_compiler.get_vm_code())

        # 构造if。end标签，以便执行后退出
        if_end = 'IF_END{}'.format(current_label_index)
        statement_length = len(statement.find_all('statements', recursive=False))

        # 构造if判断体
        if_true = 'IF_TRUE{}'.format(current_label_index)
        # 为真则进入 label IF_TRUE
        self.vm_code.append('if-goto {}'.format(if_true))
        if_false = 'IF_FALSE{}'.format(current_label_index)
        # 为假则进入 label IF_FALSE
        self.vm_code.append('goto {}'.format(if_false))

        # if_TRUE 则执行如下代码
        self.vm_code.append('label {}'.format(if_true))
        if_true_bodys = statement.find_all('statements', recursive=False)[0:1]
        # logger.info('if body==========={}'.format(expression_bodys))
        self.compile_statements(function_id, if_true_bodys)
        if statement_length > 1:
            self.vm_code.append('goto {}'.format(if_end))

        # if_FALSE 则执行如下代码
        self.vm_code.append('label {}'.format(if_false))
        if statement_length > 1:
            # 为假则执行
            if_false_bodys = statement.find_all('statements', recursive=False)[1:2]
            self.compile_statements(function_id, if_false_bodys)

        # 执行完毕，退出
        if statement_length > 1:
            self.vm_code.append('label {}'.format(if_end))


    def compile_let_statement(self, function_id, statement):
        expression = statement.find('expression', recursive=False)
        # 计算等号后面表达式的值
        expression_compiler = ExpressionCompiler(function_id, self.st)
        expression_compiler.compile_expression(expression)
        self.vm_code.extend(expression_compiler.get_vm_code())

        # 把上面计算出的值赋值给let后的变量
        # 找到变量名称
        var_name = statement.find_all()[1].text
        # 赋值
        var_info = self.st.check_var_info(function_id, var_name)
        if var_info['kind'] == 'field':
            # 如果是对象属性，则赋值到heap区域
            # 然后赋值
            self.vm_code.append('pop this {}'.format(var_info['index']))
        else:
            self.vm_code.append('pop {} {}'.format(var_info['kind'], var_info['index']))


    def compile_return_statement(self, function_id, statement):
        # 如果return后面有表达式
        if statement.find('expression'):
            # 计算返回值表达式
            expression_compiler = ExpressionCompiler(function_id, self.st)
            expression_compiler.compile_expression(statement.find('expression'))
            self.vm_code.extend(expression_compiler.get_vm_code())
        else:
            self.vm_code.append('push constant 0')

        self.vm_code.append('return')
        logger.info('push constant 0')
        logger.info('return')
        return

    def compile_function_start(self, function_id):
        local_vars_amount = self.st.get_local_vars_amount(function_id)
        logger.debug('function_id:{}, local_vars_amount:{}'.format(function_id, local_vars_amount))
        code = 'function {} {}'.format(function_id, local_vars_amount)
        self.vm_code.append(code)
        logger.info(code)

    def get_class_name(self):
        return self.soup.find_all()[2].text

# compiler = JackCompiler('D:/program/nand2tetris/11/Seven/Main.xml')
# compiler.compile()