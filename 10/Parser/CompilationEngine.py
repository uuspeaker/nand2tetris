import re

class CompilationEngine:

    def __init__(self, tokens):
        self.old_tokens = tokens
        self.new_tokens = []
        self.token_indx = 0

    def compile_class(self):
        # 开头必须为class className {的格式
        self.write('<class>')
        self.has_value('class')
        self.eat_token()
        self.has_name('identifier')
        self.eat_token()
        self.has_value('{')
        self.eat_token()
        # 下面的内容必须为0个或多个classVarDex, subroutineDec
        while (True):
            if self.is_value(['static', 'field']):
                self.compile_class_var_dec()
            elif self.is_value(['constructor', 'function', 'method']):
                self.compile_subroutine_dec()
            else:
                # 进入此处表示class解析完成，必须以}结束
                break
        # 最后必须以}结尾
        self.has_value('}')
        self.write('</class>')
        return self.new_tokens

    def write(self, value):
        self.new_tokens.append(value)

    def eat_token(self):
        self.new_tokens.append(self.get_current_token())
        print('翻译完成:{}'.format(self.get_current_token()))
        self.token_indx += 1

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

    def has_value(self, value_range):
        if not self.is_value(value_range):
            self.raise_exception('节点值必须为 {}'.format(value_range))

    def has_name_value(self, name_range, value_range):
        self.has_name(name_range)
        self.has_value(value_range)

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
        return

    def compile_if_statement(self):
        return

    def compile_while_statement(self):
        return

    def compile_let_statement(self):
        return

    def compile_class_var_dec(self):
        self.next_token_value in ('static', 'field', 'method')
        return

    def compile_subroutine_dec(self):
        self.new_tokens.append('<subroutineDec>')
        self.eat_token()
        if (not self.is_value(['void', 'int', 'char', 'boolean'])) and (not self.is_name('identifier')):
            self.raise_exception('修饰符必须为 void, int, char, boolean, className')
        self.eat_token()
        self.has_name('identifier')
        self.eat_token()
        self.compile_parameter_list()
        self.compile_subroutine_body()
        self.new_tokens.append('</subroutineDec>')

    def compile_subroutine_body(self):
        self.new_tokens.append('<subroutineBody>')
        self.has_value('{')
        self.eat_token()
        self.new_tokens.append('<parameterList>')
        self.compile_var_dec()
        self.compile_statements()
        self.has_value('}')
        self.eat_token()
        self.new_tokens.append('</subroutineBody>')

    def compile_parameter_list(self):
        self.has_value('(')
        self.eat_token()
        self.new_tokens.append('<parameterList>')
        index = 0
        while (True):
            # 如果参数没有结束
            if self.is_value(')'):
                break
            if self.is_value(','):
                # 如果是逗号，表示后面还有参数
                self.eat_token()
                self.compile_type()
            else:
                self.compile_type()
        self.new_tokens.append('</parameterList>')
        self.has_value(')')
        self.eat_token()

    def compile_type(self):
        if self.is_value(['void', 'int', 'char', 'boolean']) or self.is_name('identifier'):
            self.eat_token()
            self.has_name('identifier')
            self.eat_token()

    def compile_var_dec(self):
        return

    def compile_term(self):
        return

    def compile_expression_list(self0):
        return

    def raise_exception(self, value):
        print('翻译:{}'.format(self.get_current_token()))
        print(value)
        # raise Exception(value)
