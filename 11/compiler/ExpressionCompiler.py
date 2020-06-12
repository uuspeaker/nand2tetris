from Log import logger
import logging
import re

class ExpressionCompiler:

    op_dic = {
        '+': 'add',
        '-': 'sub',
        '*': 'call Math.multiply 2',
        '/': 'call Math.divide 2',
        '&amp;': 'and',
        '&': 'and',
        '|': 'or',
        '&gt;': 'gt',
        '>': 'gt',
        '&lt;': 'lt',
        '<': 'lt',
        '=': 'eq',
        '~': 'not',
    }

    # 传入的expression_xml有两种可能
    # 1，前面解析的语句为let var = expression， 内容为expression
    # 2，do functionCall，此时内容为functionCall
    def __init__(self, function_id, symbol_table):
        self.function_id = function_id
        self.symbol_table = symbol_table
        self.vm_code = []

    def get_op(self, value):
        return self.op_dic.get(value, '')

    def get_vm_code(self):
        return self.vm_code

    def compile_expression(self, expression):
        self.compile_terms(expression.find_all(recursive=False))

    # 递归的方式计算表达式（term表示一个独立的表达式，op表示一个算术符号+-×/&|~）
    # 规则：如果出现op，则后面紧接着的expression（term或op）提前，其他expression顺延
    def compile_terms(self, items):
        if len(items) == 0:
            return
        item = items[0]
        logger.debug('解析{}'.format(item))
        # 如果是操作符号op
        if item.name == 'symbol' and item.text in ['+', '-', '*', '/', '=', '&gt;', '>', '&lt;', '<', '&', '&amp;', '|']:
            self.compile_term(items[1])
            self.vm_code.append('{}'.format(self.get_op(item.text)))
            if len(items) == 2:
                return
            self.compile_terms(items[2:])
        elif item.name == 'term':
            self.compile_term(item)
            if len(items) == 1:
                return
            self.compile_terms(items[1:])
        else:
            raise Exception('未知{}'.format(item))

    def compile_term(self, term):
        # logger.debug(term)
        name = term.find().name
        text = term.find().text
        length = len(term.find_all(recursive=False))
        if length > 1:
            next_text = term.find_all(recursive=False)[1].text
        # 如果是前缀操作符号
        if name == 'symbol' and length > 1 and text in ['~', '-']:
            next_item = term.find('term')
            self.compile_term(next_item)
            # 处理前缀操作符
            if text == '~':
                self.vm_code.append('not')
            else:
                self.vm_code.append('neg')
        # 如果是数字常量
        elif name == 'integerConstant':
            self.vm_code.append('push constant {}'.format(text))
        # 如果是复合表达式
        elif text == '(':
            expression = term.find('expression', recursive=False)
            # expression_compiler = ExpressionCompiler(self.function_id, self.symbol_table, expression)
            # expression_compiler.compile()
            self.compile_expression(expression)
            # self.vm_code.extend(expression_compiler.get_vm_code())
        # 如果是方法调用
        elif name == 'identifier' and length > 1 and (next_text == '(' or next_text == '.'):
            func_name = self.get_func_name(term)
            # 如果是对象方法调用，则把此对象的地址放到栈中（等下面的《方法调用》时，此地址会自动成为argument 0）
            self.obj_invoke_handler(func_name)
            # 把参数推入堆栈
            expressions = term.find('expressionList', recursive=False).find_all('expression', recursive=False)
            for expression in expressions:
                self.compile_expression(expression)
            # 进行《方法调用》
            arg_amount = len(expressions)
            self.vm_code.append('call {} {}'.format(func_name, arg_amount))
        # 如果是变量
        elif name == 'identifier' and length == 1:
            # 则先找到变量地址信息，然后push
            # logger.info(self.function_id)
            # logger.info(text)
            var_info = self.symbol_table.check_var_info(self.function_id, text)

            if var_info['kind'] == 'field':
                logger.debug('处理对象{}'.format(var_info))
                # 如果是对象属性，则从heap区域取值
                self.vm_code.append('push argument 0')
                self.vm_code.append('pop pointer 0')
                self.vm_code.append('push this {}'.format(var_info['index']))
            elif var_info['kind'] == 'argument':
                index = int(var_info['index']) + 1
                self.vm_code.append('push argument {}'.format(index))
            elif var_info['kind'] == 'local':
                # 如果是普通变量，则从对应local或者argument取值
                self.vm_code.append('push local {}'.format(var_info['index']))
        # todo 如果是数组变量
        elif name == 'identifier' and length > 1 and next_text == '[':
            logger.error('还未实现数组'.format(term))
            raise Exception('还未实现数组'.format(term))
        elif name == 'keyword' and text in ['true', 'false', 'null', 'this']:
            if text == 'this':
                self.vm_code.append('push pointer 0')
            elif text == 'true':
                self.vm_code.append('push constant 0')
                self.vm_code.append('not')
            elif text == 'false':
                self.vm_code.append('push constant 0')
            elif text == 'null':
                self.vm_code.append('push constant 0')
        else:
            logger.error('无法识别此表达式{}'.format(term))
            raise Exception('无法识别此表达式{}'.format(term))
        # logger.info(self.vm_code)

    # 对象方法调用时，则将对象地址放到第一个参数
    # 是对象调用则返回True，否则返回False
    def obj_invoke_handler(self, invoked_func_name):
        # 获取对象名称
        obj = re.findall(r'^(.+)\.', invoked_func_name)
        if len(obj) == 0:
            return False
        obj_name = obj[0]
        # 如果能够在变量表找到，则表示是对象
        var_info = self.symbol_table.get_var_info(self.function_id, obj_name)
        if var_info != '':
            # 将此对象地址放到第一个参数
            # 如果是local变量
            if var_info['kind'] == 'local':
                # 将对象的地址放入栈顶
                self.vm_code.append('push local {}'.format(var_info['index']))
            elif var_info['kind'] == 'argument':
                # 获取参数位置
                index = int(var_info['index']) + 1
                # 将对象的地址放入栈顶
                self.vm_code.append('push argument {}'.format(index))
            elif var_info['kind'] == 'field':
                # 获取调用方对象地址
                field_index = int(var_info['index'])
                self.vm_code.append('push argument 0 ')
                # 将对象的地址放入栈顶
                self.vm_code.append('pop pointer 0 ')
                self.vm_code.append('push this {}'.format(field_index))

            return True
        else:
            return False

    def get_func_name(self, item):
        # logger.debug(term)
        name = ''
        for value in item.find_all():
            if value.text == '(':
                return name
            else:
                name += value.text
        return name



