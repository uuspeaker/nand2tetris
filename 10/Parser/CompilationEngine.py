import re

class CompilationEngine:

    def __init__(self, tokens):
        self.old_tokens = tokens
        self.new_tokens = []
        self.token_indx = 0

    def compile(self):
        try:
            self.compile_class()
        except Exception as e:
            print('compile error', e)
        return self.new_tokens

    def compile_class(self):
        # 开头必须为class className {的格式
        self.write('<class>')
        self.eat_value('class')
        self.eat_name('identifier')
        self.eat_value('{')
        # 下面的内容必须为0个或多个classVarDex, subroutineDec
        while (True):
            if self.is_value(['static', 'field']):
                self.write('<classVarDec>')
                self.eat_value(['static', 'field'])
                self.compile_var_dec()
                self.write('</classVarDec>')
            elif self.is_value(['constructor', 'function', 'method']):
                self.compile_subroutine_dec()
            else:
                # 进入此处表示class解析完成，必须以}结束
                break
        # 最后必须以}结尾
        self.eat_value('}')
        self.write('</class>')
        return self.new_tokens

    def write(self, value):
        self.new_tokens.append(value)

    def get_current_token(self):
        if self.token_indx == len(self.old_tokens):
            return ''
        return self.old_tokens[self.token_indx]

    def is_name(self, name_range):
        if self.get_current_token_name() in name_range:
            return True
        else:
            return False

    def is_value(self, value_range):
        if self.get_current_token_value() == '':
            return False
        if self.get_current_token_value() in value_range:
            return True
        else:
            return False

    def is_name_value(self, name_range, value_range):
        return self.is_name(name_range) and self.is_value(value_range)

    def eat_name(self, name_range):
        if not self.is_name(name_range):
            self.raise_exception('节点名称必须为 {}'.format(name_range))
        self.eat_current()

    # 处理当前token并进入下一个token
    # 如果传入value_range则检查当前token必须在传入值范围内
    def eat_value(self, value_range):
        if not self.is_value(value_range):
            self.raise_exception('token值必须为 {}'.format(value_range))
        self.eat_current()

    def eat_current(self):
        self.write(self.get_current_token())
        print('翻译完成:{}'.format(self.get_current_token()))
        self.token_indx += 1

    def has_name_value(self, name_range, value_range):
        self.eat_name(name_range)
        self.eat_value(value_range)

    def get_current_token_name(self):
        return self.get_token_content(r'<(\w+)>')

    def get_current_token_value(self):
        return self.get_token_content(r'> (.+) <')

    def get_token_content(self, re_exp):
        if self.token_indx == len(self.old_tokens):
            return ''
        current_token = self.old_tokens[self.token_indx]
        # print('current_token', current_token)
        names = re.findall(re_exp, current_token)
        if len(names) == 0:
            return ''
        else:
            return names[0]



    def compile_symbol(self):
        return

    def compile_statements(self):
        self.write('<statements>')
        while True:
            if self.is_value('if'):
                self.compile_if_statement()
            elif self.is_value('while'):
                self.compile_while_statement()
            elif self.is_value('let'):
                self.compile_let_statement()
            elif self.is_value('do'):
                self.compile_do_statement()
            elif self.is_value('return'):
                self.compile_return_statement()
            else:
                break
        self.write('</statements>')

    def compile_if_statement(self):
        self.write('<ifStatement>')
        self.eat_value('if')
        self.eat_value('(')
        self.compile_expression()
        self.eat_value(')')
        self.eat_value('{')
        self.compile_statements()
        self.eat_value('}')
        if self.is_value('else'):
            self.eat_value('else')
            self.eat_value('{')
            self.compile_statements()
            self.eat_value('}')
        self.write('</ifStatement>')

    def compile_while_statement(self):
        self.write('<whileStatement>')
        self.eat_value('while')
        self.write('</whileStatement>')

    def compile_do_statement(self):
        self.write('<doStatement>')
        self.eat_value('do')
        self.eat_name('identifier')
        self.eat_value('.')
        self.eat_name('identifier')
        self.eat_value('(')
        self.write('<expressionList>')
        # 如果没有以)结束，则下面必须为表达式
        if not self.is_value(')'):
            self.compile_expression_list()
        self.write('</expressionList>')
        self.eat_value(')')
        self.eat_value(';')
        self.write('</doStatement>')

    def compile_return_statement(self):
        self.write('<returnStatement>')
        self.eat_value('return')
        self.eat_value(';')
        self.write('</returnStatement>')
        return

    def compile_let_statement(self):
        self.write('<letStatement>')
        self.eat_value('let')
        self.eat_name('identifier')
        if self.is_value('['):
            self.eat_current()
            self.compile_expression()
            self.eat_value(']')
        self.eat_value('=')
        self.compile_expression()
        self.eat_value(';')
        self.write('</letStatement>')

    def compile_subroutine_dec(self):
        self.write('<subroutineDec>')
        self.eat_value(['constructor', 'function', 'method'])
        if (not self.is_value(['void', 'int', 'char', 'boolean'])) and (not self.is_name('identifier')):
            self.raise_exception('修饰符必须为 void, int, char, boolean, className')
        self.eat_current()
        self.eat_name('identifier')
        self.compile_parameter_list()
        self.compile_subroutine_body()
        self.write('</subroutineDec>')

    def compile_subroutine_body(self):
        self.write('<subroutineBody>')
        self.eat_value('{')

        while (True):
            if self.is_value('var'):
                self.write('<varDec>')
                self.eat_value('var')
                self.compile_var_dec()
                self.write('</varDec>')
            elif self.is_value(['if', 'while', 'let', 'do', 'return']):
                self.compile_statements()
            else:
                break

        self.eat_value('}')
        self.write('</subroutineBody>')

    def compile_parameter_list(self):
        self.eat_value('(')
        self.write('<parameterList>')
        index = 0
        while (True):
            # 如果参数没有结束
            if self.is_value(')'):
                break
            if self.is_value(','):
                # 如果是逗号，表示后面还有参数
                self.compile_type()
            else:
                self.compile_type()
        self.write('</parameterList>')
        self.eat_value(')')

    # 格式必须为type varName
    def compile_type(self):
        if self.is_value(['void', 'int', 'char', 'boolean']) or self.is_name('identifier'):
            self.eat_current()
            self.eat_name('identifier')

    # 格式必须是type varName (, varName)*;
    def compile_var_dec(self):
        # 格式必须是type varName
        self.compile_type()
        # 格式必须是 (, varName)*;
        while self.is_value(','):
            self.eat_value(',')
            self.eat_name('identifier')
        self.eat_value(';')

    def compile_term(self):
        self.write('<term>')
        if self.is_array():
            # 如果是数组格式
            self.eat_current()
        elif self.is_name(['integerConstant', 'stringConstant']):
            # 如果是数字或字符串
            self.eat_current()
        elif self.is_value(['true', 'false', 'null', 'this']):
            # 如果是关键字常量
            self.eat_current()
        elif self.is_name('identifier'):
            # 如果是变量名称
            self.eat_current()
        elif self.is_subtoutine_call():
            # 如果是子程序调用
            self.eat_current()
        elif self.is_subtoutine_call():
            # 如果是带括号的表达式
            self.eat_current()
        elif self.is_subtoutine_call():
            # 如果是(~|-) term
            self.eat_current()
        else:
            self.raise_exception('必须为表达式')
        self.write('</term>')

    def is_subtoutine_call(self):
        return

    def is_array(self):
        return

    def is_term(self):
        value = self.get_current_token_value()
        # 如果是数字
        if re.match(r'\d+', value):
            return True
        # 如果是字符串
        # 如果是关键字常量
        # 如果是变量名称
        # 如果是数组格式
        # 如果是子程序调用
        # 如果是带括号的表达式
        # 如果是(~|-) term

    def compile_expression(self):
        self.write('<expression>')
        self.compile_term()
        if self.is_value(['+', '-', '=', '>', '<', '/', '&', '|']):
            self.eat_current()
            self.compile_term()
        self.write('</expression>')

    def compile_expression_list(self):
        self.compile_expression()
        while self.is_value(','):
            self.compile_expression()

    def is_number(self):
        return re.match(r'\d+', self.get_current_token_value())

    def is_var_name(self):
        return re.match(r'^[a-zA-Z_]\w*', self.get_current_token_value())

    def raise_exception(self, value):
        print('翻译:{}'.format(self.get_current_token()))
        print('错误：', value)
        raise Exception(value)
