class Instruction:

    def comment(self, list):
        code = []
        if len(list) == 1:
            code.append('//========{}'.format(list[0]))
        elif len(list) == 2:
            code.append('//========{} {}'.format(list[0], list[1]))
        elif len(list) == 3:
            code.append('//========{} {} {}'.format(list[0], list[1], list[2]))
        return code