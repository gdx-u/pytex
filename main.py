
def scan_ahead(of, lf, ptr, inx):
    ptr += 1
    start = ptr
    opened = 0
    while ptr < len(inx) and inx[ptr] != lf or opened:
        if inx[ptr] == of:
            opened += 1
        elif inx[ptr] == lf:
            opened -= 1
        ptr += 1

    return ptr + 1, inx[start : ptr] 

def scan_to(ptr, inx):
    if not inx[ptr].isalnum():
        return ptr + 1, inx[ptr]
    s = ptr
    while ptr < len(inx) and inx[ptr].isalnum() and inx[ptr] != " ":
        ptr += 1
    
    return ptr, inx[s : ptr]


def evaluate(inx, raw = False):
    import constants as c

    expr = []
    ptr = 0

    # First run through
    while ptr < len(inx):
        char = inx[ptr]
        exp = None
        if char in c.lookaheads:
            ptr, exp = scan_ahead(char, c.lookaheads[char], ptr, inx)
            if char == "(":
                expr += [exp]
            elif char == "{":
                expr += ["\\" + exp + " "]
            elif char == "!":
                expr += ["\\mathrm{" + exp + "}"]
            elif char == "`":
                expr += ["".join(map(lambda e: "".join(e), zip(exp, "`" * len(exp)))).replace("`", "` ")]

        elif char in c.constants:
            if type(c.constants[char]) == str:
                expr += [c.constants[char]]
                ptr += 1
            else:
                expr += char
                ptr += 1
                # ptr = c.constants[char](ptr, expr)

        else:
            ptr, exp = scan_to(ptr, inx)
            expr += [exp]

        if raw: print(expr)

    ptr = 0
    while ptr < len(expr):
        exp = expr[ptr]
        if exp in c.constants and type(c.constants[exp]) != str:
            c.constants[exp](ptr, expr)
            ptr = 0
        else:
            ptr += 1

    ptr = 0
    while ptr < len(expr):
        exp = expr[ptr]
        for fn in c.functions:
            if exp.endswith(fn):
                c.functions[fn](ptr, expr)
                ptr = 0
                break
        else:
            ptr += 1

    for exp in expr:

    if raw: return expr
    return "".join(expr)

if __name__ == "__main__":
    import sys
    import constants as c

    inf = open(f"in/{sys.argv[1].replace('.ptx', '')}.ptx", "r")
    outf = open(f"out/{sys.argv[2].replace('.ltx', '')}.ltx", "w")

    inx_full = inf.read()
    inf.close()

    # Preamble
    full = "\\documentclass{article}\n\\title{" + sys.argv[1].replace(".ptx", "") + "}\n\\author{PyTeX}\n\\begin{document}\n\\maketitle\n\\noindent "

    expr = "".join(evaluate(inx_full, True))
    for s in c.simples:
        expr = expr.replace(s, c.simples[s])
        expr = expr.replace(c.simples[s] + "` ", s)

    for r in c.reqs:
        for req in r.split(", "):
            if req in expr:
                full = full.replace("\\documentclass{article}", "\\documentclass{article}\n\\usepackage{" + c.reqs[r] + "}")

    expr = expr.replace("` ", "")

    full += "".join(expr) + "\n\\end{document}"
    outf.write(full)