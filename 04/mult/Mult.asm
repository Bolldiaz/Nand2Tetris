// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// i, R2 = 0
@sum
M=0
@i
M=0

(LOOP)
    // if i==R0 goto STOP
    @R0
    D=M
    @i
    D=D-M
    M=M+1 // i++
    @STOP
    D;JEQ

    // sum += R1
    @R1
    D=M
    @sum
    M=M+D
    @LOOP
    0;JMP
(STOP)
// R2 = sum
@sum
D=M
@R2
M=D

(END)
    @END
    0;JMP