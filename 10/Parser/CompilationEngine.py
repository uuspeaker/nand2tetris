import re

class CompilationEngine:

    def __init__(self, tokens):
        self.old_tokens = tokens
        self.new_tokens = []
        self.token_indx = 0

    def compile_class(self):
        # 开头必须为class className {的格式
        self.write('<class>')
        self.eat('class')
        self.has_name('identifier')
        self.eat_current()
        self.eat('{')
        # 下面的内容必须为0个或多个classVarDex, subroutineDec
        while (True):
            if self.is_value(['static', 'field']):
                self.eat(['static', 'field'])
                self.compile_var_dec()
            elif self.is_value(['constructor', 'function', 'method']):
                self.compile_subroutine_dec()
            else:
                # 进入此处表示class解析完成，必须以}结束
                break
        # 最后必须以}结尾
        self.eat('}')
        self.write('</class>')
        return self.new_tokens

    def write(self, value):
        self.new_tokens.append(value)

    def get_current_token(self):
        return self.old_tokens[self.token_indx]

    def is_name(self, name_range):
        if self.get_current_token_name() in name_range:
            return True
        else:
            return False

    def is_value(self, value_range):
        if self.get_current_token_value() in value_range:
            return True
        else:
            return False

    def is_name_value(self, name_range, value_range):
        return self.is_name(name_range) and self.is_value(value_range)

    def has_name(self, name_range):
        if not self.is_name(name_range):
            self.raise_exception('节点名称必须为 {}'.format(name_range))

    # 处理当前token并进入下一个token
    # 如果传入value_range则检查当前token必须在传入值范围内
    def eat(self, value_range):
        if not self.is_value(value_range):
            self.raise_exception('token值必须为 {}'.format(value_range))
        self.eat_current()

    def eat_current(self):
        self.new_tokens.append(self.get_current_token())
        print('翻译完成:{}'.format(self.get_current_token()))
        self.token_indx += 1

    def has_name_value(self, name_range, value_range):
        self.has_name(name_range)
        self.eat(value_range)

    def get_current_token_name(self):
        return self.get_token_content(r'<(\w+)>')

    def get_current_token_value(self):
        return self.get_token_content(r'> (.+) <')

    def get_token_content(self, re_exp):
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
        print('============')
        self.new_tokens.append('<statements>')
        while True:
            print('------------------')
            if self.is_value('if'):
                self.compile_if_statement()
            elif self.is_value('while'):
                self.compile_while_statement()
            elif self.is_value('let'):
                self.compile_let_statement()
            else:
                break
        self.new_tokens.append('</statements>')

    def compile_if_statement(self):
        return

    def compile_while_statement(self):
        return

    def compile_let_statement(self):
        self.new_tokens.append('<letStatement>')
        self.eat('let')
        self.has_name('identifier')
        
        self.eat(')')
        self.new_tokens.append('</letStatement>')

    def compile_subroutine_dec(self):
        self.new_tokens.append('<subroutineDec>')
        self.eat(['constructor', 'function', 'method'])
        if (not self.is_value(['void', 'int', 'char', 'boolean'])) and (not self.is_name('identifier')):
            self.raise_exception('修饰符必须为 void, int, char, boolean, className')
        self.eat_current()
        self.has_name('identifier')
        self.eat_current()
        self.compile_parameter_list()
        self.compile_subroutine_body()
        self.new_tokens.append('</subroutineDec>')

    def compile_subroutine_body(self):
        self.new_tokens.append('<subroutineBody>')
        self.eat('{')

        while (True):
            print('++++++++++++')
            if self.is_value('var'):
                self.new_tokens.append('<varDec>')
                self.eat('var')
                self.compile_var_dec()
                self.new_tokens.append('</varDec>')
            elif self.is_value(['if', 'while', 'let']):
                self.compile_statements()
            else:
                break

        self.eat('}')
        self.new_tokens.append('</subroutineBody>')

    def compile_parameter_list(self):
        self.eat('(')
        self.new_tokens.append('<parameterList>')
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
        self.new_tokens.append('</parameterList>')
        self.eat(')')

    # 格式必须为type varName
    def compile_type(self):
        if self.is_value(['void', 'int', 'char', 'boolean']) or self.is_name('identifier'):
            self.eat_current()
            self.has_name('identifier')
            self.eat_current()

    # 格式必须是type varName (, varName)*;
    def compile_var_dec(self):
        # 格式必须是type varName
        self.compile_type()
        # 格式必须是 (, varName)*;
        while self.is_value(','):
            self.eat(',')
            self.has_name('identifier')
            self.eat_current()
        self.eat(';')

    def compile_term(self):
        return

    def compile_expression_list(self0):
        return

    def raise_exception(self, value):
        print('翻译:{}'.format(self.get_current_token()))
        print('错误：', value)
        # raise Exception(value)
