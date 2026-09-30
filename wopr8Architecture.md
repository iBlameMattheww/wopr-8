# WOPR-8 Custom 8-bit CPU Architecture


## Core Architecture
| Property | Definition |
| ----------- | ----------- |
| Data width | 8 bits |
| Integer representation | Two's complement |
| General-purpose registers | 8 registers, R0-R7, each 8 bits|
| Instruction width | 16 bits, fixed width |
| Primary opcode width | 5 bits |
| Data address width | 8 bits |
| PC width | 11 bits |
| Instruction address space | 2^11 = 2048 instruction addresses |
| Program storage | 2048 x 16 = 32768 bits = 4 KiB |


## Special Registers
| Name | Width | Reset/Initial Value |
| ----------- | ----------- | ----------- |
| PC | 11 bits | implementation reset vector |
| SP | 8 bits | 0xDF |
| PSR | 8 bits | 00000000 |


## Processor Status Register (PSR)
| Bit | Name |
| ----------- | ----------- |
| 0 | Z (Zero flag) |
| 1 | C (Carry) |
| 2 | STACK_UNDERLOW |
| 3 | STACK_OVERFLOW |
| 4 | ILLEGAL_INSTRUCTION |
| 5 | HALTED |
| 6 | ILLEGAL_MEMORY_ADDRESS |
| 7 | RESERVED |


## Memory Architecture
### Data Memory Map
| Range | Size | Purpose |
| ----------- | ----------- | ----------- |
| 0x00 - 0x7F | 128 bytes | General/static program data |
| 0x80 - 0xDF | 96 bytes | Stack region |
| 0xE0 - 0xFF | 32 bytes | Reserved for memory-mapped I/O |

General data conventionally grows upward from 0x00. The stack begins at 0xDF and grows downward.
The fixed stack floor for WOPR-8 v1 is 0x80.

### Instruction Memory
Instruction memory is separate from data memory. The 11-bit program counter directly identifies one of
2048 fixed-width 16-bit instruction words.


## Instruction Formats
All instructions are exactly 16 bits. The 5-bit primary opcode occupies bits [15:11].

### R Format
| [15:11] | [10:8] | [7:5] | [4:2] | [1] | [0] |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| opcode (5) | Rd (3) | Rs (3) | shamt (3) | dir (1) | reserved (1) |

For ordinary R-format instructions, shamt, dir, and the reserved bit are encoded as zero unless the
instruction explicitly uses them. For SHIFT, shamt is a 3-bit shift amount (0–7), dir=0 selects left shift,
and dir=1 selects right shift. Bit 0 remains reserved and must be zero.

### I Format
| [15:11] | [10:8] | [7:0] | 
| ----------- | ----------- | ----------- | 
| opcode (5) | Rd (3) | immediate (8) |

### J Format
| [15:11] | [10:0] | 
| ----------- | ----------- |
| opcode (5) | address (11) |


## Calling Convention / ABI
| Register | Role | Preservation | 
| ----------- | ----------- | ----------- | 
| R0 | Argument 0 / return call | Caller-saved |
| R1 | Argument 1 | Caller-saved |
| R2 | Argument 2 | Caller-saved |
| R3 | Temporary T0 | Caller-saved |
| R4 | Temporary T1 | Caller-saved |
| R5 | Temporary T2 | Caller-saved |
| R6 | Temporary T3 | Caller-saved |
| R7 | Saved register S0 | Callee-saved |

A callee that modifies R7 must restore its incoming value before returning, typically using PUSH/POP.
No dedicated frame pointer is required. Recursive and nested calls are supported because each CALL
pushes its own return address to the stack.




