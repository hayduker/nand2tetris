from gates import *
from arithmetic import Inc16


##########################################################
# Up to now, all of the gates we've defined have been
# stateless (i.e. time-independent), and this is why they
# can be represented in a purely-functional manner. We now
# begin defining sequential logic gates, those which carry
# state and thus whose outputs depend not only on their
# inputs at the current time but also on those inputs
# which came previously.
#
# Purely-functional programming becomes inconvenient here,
# so these sequential logic gates are defined using Python
# classes which define an "eval" method for simulating
# running the chips with a given set of inputs. The eval
# methods take the place of the functional definitions
# above and attempt to resemble the nand2tetris HDL in
# in that the only operations made available are calls to
# previously-defined gates and naming the outputs of those
# calls. In a sense, this code (and definitely the HDL on
# which it is based) is simply supposed to enumerate how
# chips are connected to each other physically.
#
# At some point it may be nice to rewrite the above gates
# as classes as well. This would give all the gates the
# same "structure" in the Python code and would make it
# easier to write unit tests other tooling for the
# hardware simulation. Care must be taken here though not
# to mix up the HDL-like specification with this tooling
# code, as it would be all-too-easy to start using higher-
# level abstractions where we should only be using gates
# we've previously defined connected to one another.
##########################################################

class DFF:
    def __init__(self):
        self.q = 0
    
    def eval(self, inp):
        last_q = self.q
        self.q = inp
        return last_q


class Bit:
    def __init__(self):
        self.dff = DFF()
    
    def eval(self, inp, load):
        which = Mux(self.dff.q, inp, load)
        return self.dff.eval(which)

    @property
    def val(self):
        return self.dff.q

    def __str__(self):
        return str(self.dff.q)
    
    def __repr__(self):
        return str(self)


class Register:
    def __init__(self):
        self.bit0  = Bit()
        self.bit1  = Bit()
        self.bit2  = Bit()
        self.bit3  = Bit()
        self.bit4  = Bit()
        self.bit5  = Bit()
        self.bit6  = Bit()
        self.bit7  = Bit()
        self.bit8  = Bit()
        self.bit9  = Bit()
        self.bit10 = Bit()
        self.bit11 = Bit()
        self.bit12 = Bit()
        self.bit13 = Bit()
        self.bit14 = Bit()
        self.bit15 = Bit()
    
    def eval(self, inp, load):
        out0  = self.bit0.eval(inp[15], load)
        out1  = self.bit1.eval(inp[14], load)
        out2  = self.bit2.eval(inp[13], load)
        out3  = self.bit3.eval(inp[12], load)
        out4  = self.bit4.eval(inp[11], load)
        out5  = self.bit5.eval(inp[10], load)
        out6  = self.bit6.eval(inp[9],  load)
        out7  = self.bit7.eval(inp[8],  load)
        out8  = self.bit8.eval(inp[7],  load)
        out9  = self.bit9.eval(inp[6],  load)
        out10 = self.bit10.eval(inp[5], load)
        out11 = self.bit11.eval(inp[4], load)
        out12 = self.bit12.eval(inp[3], load)
        out13 = self.bit13.eval(inp[2], load)
        out14 = self.bit14.eval(inp[1], load)
        out15 = self.bit15.eval(inp[0], load)

        return out15, out14, out13, out12, out11, out10, out9, out8, \
               out7, out6, out5, out4, out3, out2, out1, out0
    
    @property
    def val(self):        
        return (self.bit15.val, self.bit14.val, self.bit13.val, self.bit12.val,
                self.bit11.val, self.bit10.val, self.bit9.val, self.bit8.val,
                self.bit7.val,  self.bit6.val,  self.bit5.val,  self.bit4.val,
                self.bit3.val,  self.bit2.val,  self.bit1.val,  self.bit0.val)
        
    def __str__(self):
        return f'{self.bit15} {self.bit14} {self.bit13} {self.bit12} ' + \
               f'{self.bit11} {self.bit10} {self.bit9} {self.bit8} ' + \
               f'{self.bit7} {self.bit6} {self.bit5} {self.bit4} ' + \
               f'{self.bit3} {self.bit2} {self.bit1} {self.bit0}'
    
    def __repr__(self):
        return str(self)


class RAM8:
    def __init__(self):
        self.r0 = Register()
        self.r1 = Register()
        self.r2 = Register()
        self.r3 = Register()
        self.r4 = Register()
        self.r5 = Register()
        self.r6 = Register()
        self.r7 = Register()

    def eval(self, inp, load, addr):
        ld0, ld1, ld2, ld3, ld4, ld5, ld6, ld7 = DMux8Way(load, sel=addr)

        out0 = self.r0.eval(inp, ld0)
        out1 = self.r1.eval(inp, ld1)
        out2 = self.r2.eval(inp, ld2)
        out3 = self.r3.eval(inp, ld3)
        out4 = self.r4.eval(inp, ld4)
        out5 = self.r5.eval(inp, ld5)
        out6 = self.r6.eval(inp, ld6)
        out7 = self.r7.eval(inp, ld7)

        return Mux8Way16(out0, out1, out2, out3, out4, out5, out6, out7, sel=addr)
    
    def __str__(self):
        return f'{self.r0}\n{self.r1}\n{self.r2}\n{self.r3}\n' + \
               f'{self.r4}\n{self.r5}\n{self.r6}\n{self.r7}'

    def __repr__(self):
        return str(self)


class RAM64:
    def __init__(self):
        self.r0 = RAM8()
        self.r1 = RAM8()
        self.r2 = RAM8()
        self.r3 = RAM8()
        self.r4 = RAM8()
        self.r5 = RAM8()
        self.r6 = RAM8()
        self.r7 = RAM8()
    
    def eval(self, inp, load, addr):
        msb_addr = (addr[0], addr[1], addr[2])
        lsb_addr = (addr[3], addr[4], addr[5])

        ld0, ld1, ld2, ld3, ld4, ld5, ld6, ld7 = DMux8Way(load, sel=msb_addr)

        out0 = self.r0.eval(inp, ld0, lsb_addr)
        out1 = self.r1.eval(inp, ld1, lsb_addr)
        out2 = self.r2.eval(inp, ld2, lsb_addr)
        out3 = self.r3.eval(inp, ld3, lsb_addr)
        out4 = self.r4.eval(inp, ld4, lsb_addr)
        out5 = self.r5.eval(inp, ld5, lsb_addr)
        out6 = self.r6.eval(inp, ld6, lsb_addr)
        out7 = self.r7.eval(inp, ld7, lsb_addr)

        return Mux8Way16(out0, out1, out2, out3, out4, out5, out6, out7, sel=msb_addr)

    def __str__(self):
        return f'{self.r0}\n{self.r1}\n{self.r2}\n{self.r3}\n' + \
               f'{self.r4}\n{self.r5}\n{self.r6}\n{self.r7}'

    def __repr__(self):
        return str(self)


class RAM512:
    def __init__(self):
        self.r0 = RAM64()
        self.r1 = RAM64()
        self.r2 = RAM64()
        self.r3 = RAM64()
        self.r4 = RAM64()
        self.r5 = RAM64()
        self.r6 = RAM64()
        self.r7 = RAM64()
    
    def eval(self, inp, load, addr):
        msb_addr = (addr[0], addr[1], addr[2])
        lsb_addr = (addr[3], addr[4], addr[5], addr[6], addr[7], addr[8])

        ld0, ld1, ld2, ld3, ld4, ld5, ld6, ld7 = DMux8Way(load, sel=msb_addr)

        out0 = self.r0.eval(inp, ld0, lsb_addr)
        out1 = self.r1.eval(inp, ld1, lsb_addr)
        out2 = self.r2.eval(inp, ld2, lsb_addr)
        out3 = self.r3.eval(inp, ld3, lsb_addr)
        out4 = self.r4.eval(inp, ld4, lsb_addr)
        out5 = self.r5.eval(inp, ld5, lsb_addr)
        out6 = self.r6.eval(inp, ld6, lsb_addr)
        out7 = self.r7.eval(inp, ld7, lsb_addr)

        return Mux8Way16(out0, out1, out2, out3, out4, out5, out6, out7, sel=msb_addr)

    def __str__(self):
        return f'{self.r0}\n{self.r1}\n{self.r2}\n{self.r3}\n' + \
               f'{self.r4}\n{self.r5}\n{self.r6}\n{self.r7}'

    def __repr__(self):
        return str(self)


class RAM4K:
    def __init__(self):
        self.r0 = RAM512()
        self.r1 = RAM512()
        self.r2 = RAM512()
        self.r3 = RAM512()
        self.r4 = RAM512()
        self.r5 = RAM512()
        self.r6 = RAM512()
        self.r7 = RAM512()
    
    def eval(self, inp, load, addr):
        msb_addr = (addr[0], addr[1], addr[2])
        lsb_addr = (addr[3], addr[4], addr[5],
                    addr[6], addr[7], addr[8],
                    addr[9], addr[10], addr[11])

        ld0, ld1, ld2, ld3, ld4, ld5, ld6, ld7 = DMux8Way(load, sel=msb_addr)

        out0 = self.r0.eval(inp, ld0, lsb_addr)
        out1 = self.r1.eval(inp, ld1, lsb_addr)
        out2 = self.r2.eval(inp, ld2, lsb_addr)
        out3 = self.r3.eval(inp, ld3, lsb_addr)
        out4 = self.r4.eval(inp, ld4, lsb_addr)
        out5 = self.r5.eval(inp, ld5, lsb_addr)
        out6 = self.r6.eval(inp, ld6, lsb_addr)
        out7 = self.r7.eval(inp, ld7, lsb_addr)

        return Mux8Way16(out0, out1, out2, out3, out4, out5, out6, out7, sel=msb_addr)

    def __str__(self):
        return f'{self.r0}\n{self.r1}\n{self.r2}\n{self.r3}\n' + \
               f'{self.r4}\n{self.r5}\n{self.r6}\n{self.r7}'

    def __repr__(self):
        return str(self)


class RAM16K:
    def __init__(self):
        self.r0 = RAM4K()
        self.r1 = RAM4K()
        self.r2 = RAM4K()
        self.r3 = RAM4K()
    
    def eval(self, inp, load, addr):
        msb_addr = (addr[0], addr[1])
        lsb_addr = (addr[2], addr[3], addr[4],
                    addr[5], addr[6], addr[7],
                    addr[8], addr[9], addr[10],
                    addr[11], addr[12], addr[13])

        ld0, ld1, ld2, ld3 = DMux4Way(load, sel=msb_addr)

        out0 = self.r0.eval(inp, ld0, lsb_addr)
        out1 = self.r1.eval(inp, ld1, lsb_addr)
        out2 = self.r2.eval(inp, ld2, lsb_addr)
        out3 = self.r3.eval(inp, ld3, lsb_addr)

        return Mux4Way16(out0, out1, out2, out3, sel=msb_addr)

    def __str__(self):
        return f'{self.r0}\n{self.r1}\n{self.r2}\n{self.r3}'

    def __repr__(self):
        return str(self)


class PC:
    def __init__(self):
        self.reg = Register()

    def eval(self, inp, load, inc, reset):
        # For simplicity in the implementation, we use an 8-way Mux to
        # select between the four possible inputs to this gate. The four
        # inputs include the cases where reset, inc, and load are all 0
        # or one of them is 1. Supplying multiple high values will result
        # in the first high most-significant bit being selected. These
        # inputs can be summarized as follows:
        # 
        # sel = (reset, inc, load)
        #
        # where
        #
        # reset | inc | load | output
        # 0     | 0   | 0    | curr_val
        # 0     | 0   | 1    | inp
        # 0     | 1   | 0    | curr_val + 1
        # 0     | 1   | 1    | inp
        # 1     | 0   | 0    | 0
        # 1     | 0   | 1    | 0
        # 1     | 1   | 0    | 0
        # 1     | 1   | 1    | 0
        #

        false = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        curr_val = self.reg.val
        next_val = Inc16(curr_val)

        sel = (reset, inc, load)

        muxout = Mux8Way16(a=curr_val, b=inp, c=next_val, d=inp,
                           e=false, f=false, g=false, h=false,
                           sel=sel)
        
        regout = self.reg.eval(inp=muxout, load=1)

        return self
    
    @property
    def val(self):
        return self.reg.val

    def __str__(self):
        return str(self.reg)
    
    def __repr__(self):
        return str(self)
