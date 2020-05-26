import re
import os



def getLines(src):
    with open(src, 'r') as file:
        lines = file.readlines()
        print('getLine line size is ',len(lines))
        # print(lines)
        return lines

def getValidLines(src):
    lines = getLines(src)
    validLines = []
    for line in lines:
        #全为空白则无效
        if re.match(r'^\s*$', line):
            continue
        #//打头则无效
        if re.match(r'^\s*//', line):
            continue
        line = re.sub(r'//.*', '', line)
        line = line.strip()
        validLines.append(line.strip())
    print('getValidLines line size is ', len(validLines))
    print(validLines)
    return validLines

predefinedInstructions = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'Screen': 16384,
    'KBD': 24576,
}


def tranlateA(instruction):
    ins = instruction.replace('@','')
    isInt = re.match('^\d+$', ins)
    if isInt:
        return getBinValue16(ins)
    else:
        return translateVar(ins)

varAddress = 16
def translateVar(ins):
    global varAddress
    insValue = predefinedInstructions.get(ins, '')
    # print('ins', ins)
    # 未找到地址则添加进去
    if insValue == '':
        dicPair = {ins: varAddress}
        # print('dicPair', dicPair)
        predefinedInstructions.update(dicPair)
        varAddress = varAddress + 1
        return getBinValue16(varAddress)
    else:
        return getBinValue16(insValue)


def getBinValue16(intValue):
    value = bin(intValue)
    value =value.replace('b','')
    return value.zfill(16)

def getAflag(ins):
    ins = ins.replace(' ', '')
    isMatch = re.search(r'=.*M', ins)
    if isMatch:
        return '1'
    else:
        return '0'


def getCalculateFlag(ins):
    dic = {
        '0': '101010',
        '1': '111111',
        '-1': '111010',
        'D': '001100',
        'A': '110000',
        'M': '110000',
        '!D': '001101',
        '!A': '110001',
        '!M': '110001',
        '-D': '001111',
        '-A': '110011',
        '-M': '110011',
        'D+1': '011111',
        'A+1': '110111',
        'M+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'D+A': '000010',
        'D+M': '000010',
        'D-A': '010011',
        'D-M': '010011',
        'A-D': '000111',
        'M-D': '000111',
        'D&A': '000000',
        'D&M': '000000',
        'D|A': '010101',
        'D|M': '010101',
    }
    ins = ins.replace(' ', '')
    matchValue1 = re.findall(r'=(.*)', ins)
    matchValue2 = re.findall(r'(.*);', ins)
    # print('matchValue', matchValue)
    if len(matchValue1) != 0 :
        return dic.get(matchValue1[0], '000000')
    elif len(matchValue2) != 0:
        return dic.get(matchValue2[0], '000000')
    else:
        return '000000'

def getDestination(ins):
    dic = {
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111',
    }
    ins = ins.replace(' ', '')
    matchValue = re.findall(r'(.*)=', ins)
    # print('matchValue', matchValue)
    if len(matchValue) == 0:
        return '000'
    else:
        return dic.get(matchValue[0], '000')

getDestination('M=D+M')

def getJump(ins):
    dic = {
        'D;JGT': '001',
        'D;JEQ': '010',
        'D;JGE': '011',
        'D;JLT': '100',
        'D;JNE': '101',
        'D;JLE': '110',
        '0;JMP': '111',
    }
    ins = ins.replace(' ', '')
    return dic.get(ins, '000')

def translateC(instruction):
    aflag = getAflag(instruction)
    calculateFlag = getCalculateFlag(instruction)
    destination = getDestination(instruction)
    jump = getJump(instruction)
    return '111' + aflag + calculateFlag + destination + jump

def getInstruction(src):
    validLines = getValidLines(src)
    lines = []
    index = 0
    for line in validLines:
        line = validLines[index]
        if re.match(r'^\s*@', line):
            lines.append({'index': index, 'type': 'A', 'value': tranlateA(line)})
            index = index + 1
        elif re.match(r'^\(.+\)$', line):
            lines.append({'index': index, 'type': 'L', 'value': line})
        else:
            lines.append({'index': index, 'type': 'C', 'value': translateC(line)})
            index = index + 1

    print('getInstruction line size is ', len(lines))
    print(lines)
    return lines

def generateBinFile(src):
    path = os.path.dirname(src)
    print('path', path)
    fileName = os.path.basename(src)
    fileName = re.findall(r'(.*)\.', fileName)[0]

    print('fileName', fileName)
    newFileName = fileName + '.hack'
    lines = getInstruction(src)
    with open(path + '/' + newFileName, 'w+') as file:
        for line in lines:
            file.write(line['value'] + '\n')






fileSrc = 'D:/program/nand2tetris/06/add/Add.asm'
# getValidLines(fileSrc)
# generateBinFile('D:/program/nand2tetris/06/add/Add.asm')
generateBinFile('D:/program/nand2tetris/06/max/Max.asm')