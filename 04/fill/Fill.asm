// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(BEGIN)
////////////根据键盘输入值决定屏幕颜色//////////////
////////////获取键盘输入值

//获取键盘输入值
@KBD
D=M

///////////根据输入值决定屏幕颜色（将颜色保存到screenValue，以便渲染程序处理）
@WHITE
D; JEQ

//缓存黑色
@screenValue
M=-1

@DISPLAY
0; JMP

(WHITE)
//缓存白色
@screenValue
M=0

(DISPLAY)
////////////开始渲染屏幕//////////////

////////////第一步：构造循环块（初始化循环总次数，循环计数器）
//初始化loop次数loop_amount，8191次
@8191
D=A

@loop_amount
M=D

//初始化计数器
@0
D=A

@count
M=D

///////////第二步：定位要渲染的屏幕地址
(DISPLAY_START)
//定位地址
@SCREEN
D=A

@count
D=D+M

@address
M=D

///////////第三步：开始渲染
@screenValue
D=M

@address
A=M
M=D

//////////第四步：推进计数块
//计数器+1
@count
M=M+1

//循环次数-1
@loop_amount
M=M-1
D=M

//循环次数未用完则跳回，继续渲染
@DISPLAY_START
D;JGE

//重置键盘输入值
//@KBD
//M=0

@BEGIN
0; JMP
