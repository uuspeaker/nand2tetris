from Log import logger

class ExpressionCompiler:

    op_dic = {
        '+': 'add',
        '-': 'sub',
        '*': 'call Math.multiply 2',
        '/': 'call Math.divide 2',
        '&': 'and',
        '|': 'or',
        '>': 'gt',
        '<': 'lt',
        '=': 'eq',
    }

    def __init__(self, function_id, symbol_table, expression):
        self.function_id = function_id
        self.expression = expression
        self.symbol_table = symbol_table
        self.vm_vode = []

    def get_op(self, value):
        return self.op_dic.get(value, '')

    def get_vm_code(self):
        return self.vm_vode

    def recognize_items(self, expression):
        items = expression.find_all(['term','symbol'], recursive=False)
        exp_items = []
        for item in items:
            # logger.info('解析{}'.format(item))
            # 如果是操作符号op
            if item.name == 'symbol':
                exp_items.append({'item': 'op', 'value': item.text})
            # 如果是数字常量
            elif item.find().name == 'integerConstant':
                exp_items.append({'item': 'exp', 'type': 'number', 'value': item.find().text})
            # 如果是变量
            elif item.find().name == 'identifier':
                exp_items.append({'item': 'exp','type': 'var', 'value': item.find().text})
            # 如果是表达式
            elif item.find().text == '(':
                exp_items.append({'item': 'exp','type': 'exp', 'expression': self.recognize_items(item.find('expression'))})
            # 如果是方法调用
            elif item.find().name == 'identifier' and  (item.find_all()[1].text == '(' or item.find_all()[1].text == '.'):
                func_name = self.get_func_name(item)
                func_arg = []
                for func_exp in item.find('expressionList', recursive=False).find_all('expression', recursive=False):
                    func_arg.append(self.recognize_items(func_exp))
                exp_items.append({'item': 'exp', 'type': 'func', 'func_name': func_name, 'args': func_arg})
        return exp_items

    def get_func_name(self, item):
        name = ''
        for value in item.find_all():
            if value == '(':
                return name
            else:
                name += value
        return name

    def compile(self):
        # logger.debug(self.expression)
        exp_items = self.recognize_items(self.expression)
        logger.debug('第一步：xml转化成exp，op，func，以下为本次转化后的结果')
        logger.debug(exp_items)
        self.compile_item(exp_items)

    def get_item(self, items, index):
        if len(items) > index:
            return items[index]
        else:
            return ''

    def compile_item(self, items):
        item1 = self.get_item(items, 0)
        item2 = self.get_item(items, 1)
        item3 = self.get_item(items, 2)
        if item1 == '':
            return
        # logger.info(items)
        if item1['item'] == 'exp' and item2 == '' and item3 == '':
            if item1['type'] == 'number':
                code = 'push constant {}'.format(item1['value'])
                self.vm_vode.append(code)
                logger.info(code)
            elif item1['type'] == 'var':
                # 如果是 单独一个变量，则先找到变量地址信息，然后push
                kind, index = self.symbol_table.get_vars(self.function_id, item1.value)
                code = 'push {} {}'.format(kind, index)
                self.vm_code.append(code)
                logger.info(code)
            elif item1['type'] == 'exp':
                self.compile_item(item1['expression'])
            else:
                logger.error('未知的表达式item1:{}'.format(item1))
                raise Exception('未知的表达式item1:{}'.format(item1))
        elif item1['item'] == 'op' and item2['item'] == 'exp':
            self.compile_item([item2])
            code = self.get_op(item1.value)
            self.vm_vode.append('{}'.format(code))
            logger.info(code)
        elif item1['item'] == 'exp' and item2['item'] == 'op' and item3['item'] == 'exp':
            # logger.info('enter into exp-op-exp')
            self.compile_item([item1])
            self.compile_item([item3])
            code = '{}'.format(self.get_op(item2['value']))
            self.vm_vode.append(code)
            logger.info(code)
        elif item1['type'] == 'func':
            args = item1['args']
            for arg in args:
                code = 'push argument {}'.format(arg.value)
                self.vm_vode.append(code)
                logger.info(code)
            code = 'call {} {}'.format(item1.func_name, len(args))
            self.vm_vode.append(code)
            logger.info(code)


