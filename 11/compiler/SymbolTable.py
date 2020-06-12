from bs4 import BeautifulSoup
from Log import logger

class SymbolTable:

    def __init__(self, soup):
        self.class_table = []
        self.local_table = []
        self.arg_table = []
        self.all_table = []
        self.soup = soup
        self.class_name = self.soup.find_all()[2].text
        self.parse()

    def get_class_table(self):
        return self.class_table

    def get_sub_table(self):
        return self.local_table

    def parse(self):
        file = []
        self.parse_class_vars()
        self.parse_local_vars()
        self.parse_argument_vars()
        self.all_table.extend(self.class_table)
        self.all_table.extend(self.local_table)
        self.all_table.extend(self.arg_table)
        logger.info('类变量 {} 个'.format(len(self.class_table)))
        for item in self.class_table:
            logger.info(item)
        logger.info('私有变量 {} 个'.format(len(self.local_table)))
        for item in self.local_table:
            logger.info(item)
        logger.info('参数变量 {} 个'.format(len(self.arg_table)))
        for item in self.arg_table:
            logger.info(item)

    def parse_class_vars(self):
        class_var_decs = self.soup.find_all('classVarDec')
        static_index = 0
        field_index = 0

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
                elif var_kind == 'field':
                    self.class_table.append({'id': self.class_name,'name': element.string, 'type': var_type, 'kind': 'field', 'index': field_index})
                    field_index += 1
                else:
                    logger.error('解析类变量出错，未知的变量类型{}'.format(element))
                    raise Exception('解析类变量出错，未知的变量类型{}'.format(element))

    def parse_local_vars(self):
        sub_var_decs = self.soup.find_all('varDec')
        # logger.debug(sub_var_decs)
        local_index = 0
        pre_id = ''
        for sub_var_dec in sub_var_decs:
            # 类名+方法名作为id
            sub_name = sub_var_dec.parent.parent.find_all()[2].text
            id = self.class_name + '.' + sub_name
            # 若id变化，表示进入新方法，则变量的所索引值需要重置
            if id != pre_id:
                local_index = 0
                pre_id = id
            all_elements = sub_var_dec.find_all()
            # 第二个元素表示变量类型（int, boolean, char, className）
            var_type = all_elements[1].string
            # 只取变量名称部分
            all_elements = all_elements[2:]
            for element in all_elements:
                if element.text in [',', ';']:
                    continue
                self.local_table.append({'id': id, 'name': element.text, 'type': var_type, 'kind': 'local', 'index': local_index})
                local_index += 1

    def parse_argument_vars(self):
        subroutine_decs = self.soup.find_all('subroutineDec')
        for subroutine_dec in subroutine_decs:
            # logger.info(subroutine_dec)
            # 进入新的方法，重置索引值
            argument_index = 0
            # 类名+方法名作为id
            sub_name = subroutine_dec.find('identifier').text
            id = self.class_name + '.' + sub_name
            param_pair_list = subroutine_dec.find('parameterList').find_all()
            if len(param_pair_list) == 0:
                continue
            var_type = param_pair_list[0].text
            var_name = param_pair_list[1].text
            self.arg_table.append(
                {'id': id, 'name': var_name, 'type': var_type, 'kind': 'argument', 'index': argument_index})
            argument_index += 1

            length = int((len(param_pair_list) - 2) / 3)
            for index in range(length):
                var_type = param_pair_list[index * 3 + 3].text
                var_name = param_pair_list[index * 3 + 4].text
                self.arg_table.append({'id': id, 'name': var_name, 'type': var_type, 'kind': 'argument', 'index': argument_index})
                argument_index += 1


    def get_local_vars(self, id):
        return self.filte_sub_vars(id, 'local')

    def get_local_vars_amount(self, id):
        return len(self.filte_sub_vars(id, 'local'))

    def get_argument_vars(self):
        return self.filte_sub_vars(id, 'argument')

    def filte_sub_vars(self, id, kind):
        args = []
        for item in self.all_table:
            if item['id'] == id and item['kind'] == kind:
                args.append(item)
        return args

    def get_var_info(self, id, name):
        for item in self.all_table:
            if item['id'] == id and item['name'] == name:
                return (item['kind'], item['index'])
        logger.error('根据id：{}，name：{}，未找到对应变量'.format(id, name))
        raise Exception('根据id：{}，name：{}，未找到对应变量'.format(id, name))



