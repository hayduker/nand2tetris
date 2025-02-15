##########################################################
# This is our axiomatic gate, so we can create it
# with high-level Python constructs.
##########################################################

def Nand(a, b):
    return 0 if a == 1 and b == 1 else 1


##########################################################
# Now we implement the basic gates using only Nand
# and previously-defined gates
##########################################################

def Not(a):
    return Nand(a, a)

def And(a, b):
    return Not(Nand(a, b))

def Or(a, b):
    return Nand(Not(a), Not(b))

def Xor(a, b):
    return Or(And(a, Not(b)),
              And(Not(a), b))

def Mux(a, b, sel):
    return Or(And(Not(sel), a),
              And(sel, b))

def DMux(inp, sel):
    a = And(Xor(inp, sel),
            Not(sel))
    b = And(inp, sel)
    return a, b


##########################################################
# Multi-bit versions of some of the basic gates
#
# It would be easy to implement these gates using Python
# lists, but that goes against the intention here. We want
# to build progressively more complex gates using only
# those gates we've defined already, in a way that will
# emulate the nand2tetris HDL which describes simply the
# physical interconnections of gates. This isn't meant to
# be efficient, it's meant to show how one can build a
# computer from first principles... we want to show how
# to *achieve* the high-level abstraction that is a Python
# list from such low-level parts.
##########################################################

def Not16(inp):
    out0  = Not(inp[15])
    out1  = Not(inp[14])
    out2  = Not(inp[13])
    out3  = Not(inp[12])
    out4  = Not(inp[11])
    out5  = Not(inp[10])
    out6  = Not(inp[9])
    out7  = Not(inp[8])
    out8  = Not(inp[7])
    out9  = Not(inp[6])
    out10 = Not(inp[5])
    out11 = Not(inp[4])
    out12 = Not(inp[3])
    out13 = Not(inp[2])
    out14 = Not(inp[1])
    out15 = Not(inp[0])

    return out15, out14, out13, out12, out11, out10, out9, out8, \
           out7,  out6,  out5,  out4,  out3,  out2,  out1, out0

def And16(a, b):
    out0  = And(a[15], b[15])
    out1  = And(a[14], b[14])
    out2  = And(a[13], b[13])
    out3  = And(a[12], b[12])
    out4  = And(a[11], b[11])
    out5  = And(a[10], b[10])
    out6  = And(a[9],  b[9])
    out7  = And(a[8],  b[8])
    out8  = And(a[7],  b[7])
    out9  = And(a[6],  b[6])
    out10 = And(a[5],  b[5])
    out11 = And(a[4],  b[4])
    out12 = And(a[3],  b[3])
    out13 = And(a[2],  b[2])
    out14 = And(a[1],  b[1])
    out15 = And(a[0],  b[0])

    return out15, out14, out13, out12, out11, out10, out9, out8, \
           out7,  out6,  out5,  out4,  out3,  out2,  out1, out0

def Or16(a, b):
    out0  = Or(a[15], b[15])
    out1  = Or(a[14], b[14])
    out2  = Or(a[13], b[13])
    out3  = Or(a[12], b[12])
    out4  = Or(a[11], b[11])
    out5  = Or(a[10], b[10])
    out6  = Or(a[9],  b[9])
    out7  = Or(a[8],  b[8])
    out8  = Or(a[7],  b[7])
    out9  = Or(a[6],  b[6])
    out10 = Or(a[5],  b[5])
    out11 = Or(a[4],  b[4])
    out12 = Or(a[3],  b[3])
    out13 = Or(a[2],  b[2])
    out14 = Or(a[1],  b[1])
    out15 = Or(a[0],  b[0])

    return out15, out14, out13, out12, out11, out10, out9, out8, \
           out7,  out6,  out5,  out4,  out3,  out2,  out1, out0

def Mux16(a, b, sel):
    out0  = Mux(a[15], b[15], sel)
    out1  = Mux(a[14], b[14], sel)
    out2  = Mux(a[13], b[13], sel)
    out3  = Mux(a[12], b[12], sel)
    out4  = Mux(a[11], b[11], sel)
    out5  = Mux(a[10], b[10], sel)
    out6  = Mux(a[9],  b[9],  sel)
    out7  = Mux(a[8],  b[8],  sel)
    out8  = Mux(a[7],  b[7],  sel)
    out9  = Mux(a[6],  b[6],  sel)
    out10 = Mux(a[5],  b[5],  sel)
    out11 = Mux(a[4],  b[4],  sel)
    out12 = Mux(a[3],  b[3],  sel)
    out13 = Mux(a[2],  b[2],  sel)
    out14 = Mux(a[1],  b[1],  sel)
    out15 = Mux(a[0],  b[0],  sel)

    return out15, out14, out13, out12, out11, out10, out9, out8, \
           out7,  out6,  out5,  out4,  out3,  out2,  out1, out0


##########################################################
# Multi-way versions of some of the basic gates
##########################################################

def Or8Way(inp):
    return Or(inp[7],
              Or(inp[6],
                 Or(inp[5],
                    Or(inp[4],
                       Or(inp[3],
                          Or(inp[2],
                             Or(inp[1],
                                inp[0])))))))

def Mux4Way16(a, b, c, d, sel):
    sel0 = sel[1]
    sel1 = sel[0]

    a_or_b = Mux16(a, b, sel0)
    c_or_d = Mux16(c, d, sel0)

    return Mux16(a_or_b, c_or_d, sel1)

def Mux8Way16(a, b, c, d, e, f, g, h, sel):
    sel0 = sel[2]
    sel1 = sel[1]
    sel2 = sel[0]

    a_or_b = Mux16(a, b, sel0)
    c_or_d = Mux16(c, d, sel0)
    e_or_f = Mux16(e, f, sel0)
    g_or_h = Mux16(g, h, sel0)

    abc_or_d = Mux16(a_or_b, c_or_d, sel1)
    efg_or_h = Mux16(e_or_f, g_or_h, sel1)

    return Mux16(abc_or_d, efg_or_h, sel2)

def DMux4Way(inp, sel):
    sel0 = sel[1]
    sel1 = sel[0]

    y, z = DMux(inp, sel0)

    a = And(Not(sel1), y)
    b = And(Not(sel1), z)
    c = And(sel1, y)
    d = And(sel1, z)

    return a, b, c, d

def DMux8Way(inp, sel):
    sel0 = sel[2]
    sel1 = sel[1]
    sel2 = sel[0]

    q, r = DMux(inp, sel0)

    w, x, y, z = DMux4Way(inp, (sel1, sel0))

    a = And(Not(sel2), w)
    b = And(Not(sel2), x)
    c = And(Not(sel2), y)
    d = And(Not(sel2), z)
    e = And(sel2, w)
    f = And(sel2, x)
    g = And(sel2, y)
    h = And(sel2, z)

    return a, b, c, d, e, f, g, h
    


def HalfAdder(a, b):
    sm = Xor(a, b)
    cr = And(a, b)
    return sm, cr

def FullAdder(a, b, c):
    s0, c0 = HalfAdder(a, b)
    sm, c1 = HalfAdder(s0, c)
    cr = Or(c0, c1)
    return sm, cr

def Add16(a, b):
    sm0,  cr0  = HalfAdder(a[15], b[15])
    sm1,  cr1  = FullAdder(a[14], b[14], cr0)
    sm2,  cr2  = FullAdder(a[13], b[13], cr1)
    sm3,  cr3  = FullAdder(a[12], b[12], cr2)
    sm4,  cr4  = FullAdder(a[11], b[11], cr3)
    sm5,  cr5  = FullAdder(a[10], b[10], cr4)
    sm6,  cr6  = FullAdder(a[9],  b[9],  cr5)
    sm7,  cr7  = FullAdder(a[8],  b[8],  cr6)
    sm8,  cr8  = FullAdder(a[7],  b[7],  cr7)
    sm9,  cr9  = FullAdder(a[6],  b[6],  cr8)
    sm10, cr10 = FullAdder(a[5],  b[5],  cr9)
    sm11, cr11 = FullAdder(a[4],  b[4],  cr10)
    sm12, cr12 = FullAdder(a[3],  b[3],  cr11)
    sm13, cr13 = FullAdder(a[2],  b[2],  cr12)
    sm14, cr14 = FullAdder(a[1],  b[1],  cr13)
    sm15, _    = FullAdder(a[0],  b[0],  cr14)

    return sm15, sm14, sm13, sm12, sm11, sm10, sm9, sm8, \
           sm7,  sm6,  sm5,  sm4,  sm3,  sm2,  sm1, sm0

def Inc16(inp):
    return Add16(inp,
                 (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1))

def ALU(x, y, zx, nx, zy, ny, f, no):
    zero16 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    mid_x = Mux16(x, zero16, zx)

    end_x = Mux16(mid_x, Not16(mid_x), nx)

    mid_y = Mux16(y, zero16, zy)

    end_y = Mux16(mid_y, Not16(mid_y), ny)

    mid_out = Mux16(And16(end_x, end_y),
                    Add16(end_x, end_y),
                    f)

    out = Mux16(mid_out, Not16(mid_out), no)

    zr = Not(Or(Or8Way((out[15], out[14], out[13], out[12],
                        out[11], out[10], out[9], out[8])),
                Or8Way((out[7],  out[6],  out[5], out[4],
                        out[3],  out[2],  out[1], out[0]))))
    
    ng = out[0]

    return out, zr, ng



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



##########################################################
# Now we build the computer architecture from the ALU,
# RAM, and other components we have built so far.
##########################################################

