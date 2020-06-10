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
        subroutine_decs = self.soup.select('subroutineDec')
        # print('subroutines', subroutines)
        for subroutine_dec in subroutine_decs:
            if subroutine_dec.find().text == 'function':
                self.compile_function_define(subroutine_dec)
        return self.vm_code

    def compile_constructor_define(self):

        return

    def compile_method_define(self):
        return

    def compile_function_define(self, subroutine_dec):
        return_type = subroutine_dec.find_all()[1].text
        function_id = self.get_class_name() + '.' + subroutine_dec.find_all()[2].text
        self.compile_function_start(function_id)
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
                    self.compile_while_statement()
                elif curr_statement.name == 'ifStatement':
                    self.compile_if_statement()
                elif curr_statement.name == 'returnStatement':
                    self.compile_return_statement(function_id, curr_statement)


    def compile_do_statement(self, function_id, statement):
        expression_list = statement.find('expressionList', recursive=False)
        # logger.debug(expression_list)
        self.compile_expression_list(function_id, expression_list)
        self.compile_do_function_name(statement, len(expression_list.find_all('expression', recursive=False)))


    def compile_while_statement(self, statement):
        return

    def compile_if_statement(self, statement):
        return

    def compile_return_statement(self, function_id, statement):
        self.vm_code.append('push constant 0')
        self.vm_code.append('return')
        logger.info('push constant 0')
        logger.info('return')
        return


    def compile_expression_list(self, function_id, expression_list):
        expressions = expression_list.find_all('expression', recursive=False)
        for expression in expressions:
            expression_compiler = ExpressionCompiler(function_id,self.st, expression)
            expression_compiler.compile()
            self.vm_code.extend(expression_compiler.get_vm_code())


    def compile_do_function_name(self, statement, arg_len):
        name = ''
        nodes = statement.find_all()[1:]
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
        local_vars = self.st.get_local_vars(function_id)
        code = 'function {} {}'.format(function_id, len(local_vars))
        self.vm_code.append(code)
        logger.info(code)

    def get_class_name(self):
        return self.soup.find_all()[2].text

compiler = JackCompiler('D:/program/nand2tetris/11/Seven/Main.xml')
compiler.compile()