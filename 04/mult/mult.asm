// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// a*b 相当于b个a相加
////////////初始化循环参数，n，sum，a
//循环次数n
@R1
D=M

@n
M=D

//累加基数a
@R0
D=M

@a
M=D

//求和结果
@R2
M=0

(LOOP)
/////////////开始循环
//若循环次数<=0则退出
@n
D=M

@END
D;JLE

//剩余循环次数-1
@n
M=M-1

//累加结果
@a
D=M

@R2
M=D+M

@LOOP
0;JMP

(END)
@END
0;JMP
