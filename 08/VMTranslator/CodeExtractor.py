import re


class CodeExtractor:
    lable_lines = []

    def __init__(self, src_value):
        self.src = src_value

    def get_lines(self):
        with open(self.src, 'r') as file:
            lines = file.readlines()
            print('总行数 ', len(lines))
            # print(lines)
            return lines

    # 去掉注释和前后空格
    def format_content(self, content):
        content = re.sub(r'//.*', '', content)
        content = content.strip()
        return content

    def get_valid_lines(self):
        lines = self.get_lines()
        valid_lines = []
        for line in lines:
            # 全为空白则无效
            if re.match(r'^\s*$', line):
                continue
            # //打头则无效
            if re.match(r'^\s*//', line):
                continue
            valid_lines.append(self.format_content(line))
        print('有效代码行数 ', len(valid_lines))
        print(valid_lines)
        return valid_lines

    def get_instruction(self):
        valid_lines = self.get_valid_lines()
        lines = []
        for line in valid_lines:
            words = re.split(r'\s+', line)
            lines.append(words)
            # if re.match(r'^push', line):
            #     lines.append({'ins_type': 'push', 'param_type': words[1], 'value': words[2]})
            # elif re.match(r'^pop', line):
            #     lines.append({'ins_type': 'pop', 'param_type': words[1], 'value': words[2]})
            # else:
            #     lines.append({'ins_type': 'cal', 'value': words[0]})

        return lines

# extractor = CodeExtractor('D:/program/nand2tetris/07/StackArithmetic/SimpleAdd/SimpleAdd.vm')
# print(extractor.get_instruction())