from enum import Enum
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Callable

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
        line = ''
        while line == '' or line.startswith('//'):
            line = next(self.file).strip()            

        splat = line.split()
        command = splat[0]

        if command in ['push', 'pop']:
            return VMCommand(
                type=CommandType.PUSH if command == 'push' else CommandType.POP,
                arg1=splat[1],
                arg2=int(splat[2])
            )
        
        elif command in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return VMCommand(
                type=CommandType.ARITHMETIC,
                arg1=command
            )


segment2symbol = {
    'local': 'LCL',
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT',
}

class CodeWriter:
    POINTER_OFFSET = 3
    TEMP_OFFSET = 5
    
    def __init__(self, output_file: Path):
        self.output_file = output_file
        self.static_name = output_file.stem
        self.next_label = self._create_label_maker()

    def __enter__(self):
        self.file = open(self.output_file, 'w')
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.file:
            self._write_end_loop()
            self.file.close()

    def write_arithmetic(self, command: str) -> None:
        if command == 'add':
            self._write_binary_operation('+')

        if command == 'sub':
            self._write_binary_operation('-')
        
        if command == 'neg':
            self._write_unary_operation('-')
        
        if command == 'eq':
            self._write_compare_operation('==')

        if command == 'gt':
            self._write_compare_operation('>')
        
        if command == 'lt':
            self._write_compare_operation('<')

        if command == 'and':
            self._write_binary_operation('&')

        if command == 'or':
            self._write_binary_operation('|')
        
        if command == 'not':
            self._write_unary_operation('!')

    def write_push_pop(self, command, segment: str, index: int) -> None:
        if command == CommandType.PUSH:
            if segment == 'constant':
                self._push_constant_to_stack(constant=index)
            else:
                self._push_memory_to_stack(segment, index)

        elif command == CommandType.POP:               
            self._pop_stack_to_memory(segment, index)

    def _write_binary_operation(self, op: str) -> None:
        self._pop_stack_to_variable('R13')
        self._pop_stack_to_d()
        
        self._set_address('R13')
        self._write(f'D=D{op}M')

        self._push_d_to_stack()

    def _write_unary_operation(self, op: str) -> None:
        self._pop_stack_to_d()        
        self._write(f'D={op}D')
        self._push_d_to_stack()

    def _write_compare_operation(self, op: str) -> None:
        jump_op = {
            '==': 'JEQ',
            '>':  'JGT',
            '<':  'JLT',
        }[op]

        self._pop_stack_to_variable('R13')
        self._pop_stack_to_d()

        ## D -= R13
        self._set_address('R13')
        self._write('D=D-M')

        # If operation is true, jump to TRUE label
        true_label = self.next_label('TRUE')
        self._set_address(true_label)
        self._write(f'D;{jump_op}')

        # False block
        false_label = self.next_label('FALSE')
        self._write_label(false_label)
        self._write('D=0')
        self._push_d_to_stack()
        after_label = self.next_label('AFTER')
        self._set_address(after_label)
        self._write('0;JMP')

        # True block
        self._write_label(true_label)
        self._write('D=-1')
        self._push_d_to_stack()

        self._write_label(after_label)

    def _push_constant_to_stack(self, constant: int) -> None:
        self._store_value_in_d(constant)
        self._push_d_to_stack()

    def _push_memory_to_stack(self, segment: str, index: int) -> None:
        if segment == 'pointer':
            self._set_address(self.POINTER_OFFSET + index)
        elif segment == 'temp':
            self._set_address(self.TEMP_OFFSET + index)
        elif segment == 'static':
            self._set_address(f'{self.static_name}.{index}')
        else:
            symbol = segment2symbol[segment]
            self._set_address(symbol)
            self._write(f'D=M')
            self._set_address(index)
            self._write(f'A=D+A')

        self._write(f'D=M')
        self._push_d_to_stack()

    def _push_d_to_stack(self) -> None:
        self._write_d_to_ram_at_sp()
        self._write_increment_sp()

    def _pop_stack_to_memory(self, segment: str, index: int) -> None:
        # D = segment + index
        if segment == 'pointer':
            self._store_value_in_d(self.POINTER_OFFSET + index)
        elif segment == 'temp':
            self._store_value_in_d(self.TEMP_OFFSET + index)
        elif segment == 'static':
            self._store_value_in_d(f'{self.static_name}.{index}')
        else:
            symbol = segment2symbol[segment]
            self._set_address(symbol)
            self._write(f'D=M')
            self._set_address(index)
            self._write(f'D=D+A')

        # R13 = D
        self._set_address('R13')
        self._write(f'M=D')
        
        # D = RAM[SP]
        self._pop_stack_to_d()

        # RAM[R13] = D
        self._set_address('R13')
        self._write(f'A=M')
        self._write(f'M=D')

    def _pop_stack_to_variable(self, name: str) -> None:
        self._pop_stack_to_d()
        self._set_address(name)
        self._write('M=D')

    def _pop_stack_to_d(self) -> None:
        self._write_decrement_sp()
        self._write_ram_at_sp_to_d()

    def _store_value_in_d(self, value: int | str) -> None:
        self._set_address(value)
        self._write(f'D=A')

    def _write_ram_at_sp_to_d(self) -> None:
        self._set_address('SP')
        self._write(f'A=M')
        self._write(f'D=M')

    def _write_d_to_ram_at_sp(self) -> None:
        self._set_address('SP')
        self._write(f'A=M')
        self._write(f'M=D')

    def _write_increment_sp(self) -> None:
        self._set_address('SP')
        self._write(f'M=M+1')

    def _write_decrement_sp(self) -> None:
        self._set_address('SP')
        self._write(f'M=M-1')

    def _write_label(self, label: str) -> None:
        self._write(f'({label})')

    def _write_end_loop(self) -> None:
        end_label = self.next_label('END')
        self._write_label(end_label)
        self._set_address(end_label)
        self._write(f'0;JMP')

    def _set_address(self, addr: int | str) -> None:
        self._write(f'@{addr}')

    def _write(self, text: str) -> None:
        self.file.write(text + '\n')

    def _generate_label(self) -> None:
        return ''.join(random.choices(string.ascii_uppercase, k=10))

    def _create_label_maker(self) -> Callable[[], str]:
        index = -1

        def next_label(prefix: str = 'LABEL') -> str:
            nonlocal index
            index += 1
            return f'{prefix}{index}'
        
        return next_label



class VMTranslator:
    def __init__(self, input_file: str):
        input_path = Path(input_file)
        output_path = input_path.with_suffix('.asm')

        with Parser(input_file) as parser, CodeWriter(output_path) as writer:
            for cmd in parser:
                print(f'Parsed {cmd.type} command with args: {(cmd.arg1, cmd.arg2)}')

                if cmd.type in [CommandType.PUSH, CommandType.POP]:
                    writer.write_push_pop(
                        command=cmd.type,
                        segment=cmd.arg1,
                        index=cmd.arg2,
                    )

                elif cmd.type == CommandType.ARITHMETIC:
                    writer.write_arithmetic(
                        command=cmd.arg1
                    )


if __name__ == '__main__':
    import sys
    src_file = sys.argv[1]
    VMTranslator(src_file)
