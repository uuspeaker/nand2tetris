import re

class JackTokenizer:

    keywords = ['class', 'constructor', 'function', 'method', 'field','static', 'var','int','char','boolean','void','true','false','null','this','let', 'do','if', 'else','while','return']
    symbols = '{}()[].,;+-*/&|<>=~'

    def __init__(self, sentence):
        self.sentence = sentence
        # 当前已经提取出来的token
        self.tokens = []
        # 当前要检测的字符串的开头
        self.begin = 0
        # 当前要检测的字符串的结尾
        self.end = 0
        # sentence[begin:end]的类型，0无，1空格，2symbol，3数字，4以双引号打头的字符串， 5标识符
        self.current_status = 0
        # next字符的类型, 0无，1空格，2symbol， 3数字，4双引号， 5英文字母或下划线
        self.next_status = 0

    def execute(self):
        if len(self.sentence) < self.end:
            return
        # 处理下一个字符
        self.preceed_next()
        # 以无或者空格开头时，不管后面是什么，都变成后面的状态
        if self.current_status in (0,1):
            self.proceed_blank()
        elif self.current_status == 2:
            # 处理symbol识别
            self.proceed_symbol()
        elif self.current_status == 3:
            # 处理数字识别
            self.proceed_number()
        elif self.current_status == 4:
            # 处理字符串识别
            self.proceed_string()
        elif self.current_status == 5:
            # 处理标识符识别
            self.proceed_identity()
        # 推进下一位
        self.end = self.end + 1
        self.execute()

    def proceed_blank(self):
        self.current_status = self.next_status

    def proceed_symbol(self):
        # 登记token
        self.record_token('symbol')

    def proceed_number(self):
        if self.next_status != 3:
            # 如果后面的不是数字，表示数字识别完成，登记token
            self.record_token('integerConstant')
        else:
            # 如果后面还是数字，表示数字还未识别完成，什么都不用做
            return

    def proceed_string(self):
        if self.next_status == 4:
            # 第二次出现双引号，表示字符串识别完成
            # 此时第二次出现双引号是字符串的一部分，故需要推进一位
            self.end = self.end + 1
            self.preceed_next()
            # 登记token
            self.record_token('stringConstant')

        else:
            # 如果不是双引号，表示字符串还未识别完成，什么都不用做
            return

    def proceed_identity(self):
        if self.next_status in (3,5):
            # 如果后面的是字母，数字或下划线，表示标识符还未识别完，继续识别
            return
        else:
            # 其他情况表示识别结束
            self.record_token('identifier')

    def record_token(self, token):
        word = self.sentence[self.begin: self.end].strip()
        word = self.replace_special_char(word)
        if(self.current_status == 4):
            word = word.replace('"','')
        # 登记token
        if(word in self.keywords):
            self.tokens.append('<keyword> {} </keyword>'.format(word))
        else:
            self.tokens.append('<{}> {} </{}>'.format(token, word, token))

        # 重新开始
        self.begin = self.end
        # 更新状态
        self.current_status = self.next_status

    def replace_special_char(self, value):
        value = value.replace('&', '&amp;')
        value = value.replace('<', '&lt;')
        value = value.replace('>', '&gt;')

        return value

    def get_tokens(self):
        self.execute()
        return self.tokens

    # 处理下一个字符，推进一位并获取下一个字符的类型
    def preceed_next(self):
        if len(self.sentence) == self.end:
            self.next_status = 0
            return
        next_char = self.sentence[self.end: self.end + 1]
        if next_char == ' ':
            self.next_status = 1
        elif next_char in self.symbols:
            self.next_status = 2
        elif re.match(r'\d', next_char):
            self.next_status = 3
        elif next_char == '"':
            self.next_status = 4
        elif re.match(r'[A-Za-z_]', next_char):
            self.next_status = 5




