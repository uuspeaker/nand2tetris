from bs4 import BeautifulSoup
from SymbolTable import SymbolTable
from ExpressionCompiler import ExpressionCompiler
from Log import logger
import re



class JackCompiler:

    label_index = 1

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
            logger.info('第{}个方法处理完成'.format(index))
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
        expression_compiler = ExpressionCompiler(function_id, self.st, statement)
        self.vm_code.extend(expression_compiler.compile())
        # do语句没有变量接受返回值，故把值丢到临时区域
        self.vm_code.append('pop temp 0')

    def compile_while_statement(self, function_id, statement):
        # 方式while。start标签，以便重复执行
        while_start = '{}$WHILE_START.{}'.format(function_id, self.label_index)
        self.vm_code.append('label {}'.format(while_start))
        # 计算while表达式的值，放入堆栈中
        expression = statement.find('expression', recursive=False).find('term')
        expression_compiler = ExpressionCompiler(function_id, self.st, expression)
        self.vm_code.extend(expression_compiler.compile())
        # 构造while判断体
        # 判断这个值大于0则进入程序块function_id$WHILE_START.label_index
        while_true = '{}$WHILE_TRUE.{}'.format(function_id, self.label_index)
        while_false = '{}$WHILE_FALSE.{}'.format(function_id, self.label_index)
        self.vm_code.append('if-goto {}'.format(while_true))
        # 小于0则退出到function_id$WHILE_END.label_index
        self.vm_code.append('goto {}'.format(while_false))
        self.label_index += 1
        # 构造while程序体
        self.vm_code.append('label {}'.format(while_true))
        expression_bodys = statement.find_all('statements', recursive=False)
        self.compile_statements(function_id, expression_bodys)
        self.vm_code.append('goto {}'.format(while_start))
        self.vm_code.append('label {}'.format(while_false))



    def compile_if_statement(self, function_id, statement):
        # 计算if表达式的值，放入堆栈中
        expression = statement.find('expression', recursive=False).find('term')
        expression_compiler = ExpressionCompiler(function_id, self.st, expression)
        self.vm_code.extend(expression_compiler.compile())
        # 构造if。end标签，以便执行后退出
        if_end = '{}$IF_END.{}'.format(function_id, self.label_index)
        # 构造if判断体
        # 判断这个值大于0则进入程序块function_id$IF_TRUE.label_index
        if_true = '{}$IF_TRUE.{}'.format(function_id, self.label_index)
        self.vm_code.append('if-goto {}'.format(if_true))
        # 小于0则退出到function_id$IF_FALSE.label_index
        if_false = '{}$IF_FALSE.{}'.format(function_id, self.label_index)
        self.vm_code.append('goto {}'.format(if_false))
        self.label_index += 1
        # 构造IF_TRUE程序体
        self.vm_code.append('label {}'.format(if_true))
        expression_bodys = statement.find_all('statements', recursive=False)[0:1]
        # logger.info('if body==========={}'.format(expression_bodys))
        self.compile_statements(function_id, expression_bodys)
        self.vm_code.append('goto {}'.format(if_end))
        # 构造IF_FALSE程序体
        self.vm_code.append('label {}'.format(if_false))
        expression_bodys = statement.find_all('statements', recursive=False)[1:2]
        self.compile_statements(function_id, expression_bodys)
        # 执行完毕，退出
        self.vm_code.append('label {}'.format(if_end))

    def compile_let_statement(self, function_id, statement):
        expression = statement.find('expression', recursive=False).find('term')
        # logger.debug(expression)
        expression_compiler = ExpressionCompiler(function_id, self.st, expression)
        self.vm_code.extend(expression_compiler.compile())

        # 实现pop
        # 找到变量名称
        var_name = statement.find_all()[1].text
        # 获取变量类别
        kind, index = self.st.get_var_info(function_id, var_name)
        code = 'pop {} {}'.format(kind, index)
        # 实现pop
        self.vm_code.append(code)
        logger.debug(code)
        return

    def compile_return_statement(self, function_id, statement):
        # 如果return后面有表达式
        if statement.find('expression'):
            # 计算返回值表达式
            expression_compiler = ExpressionCompiler(function_id, self.st, statement.find('expression').find('term'))
            self.vm_code.extend(expression_compiler.compile())
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