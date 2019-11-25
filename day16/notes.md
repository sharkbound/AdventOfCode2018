# goal
Ignoring the opcode numbers, how many samples in your puzzle input behave like three or more opcodes?

# samples
1. start with `After`
2. have space separate numbers for register values
3. end with `Before`

# example
9 2 1 2

* possibilies:
    * MULR - B=2 * C=1 == 2 
    
means that opcode 9 was executed with A=2, B=1, and C=2. Opcode 9 could be any of the 16 opcodes listed above, but only three of them behave in a way that would cause the result shown in the sample:

    Opcode 9 could be mulr: register 2 (which has a value of 1) times register 1 (which has a value of 2) produces 2, which matches the value stored in the output register, register 2.
    Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1 produces 2, which matches the value stored in the output register, register 2.
    Opcode 9 could be seti: value 2 matches the value stored in the output register, register 2; the number given for B is irrelevant.
