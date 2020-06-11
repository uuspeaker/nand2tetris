from Log import logger
import logging

class ExpressionCompiler:

    op_dic = {
        '+': 'add',
        '-': 'sub',
        '*': 'call Math.multiply 2',
        '/': 'call Math.divide 2',
        '&': 'and',
        '|': 'or',
        '&gt;': 'gt',
        '&lt;': 'lt',
        '=': 'eq',
        '~': 'not',
    }

    def __init__(self, function_id, symbol_table, expression_xml):
        self.function_id = function_id
        self.expression = expression_xml
        self.symbol_table = symbol_table
        self.vm_code = []

    def compile(self):
        logger.info(self.expression)
        self.compile_term(self.expression)
        logger.info(self.vm_code)

    def get_op(self, value):
        return self.op_dic.get(value, '')

    def get_vm_code(self):
        return self.vm_code

    def compile_items(self, items):
        if len(items) == 0:
            return
        item = items[0]
        logger.debug('解析{}'.format(item))
        # 如果是操作符号op
        if item.name == 'symbol' and item.text in ['+', '-', '*', '/', '=', '&gt;', '&lt;', '&', '|']:
            self.compile_term(items[1])
            self.vm_code.append('{}'.format(self.get_op(item.text)))
            if len(items) == 2:
                return
            self.compile_items(items[2:])
        elif item.name == 'term':
            self.compile_term(item)
            if len(items) == 1:
                return
            self.compile_items(items[1:])
        else:
            raise Exception('未知{}'.format(item))

    def compile_term(self,item):
        logger.debug(item)
        # 如果是前缀操作符号
        if item.find().name == 'symbol' and len(item.find_all()) > 1 and item.find().text in ['~', '-']:
            next_item = item.find('term')
            self.compile_term(next_item)
            # 处理前缀操作符
            if item.find().text == '~':
                self.vm_code.append('not')
            else:
                self.vm_code.append('neg')
        # 如果是数字常量
        elif item.find().name == 'integerConstant':
            self.vm_code.append('push constant {}'.format(item.find().text))
        # 如果是复合表达式
        elif item.find().text == '(':
            expression = item.find('expression', recursive=False)
            # expression_compiler = ExpressionCompiler(self.function_id, self.symbol_table, expression)
            # expression_compiler.compile()
            self.compile_items(expression.find_all(recursive=False))
            # self.vm_code.extend(expression_compiler.get_vm_code())
        # 如果是方法调用
        elif item.find().name == 'identifier' and (len(item.find_all()) > 1 and item.find_all()[1].text == '(' or item.find_all()[1].text == '.'):
            func_name = self.get_func_name(item)
            # 把参数推入堆栈
            for argument in item.find('expressionList', recursive=False).find_all('expression', recursive=False):
                self.compile_items(argument.find_all(recursive=False))
            # 进行方法调用
            local_var_amount = self.symbol_table.get_local_vars_amount(self.function_id)
            self.vm_code.append('call {} {}'.format(func_name, local_var_amount))
        # 如果是普通变量
        elif item.find().name == 'identifier' and len(item.find_all()) == 1:
            # 则先找到变量地址信息，然后push
            kind, index = self.symbol_table.get_sub_var(self.function_id, item.find().text)
            self.vm_code.append('push {} {}'.format(kind, index))
        # todo 如果是数组变量
        elif item.find().name == 'identifier' and len(item.find_all()) > 1 and item.find_all()[1].text == '[':
            logger.error('还未实现数组'.format(item))
            raise Exception('还未实现数组'.format(item))
        else:
            logger.error('无法识别此表达式{}'.format(item))
            raise Exception('无法识别此表达式{}'.format(item))
        # logger.info(self.vm_code)

    def get_func_name(self, item):
        # logger.debug(item)
        name = ''
        for value in item.find_all():
            if value.text == '(':
                return name
            else:
                name += value.text
        return name



