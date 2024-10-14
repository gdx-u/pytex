import main as m

def frac(ptr, expr):
    # return "/frac{A}{B}".replace("A", n).replace("B", d)
    # pass
    out = "\\frac{A}{B}"
    a = b = 1
    N = ptr - a
    while expr[N] == " ":
        a += 1
        N = ptr - a
 
    D = ptr + b
    while expr[D] == " ":
        b += 1
        D = ptr + b

    # print(expr[N])
    # print(expr[N], m.evaluate(expr[N]))
    out = out.replace("A", m.evaluate(expr[N])).replace("B", m.evaluate(expr[D]))
    expr[N : D + 1] = [out]

def root(ptr, expr):
    ptr += 1
    args = expr[ptr].split(",")
    args = list(map(lambda e: m.evaluate(e.strip()), args))
    if len(args) == 1:
        expr[ptr - 1 : ptr + 1] = "\\sqrt{" + args[0] + "}"
    else:
        expr[ptr - 1 : ptr + 1] = "\\sqrt[" + args[0] + "]{" + args[1] + "}"

def integrate(ptr, expr):
    ptr += 1
    args = expr[ptr].split(",")
    args = list(map(lambda e: m.evaluate(e.strip()), args))
    if len(args) == 3:
        expr[ptr - 1 : ptr + 1] = "\\int_{" + args[0] + "}^{" + args[1] + "} " + args[2]
    else:
        expr[ptr - 1 : ptr + 1] = "\\int " + args[2]

constants = {
    "/": frac,
}

lookaheads = {
    "(": ")", # Expression
    "{": "}", # Constants
    "!": "!", # Mathrm
    "`": "`", # Literal
}

simples = {
    "+-": "\\pm ",
    "*": "\\cdot ",
    ">": "\\right)",
    "<": "\\left(",
    "[": "$",
    "]": "$",
    "\n": "\\\\",
    "\\\\$$": " $$",
    "$$\\\\": "$$ "
}

functions = {
    "rt": root,
    "int": integrate
}

reqs = {
    "degree": "gensymb"
}