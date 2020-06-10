from bs4 import BeautifulSoup
from Log import logger

class SymbolTable:

    def __init__(self, soup):
        self.class_table = []
        self.sub_table = []
        self.soup = soup
        self.class_name = self.soup.find_all()[2].text
        self.parse()
        logger.info(self.class_table)
        logger.info(self.sub_table)

    def get_class_table(self):
        return self.class_table

    def get_sub_table(self):
        return self.sub_table

    def parse(self):
        file = []
        self.parse_class()
        self.parse_sub()

    def parse_class(self):
        class_var_decs = self.soup.find_all('classVarDec')
        static_index = 0
        field_index = 0
        logger.debug('类级变量个数{}'.format(len(class_var_decs)))
        for class_var_dec in class_var_decs:
            all_elements = class_var_dec.find_all()
            var_kind = all_elements[0].string
            var_type = all_elements[1].string
            # 前面两个标签是变量定义，故去除
            all_elements = all_elements[2: len(all_elements) - 1]
            for element in all_elements:
                # 变量定义一定是identifier标签
                if element.name != 'identifier':
                    continue
                if var_kind == 'static':
                    self.class_table.append({'id': self.class_name, 'name': element.string, 'type': var_type, 'kind': 'static', 'index': static_index})
                    static_index += 1
                else:
                    self.class_table.append({'id': self.class_name,'name': element.string, 'type': var_type, 'kind': var_kind, 'index': field_index})
                    field_index += 1

    def parse_sub(self):
        sub_var_decs = self.soup.find_all('varDec')
        argument_index = 0
        local_index = 0
        pre_id = ''
        logger.debug('方法级变量个数{}'.format(len(sub_var_decs)))
        for sub_var_dec in sub_var_decs:
            # 类名+方法名作为id
            sub_name = sub_var_dec.parent.parent.find_all()[2].text
            id = self.class_name + '.' + sub_name
            # 若id变化，表示进入新方法，则变量的所索引值需要重置
            if id != pre_id:
                argument_index = 0
                local_index = 0
                pre_id = id
            # print('sub_var_dec', sub_var_dec.find_all()[0].string)
            all_elements = sub_var_dec.find_all()
            # varDec下的第一个是变量种类（argument，local）
            var_kind = all_elements[0].string
            # varDec下的第二个类型（int, boolean, char, className）
            var_type = all_elements[1].string
            # 前面两个标签是变量定义，故去除
            all_elements = all_elements[2: len(all_elements) - 1]
            for element in all_elements:
                # 变量定义一定是identifier标签
                if element.name != 'identifier':
                    continue
                if var_kind == 'argument':
                    self.sub_table.append({'id': id, 'name': element.string, 'type': var_type, 'kind': 'argument', 'index': argument_index})
                    argument_index += 1
                else:
                    self.sub_table.append({'id': id, 'name': element.string, 'type': var_type, 'kind': 'local', 'index': local_index})
                    local_index += 1

    def get_local_vars(self, id):
        return self.get_vars(id, 'local')

    def get_argument_vars(self):
        return self.get_vars(id, 'argument')

    def get_vars(self, id, name):
        for item in self.sub_table:
            if item.id == id and item.name == name:
                return (item.kind, item.index)

    def get_vars(self, id, type):
        args = []
        for item in self.sub_table:
            if item.id == id and item.type == type:
                args.append(item)
        return args



