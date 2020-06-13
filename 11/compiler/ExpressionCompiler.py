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
            self.handle_symbol(term, text)
        # 如果是数字常量
        elif name == 'integerConstant':
            self.vm_code.append('push constant {}'.format(text))
            # 如果是字符串常量
        elif name == 'stringConstant':
            logger.info('=======stringConstant========{}'.format(text))
            self.handle_string(text)
        # 如果是复合表达式
        elif text == '(':
            expression = term.find('expression', recursive=False)
            self.compile_expression(expression)
        # 如果是方法调用
        elif name == 'identifier' and length > 1 and (next_text == '(' or next_text == '.'):
            self.handle_subroutine_call(next_text, term)
        # 如果是变量
        elif name == 'identifier' and length == 1:
            self.deal_single_var(text)
        # todo 如果是数组变量
        elif name == 'identifier' and length > 1 and next_text == '[':
            self.handle_array(term)
        elif name == 'keyword' and text in ['true', 'false', 'null', 'this']:
            self.headle_keyword(text)
        else:
            logger.error('无法识别此表达式{}'.format(term))
            raise Exception('无法识别此表达式{}'.format(term))
        # logger.info(self.vm_code)

    def handle_symbol(self, term, text):
        next_item = term.find('term')
        self.compile_term(next_item)
        # 处理前缀操作符
        if text == '~':
            self.vm_code.append('not')
        else:
            self.vm_code.append('neg')

    def handle_array(self, term):
        logger.debug('===========get into array========={}'.format(term))
        array_name = term.find().text
        # 获取数组地址，设置that
        # 获取变量信息
        var_info = self.symbol_table.check_var_info(self.function_id, array_name)
        # 赋值
        if var_info['kind'] == 'field':
            # 计算数组起始地址
            self.vm_code.append('push this {}'.format(var_info['index']))
        else:
            # 计算数组起始地址
            self.vm_code.append('push {} {}'.format(var_info['kind'], var_info['index']))
        # 计算出数组的index
        self.compile_expression(term.find('expression'))
        # 将数组地址和index相加
        self.vm_code.append('add')
        # 让that指向上述计算出的地址
        self.vm_code.append('pop pointer 1')
        # 计算array_name[index]的值
        self.vm_code.append('push that 0')

    def handle_string(self, text):
        self.vm_code.append('push constant {}'.format(len(text)))
        self.vm_code.append('call String.new 1')
        for char in text:
            self.vm_code.append('push constant {}'.format(ord(char)))
            self.vm_code.append('call String.appendChar 2')

    def headle_keyword(self, text):
        if text == 'this':
            self.vm_code.append('push pointer 0')
        elif text == 'true':
            self.vm_code.append('push constant 0')
            self.vm_code.append('not')
        elif text == 'false':
            self.vm_code.append('push constant 0')
        elif text == 'null':
            self.vm_code.append('push constant 0')

    def deal_single_var(self, text):
        # 则先找到变量地址信息，然后push
        # logger.info(self.function_id)
        # logger.info(text)
        var_info = self.symbol_table.check_var_info(self.function_id, text)
        if var_info['kind'] == 'field':
            logger.debug('处理对象{}'.format(var_info))
            # 如果是对象属性，则从heap区域取值
            # self.vm_code.append('push argument 0')
            # self.vm_code.append('pop pointer 0')
            self.vm_code.append('push this {}'.format(var_info['index']))
        else:
            # 如果是普通变量，则从对应local或者argument取值
            self.vm_code.append('push {} {}'.format(var_info['kind'], var_info['index']))

    def handle_subroutine_call(self, next_text, term):
        subroutine_name = self.get_subroutine_name(term)
        is_obj_invoke = False


        if next_text == '.':
            subroutine_left = re.findall(r'^(.+)\.', subroutine_name)[0]
            subroutine_right = re.findall(r'\.(.+)$', subroutine_name)[0]
            var_info = self.symbol_table.get_var_info(self.function_id, subroutine_left)
            # 如果是对象调用，则需要把对象地址推入堆栈
            if var_info != '':
                # 用变量的className代替变量名，这样才能找到方法签名
                subroutine_name = var_info['type'] + '.' + subroutine_right
                is_obj_invoke = True
                # 不为空表示subroutine_left是一个变量，既能发起调用又是变量，所以subroutine_left肯定是一个对象
                # 获取obj的地址，放入堆栈
                if var_info['kind'] == 'field':
                    self.vm_code.append('push this {}'.format(var_info['index']))
                else:
                    self.vm_code.append('push {} {}'.format(var_info['kind'], var_info['index']))
            # 如果是function方法调用，无需处理
        else:
            # 如果是method方法调用，则把当前this放入堆栈，后面重置this时会用到
            self.vm_code.append('push pointer 0')
            is_obj_invoke = True
            # 如果是method方法调用，需要加上"classname."，这样才能找到方法签名
            class_name = re.findall(r'^(.+)\.', self.function_id)[0]
            subroutine_name = class_name + '.' + subroutine_name

        # 把参数推入堆栈
        expressions = term.find('expressionList', recursive=False).find_all('expression', recursive=False)
        for expression in expressions:
            self.compile_expression(expression)
        # 进行方法调用
        arg_amount = len(expressions)
        if is_obj_invoke:
            arg_amount = arg_amount + 1
        self.vm_code.append('call {} {}'.format(subroutine_name, arg_amount))

    def get_subroutine_name(self, item):
        # logger.debug(term)
        name = ''
        for value in item.find_all():
            if value.text == '(':
                return name
            else:
                name += value.text
        return name



