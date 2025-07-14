from enum import Enum
from pathlib import Path
from dataclasses import dataclass


class CommandType(Enum):
    ARITHMETIC = 1
    PUSH = 2
    POP = 3
    LABEL = 4
    GOTO = 5
    IF = 6
    FUNCTION = 7
    RETURN = 8
    CALL = 9


@dataclass
class VMCommand:
    type: CommandType
    arg1: str
    arg2: int = None


class Parser:
    def __init__(self, input_file: Path):
        self.input_file = input_file
        self.command_type: CommandType = None

    def __enter__(self):
        self.file = open(self.input_file, 'r')
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.file:
            self.file.close()

    def __iter__(self):
        return self
    
    def __next__(self):
        line = next(self.file)
        splat = line.strip().split()
        command = splat[0]

        if command in ['push', 'pop']:
            return VMCommand(
                type=CommandType.PUSH if command == 'push' else CommandType.POP,
                arg1=splat[1],
                arg2=splat[2]
            )
        
        elif command in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return VMCommand(
                type=CommandType.ARITHMETIC,
                arg1=command
            )


segment2name = {
    'local': 'LCL',
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT',
    'temp': 'TEMP',
}

class CodeWriter:
    def __init__(self, output_file: Path):
        self.output_file = output_file

    def __enter__(self):
        self.file = open(self.output_file, 'w')
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.file:
            self.file.close()

    def write_arithmetic(self, command: str) -> None:
        pass

    def write_push_pop(self, command, segment: str, index: int) -> None:
        name = segment2name[segment]

        if command == CommandType.PUSH:
            # D = segment[index]
            self._write(f'@{name}')
            self._write(f'D=A')
            self._write(f'@{index}')
            self._write(f'A=D+A')
            self._write(f'D=M')
            # RAM[SP] = D
            self._write(f'@SP')
            self._write(f'A=M')
            self._write(f'M=D')
            # SP++
            self._write(f'@SP')
            self._write(f'M=M+1')

        elif command == CommandType.POP:
            # R13 = segment + index
            self._write(f'@{name}')
            self._write(f'D=A')
            self._write(f'@{index}')
            self._write(f'D=D+A')
            self._write(f'@R13')
            self._write(f'M=D')
            # Decrement stack pointer and go to it
            self._write(f'@SP')
            self._write(f'AM=M-1')
            # D = RAM[SP]
            # self._write(f'@SP')
            # self._write(f'A=M')
            self._write(f'D=M')
            # segment[index] = value @R13
            self._write(f'@R13')
            self._write(f'A=M')
            self._write(f'M=D')            


    def _write(self, text: str) -> None:
        self.file.write(text + '\n')


class VMTranslator:
    def __init__(self, input_file: str):
        input_path = Path(input_file)
        output_path = input_path.with_suffix('.asm')

        with Parser(input_file) as parser, CodeWriter(output_path) as writer:
            for cmd in parser:
                print(f'Parsed {cmd.type} command with args: {(cmd.arg1, cmd.arg2)}')

                if cmd.type in [CommandType.PUSH, CommandType.POP]:
                    writer.write_push_pop(command=cmd.type, segment=cmd.arg1, index=cmd.arg2)


if __name__ == '__main__':
    VMTranslator('testfiles/Test.vm')
