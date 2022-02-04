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

@SCREEN
D=A
@arr
M=D     // arr = 16384 (screen's base address)

(KEYCHECK)
    @8192       // #chunks to turned black         
    D=A
    @n
    M=D-1         // n = 8191
    @KBD
    D=M
    @PRINTWHITE
    D;JEQ         // if KEYBOARD=0 goto PRINTWHITE

    
    (PRINTBLACK)
        @n
        D=M
        @KEYCHECK
        D;JLT       // if n<0 goto KEYCHECK
        
        @arr
        D=M
        @n
        A=M+D
        M=-1        // RAM[SCREEN+n] = black

        @n
        M=M-1       // n--
        
        @PRINTBLACK
        0;JMP
    
    (PRINTWHITE)
        @n
        D=M
        @KEYCHECK
        D;JLT       // if n<0 goto KEYCHECK
        
        @arr
        D=M
        @n
        A=M+D
        M=0        // RAM[SCREEN+n] = white

        @n
        M=M-1       // n--
        
        @PRINTWHITE
        0;JMP


