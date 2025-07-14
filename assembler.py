from enum import Enum
from pathlib import Path


class InstructionType(Enum):
    A_INSTRUCTION = 0
    C_INSTRUCTION = 1
    L_INSTRUCTION = 2


class Parser:
    def __init__(self, asm_path):
        with open(asm_path, 'r') as f:
            self.lines = f.readlines()

        self.current_instruction = None
    
    @property
    def has_more_lines(self):
        return len(self.lines) > 0
    
    def advance(self):
        while True:
            if len(self.lines) == 0:
                return
            
            line = self.lines.pop(0).strip()
            if line != '' and not line.startswith('//'):
                # Remove any trailing comments
                self.current_instruction = line.split()[0]
                break
    
    @property
    def instruction_type(self):
        if self.current_instruction.startswith('@'):
            return InstructionType.A_INSTRUCTION
        elif self.current_instruction.startswith('('):
            return InstructionType.L_INSTRUCTION
        else:
            return InstructionType.C_INSTRUCTION

    @property
    def symbol(self):
        if self.instruction_type == InstructionType.L_INSTRUCTION:
            # L-instruction: return the text between "(" at the
            # beginning and the first ")"
            return self.current_instruction.split(')')[0][1:]
        else:
            # A-instruction: Return text after "@" at the beginning
            return self.current_instruction[1:]

    # For the following three methods: C-instructions are formatted
    # dest=comp;jump

    @property
    def dest(self):
        if '=' not in self.current_instruction:
            return None
        
        return self.current_instruction.split('=')[0]

    @property
    def comp(self):
        instruction = self.current_instruction
        
        if '=' in instruction:
            instruction = instruction.split('=')[1]
        
        if ';' in instruction:
            instruction = instruction.split(';')[0]
        
        return instruction
    
    @property
    def jump(self):
        if ';' not in self.current_instruction:
            return None
        
        return self.current_instruction.split(';')[1]


class Code:
    def dest(s):
        if s is None:
            return '000'

        a_bit = '1' if 'A' in s else '0'
        d_bit = '1' if 'D' in s else '0'
        m_bit = '1' if 'M' in s else '0'

        return a_bit + d_bit + m_bit
    
    def comp(s):
        r, a = ('M', '1') if 'M' in s else ('A', '0')
        comp2binary = {
            '0':    '101010',
            '1':    '111111',
            '-1':   '111010',
            'D':    '001100',
            r:      '110000',
            '!D':   '001101',
            '!'+r:  '110001',
            '-D':   '001111',
            '-'+r:  '110011',
            'D+1':  '011111',
            r+'+1': '110111',
            'D-1':  '001110',
            r+'-1': '110010',
            'D+'+r: '000010',
            'D-'+r: '010011',
            r+'-D': '000111',
            'D&'+r: '000000',
            'D|'+r: '010101', 
        }

        cccccc = comp2binary[s]
        return a + cccccc

    def jump(s):
        return {
            None:  '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'
        }[s]


class SymbolTable(dict):
    def __init__(self):
        for i in range(16):
            self[f'R{i}'] = i
        
        self['SP'] = 0
        self['LCL'] = 1
        self['ARG'] = 2
        self['THIS'] = 3
        self['THAT'] = 4

        self['SCREEN'] = 16384
        self['KBD'] = 24576


class HackAssembler:
    def __init__(self):
        self.symbol_table = SymbolTable()
    
    def translate(self, asm_path):
        self._first_pass(asm_path)
        self._second_pass(asm_path)
    
    def _first_pass(self, asm_path):
        line_number = 0
        parser = Parser(asm_path)
        while parser.has_more_lines:
            parser.advance()

            if parser.instruction_type == InstructionType.L_INSTRUCTION:
                self.symbol_table[parser.symbol] = line_number
            else:
                line_number += 1
    
    def _second_pass(self, asm_path):
        next_available_address = 16
        hack_path = Path(asm_path).with_suffix('.hack')
        with open(hack_path, 'w') as f:
            parser = Parser(asm_path)
            while parser.has_more_lines:
                parser.advance()

                if parser.instruction_type == InstructionType.C_INSTRUCTION:
                    acccccc = Code.comp(parser.comp)
                    ddd = Code.dest(parser.dest)
                    jjj = Code.jump(parser.jump)
                    f.write(f'111{acccccc}{ddd}{jjj}\n')
                elif parser.instruction_type == InstructionType.A_INSTRUCTION:
                    if not parser.symbol.isdigit():
                        if not parser.symbol in self.symbol_table:
                            self.symbol_table[parser.symbol] = next_available_address
                            next_available_address += 1
                        
                        address = str(self.symbol_table[parser.symbol])
                    else:
                        address = parser.symbol
                    
                    f.write('0' + f'{int(address):015b}\n')
                else: # L-instructions were processed in the first pass
                    continue
                

if __name__ == '__main__':
    assembler = HackAssembler()
    assembler.translate('testfiles/Test.asm')