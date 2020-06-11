from bs4 import BeautifulSoup
from SymbolTable import SymbolTable
from ExpressionCompiler import ExpressionCompiler
from Log import logger
import re

class JackCompiler:

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
            logger.debug('处理第{}个方法'.format(index))
            if subroutine_dec.find().text == 'function':
                self.compile_function_define(subroutine_dec)

            logger.debug('第{}个方法处理完成'.format(index))
        return self.vm_code

    def compile_constructor_define(self):

        return

    def compile_method_define(self):
        return

    def compile_function_define(self, subroutine_dec):
        logger.debug('进入compile_function_define')
        # todo 处理方法调用返回值
        return_type = subroutine_dec.find_all()[1].text

        function_id = self.get_class_name() + '.' + subroutine_dec.find_all()[2].text
        # 处理function声明部分
        self.compile_function_start(function_id)
        # 处理function的方法体部分
        statements = subroutine_dec.find('subroutineBody').find_all('statements', recursive=False)
        self.compile_statements(function_id, statements)

    def compile_statements(self, function_id, statements):
        for statement in statements:
            do_while_if_statements = statement.find_all(re.compile('.*Statement'),
                                                        recursive=False)
            for curr_statement in do_while_if_statements:
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


    def compile_do_statement(self, function_id, statement):
        # expression_xml = statement.contents()
        statement.find().decompose()
        expression_compiler = ExpressionCompiler(function_id, self.st, statement)
        expression_compiler.compile()
        self.vm_code.extend(expression_compiler.get_vm_code())

    def compile_do_statement2(self, function_id, statement):
        # 找到方法后面包含所有参数的expressionList节点
        expression_list_xml = statement.find('expressionList', recursive=False)
        # 实现push argument
        self.compile_expression_list(function_id, expression_list_xml)

        # 找到方法开始的地方
        nodes = statement.find_all()[1:]
        # 获取方法参数个数
        arg_amount = len(expression_list_xml.find_all('expression', recursive=False))
        # 实现call function
        self.compile_call_function(nodes, arg_amount)

    def compile_expression_list(self, function_id, expression_list_xml):
        # logger.debug('解析方法参数{},{}'.format(function_id,expression_list_xml))
        expressions = expression_list_xml.find_all('expression', recursive=False)
        for expression in expressions:
            expression_compiler = ExpressionCompiler(function_id,self.st, expression)
            expression_compiler.compile()
            self.vm_code.extend(expression_compiler.get_vm_code())

    def compile_while_statement(self, function_id, statement):
        return

    def compile_if_statement(self, function_id, statement):
        return

    def compile_let_statement(self, function_id, statement):
        expression = statement.find('expression')
        logger.debug(expression)
        expression_compiler = ExpressionCompiler(function_id, self.st, expression)
        self.vm_code.extend(expression_compiler.compile())

        # # 实现push argument
        # # 找到方法后面包含所有参数的expressionList节点
        # expression_list_xml = statement.find('expressionList')
        # logger.debug(statement)
        # self.compile_expression_list(function_id, expression_list_xml)
        #
        # # 实现call function
        # # 找到方法开始的地方
        # nodes = statement.find('expression').find('term').find_all()
        # # 获取方法参数个数
        # arg_amount = len(expression_list_xml.find_all('expression', recursive=False))
        # self.compile_call_function(nodes, arg_amount)

        # 实现pop
        # 找到变量名称
        var_name = statement.find_all()[1]
        # 获取变量类别
        var_type = self.st.get_var_type(self.get_class_name(), var_name)
        code = 'pop {} {}'.format(var_type, var_name)
        # 实现pop
        self.vm_code.append(code)
        logger.debug(code)
        return

    def compile_return_statement(self, function_id, statement):
        self.vm_code.append('push constant 0')
        self.vm_code.append('return')
        logger.info('push constant 0')
        logger.info('return')
        return




    # 传入以方法名称开始的xml节点，实现call functioin
    def compile_call_function(self, nodes, arg_len):
        name = ''
        for node in nodes:
            if node.text == '(':
                code = 'call {} {}'.format(name, arg_len)
                self.vm_code.append(code)
                logger.info(code)
                return
            name += node.text
        self.vm_code.append('call {} {}'.format(name, arg_len))
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