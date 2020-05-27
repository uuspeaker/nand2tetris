import re


class CodeExtractor:
    lable_lines = []

    def __init__(self, src_value):
        self.src = src_value

    def get_lines(self):
        with open(self.src, 'r') as file:
            lines = file.readlines()
            print('getLine line size is ', len(lines))
            # print(lines)
            return lines

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
            line = re.sub(r'//.*', '', line)
            line = line.strip()
            valid_lines.append(line.strip())
        print('get_valid_lines line size is ', len(valid_lines))
        print(valid_lines)
        return valid_lines

    def extracte_lables(self, valid_lines):
        index = 0
        self.lable_lines = []
        for line in valid_lines:
            values = re.findall(r'^\((.+)\)$', line)
            if len(values) > 0:
                self.lable_lines.append({'index': index, 'value': values[0]})
            else:
                index = index + 1
        print('self.lable_lines', self.lable_lines)

    def get_index(self, value):
        if re.match('^\d+$', value):
            return value
        compare_value = value.replace('@', '')
        # print('get_index value is ', compare_value)
        for line in self.lable_lines:
            # print('compare value and lable', compare_value, line['value'])
            if compare_value == line['value']:
                # print('============matched,tanslate lable: ',value, '@' + str(line['index']))
                return '@' + str(line['index'])
        return value

    # 识别出每个命令是A，C，或者Lable
    def get_instruction(self):
        valid_lines = self.get_valid_lines()
        self.extracte_lables(valid_lines)
        lines = []
        for line in valid_lines:
            if re.match(r'^\s*@', line):
                lines.append({'type': 'A', 'value': self.get_index(line)})
            elif re.match(r'^\(.+\)$', line):
                lines.append({'type': 'L', 'value': line})
            else:
                lines.append({'type': 'C', 'value': line})

        return lines