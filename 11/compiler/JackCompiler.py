from bs4 import BeautifulSoup
from SymbolTable import SymbolTable
from ExpressionCompiler import ExpressionCompiler
from Log import logger

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
        return

    def compile_constructor_define(self):

        return

    def compile_method_define(self):
        return

    def compile_function_define(self, subroutine_dec):
        logger.debug('get into compile_function')
        return_type = subroutine_dec.find_all()[1].text
        function_id = self.get_class_name() + '.' + subroutine_dec.find_all()[2].text
        self.compile_function_start(function_id)
        statements = subroutine_dec.find('subroutineBody').find_all('statements', recursive=False)
        self.compile_statements(function_id, statements)

    def compile_statements(self, function_id, statements):
        for statement in statements:
            do_while_if_statements = statement.find_all(['doStatement', 'whileStatement', 'ifStatement'],
                                                        recursive=False)
            for do_while_if in do_while_if_statements:
                if do_while_if.name == 'doStatement':
                    self.compile_do_statement(function_id, do_while_if)
                elif do_while_if.name == 'whileStatement':
                    self.compile_while_statement()
                elif do_while_if.name == 'ifStatement':
                    self.compile_if_statement()

    def compile_do_statement(self, function_id, statement):
        expression_list = statement.find('expressionList', recursive=False)
        self.compile_expression_list(function_id, expression_list)
        self.compile_do_function_name(statement, len(expression_list))


    def compile_while_statement(self, statement):
        return

    def compile_if_statement(self, statement):
        return


    def compile_expression_list(self, function_id, expression_list):
        expressions = expression_list.find_all('expression', recursive=False)
        for expression in expressions:
            expression_compiler = ExpressionCompiler(function_id,self.st, expression)
            expression_compiler.compile()

    # def compile_expression(self, function_id, expression):
    #     term_and_symbol = expression.find_all(['term','symbol'], recursive=False)
    #     next_term = self.get_next_term(expression)
    #     # 如果是 op exp
    #     if next_term in ['~', '-']:
    #         op = term_and_symbol.find().text
    #         expression = expression[1:]
    #         next_expression = self.get_next_expression(expression)
    #         self.compile_expression(function_id, next_expression)
    #         self.vm_code.append('{}'.format(op))
    #         self.compile_expression(function_id, expression[len(next_expression):])
    #     elif len(term_and_symbol) == 1:
    #         # 如果是 单独一个数字
    #         if term_and_symbol.find().name == 'integerConstant':
    #             self.vm_code.append('push constant {}'.format(term_and_symbol.find().text))
    #         elif term_and_symbol.find().name == 'identifier':
    #             # 如果是是 单独一个变量，则先找到变量地址信息，然后push
    #             kind, index = self.st.get_vars(function_id, term_and_symbol.find().text)
    #             self.vm_code.append('push {} {}'.format(kind, index))
    #
    #
    #
    #     elif term_and_symbol.find_all()[0].name == 'identifier' and term_and_symbol.find_all()[1].name in ['+', '-', '*', '/']:
    #         # 如果是 exp op exp
    #         self.vm_code.append('push {} {}'.format(0, 0))
    #         self.vm_code.append('push {} {}'.format(0, 0))
    #         self.vm_code.append('push {} {}'.format(0, 0))
    #     # 如果是 f(exp1,exp2...)
    #     elif self.is_func_exp(expression):
    #         self.vm_code.append('push {} {}'.format(0, 0))
    #         self.vm_code.append('push {} {}'.format(0, 0))
    #         self.vm_code.append('call {} {}'.format(0, 0))
    #     else:
    #         raise Exception('未知的表达式')
    #
    #
    #
    # def get_expression_type(self, statement, expression):
    #     term_and_symbol = expression.find_all(['term','symbol'], recursive=False)
    #     if len(term_and_symbol) == 1:
    #         if term_and_symbol.find().name == 'integerConstant':
    #             return 1
    #         elif term_and_symbol.find().name == 'identifier':
    #             return 2
    #         else:
    #             raise Exception('未知的表达式')
    #     if term_and_symbol.find().string in ['~', '-']:
    #         return 2
    #     if term_and_symbol.find_all()[0].name == 'identifier' and term_and_symbol.find_all()[1].name in ['+', '-', '*', '/']:
    #         return 3
    #     return 4
    #
    # def get_next_expression(self, statement):
    #     return



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