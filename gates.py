def Nand(a, b):
    '''
    This is our axiomatic gate, so we can create it with
    high-level Python constructs.
    '''
    return 0 if a == 1 and b == 1 else 1


def Not(a):
    return Nand(a, a)

def And(a, b):
    return Not(Nand(a, b))

def Or(a, b):
    return Not(And(Not(a), Not(b)))

def Xor(a, b):
    return Or(And(a, Not(b)),
              And(Not(a), b))

def Mux(a, b, sel):
    return Or(And(Not(sel), a),
              And(sel, b))

def Demux(inp, sel):
    a = And(Xor(inp, sel),
            Not(sel))
    b = And(inp, sel)
    return a, b

