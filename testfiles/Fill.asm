(START)
// Initialize the screen memory pointer
// (n = SCREEN)
@SCREEN
D=A
@n
M=D

(LOOP)
// Loop iteration
// If RAM[KBD] == 0, set fill value to 0, otherwise -1
@KBD
D=M

@WHITE
D;JEQ

// Fill the word black
D=-1
@CONTINUE
0;JMP

(WHITE)
// Fill the word white
D=0

(CONTINUE)
@n
A=M // change address to whatever's at n
M=D // store the black or white value there

// n = n + 1
@n
DM=M+1

@KBD
D=D-A

@START
D;JEQ

// goto LOOP
@LOOP
0;JMP
