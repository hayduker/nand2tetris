from logic import *


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
