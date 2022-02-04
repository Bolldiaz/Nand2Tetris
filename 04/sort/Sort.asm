// This file is part of nand2tetris, as taught in The Hebrew University,
// and was written by Aviv Yaish, and is published under the Creative 
// Common Attribution-NonCommercial-ShareAlike 3.0 Unported License 
// https://creativecommons.org/licenses/by-nc-sa/3.0/

// An implementation of a sorting algorithm. 
// An array is given in R14 and R15, where R14 contains the start address of the 
// array, and R15 contains the length of the array. 
// You are not allowed to change R14, R15.
// The program should sort the array in-place and in descending order - 
// the largest number at the head of the array.
// You can assume that each array value x is between -16384 < x < 16384.
// You can assume that the address in R14 is at least >= 2048, and that 
// R14 + R15 <= 16383. 
// No other assumptions can be made about the length of the array.
// You can implement any sorting algorithm as long as its runtime complexity is 
// at most C*O(N^2), like bubble-sort. 

// psuedo:
// for j=1 to RAM[R15];
//     key = RAM[R14 + j]
//     i = j-1

//     while i >= 0 RAM[R14 + i] > key
//         RAM[R14 + i + 1] = RAM[R14 + i]
//         i--
//     RAM[R14 + i + 1] = key

// insertion-sort:

@j
M=1     // j = 1

(OUTLOOP)
    @R15
    D=M
    @j
    D=D-M
    @END
    D;JEQ   // if j==RAM[R15] (array length) goto END

    @R14
    D=M
    @j
    A=D+M
    D=M
    @key
    M=D         // key = RAM[R14 + j] (arr[j])
    
    @j
    D=M-1
    @i
    M=D         // i = j-1

    (INLOOP)
        @i
        D=M
        @INSTOP
        D;JLT   // if i < 0 goto INSTOP

        @R14
        D=M
        @i
        A=D+M
        D=M
        @key
        D=M-D
        @INSTOP
        D;JLE   // if key <= RAM[R14 + i] goto INSTOP

        @i
        D=M+1
        @R14
        D=M+D
        @add
        M=D

        @R14
        D=M
        @i
        A=M+D
        D=M     // D = RAM[R14 + i] (arr[i])
        
        @add
        A=M
        M=D     // RAM[R14 + i + 1] = RAM[R14 + i] (arr[i+1]=arr[i])

        @i
        M=M-1   // i--

        @INLOOP
        0;JMP // goto INLOOP
    (INSTOP)
    @R14
    D=M+1
    @i
    D=M+D
    @add
    M=D

    @key
    D=M
    @add
    A=M
    M=D         // RAM[R14 + i + 1] = key

    @j
    M=M+1       // j++
    
    @OUTLOOP
    0;JMP

(END)
    @END
    0;JMP