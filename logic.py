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



##########################################################
# Now we build the computer architecture from the ALU,
# RAM, and other components we have built so far.
##########################################################

