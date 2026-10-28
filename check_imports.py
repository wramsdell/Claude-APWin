import sys, traceback

out = []
def p(s): out.append(str(s)); print(s)

try:
    sys.path.insert(0, r"C:\src\Claude-APWin")
    from apwin import APWin
    p("import OK")

    ap = APWin()
    p(f"APWin: {repr(ap)}")
    p(f"sys_type: {ap.app.sys_type()}")
    p(f"version: {ap.app.version()}")
    p(f"gen: {repr(ap.gen)}")
    p(f"anlr: {repr(ap.anlr)}")
    p(f"sweep: {repr(ap.sweep)}")
    p("ALL OK")
except Exception:
    p(traceback.format_exc())

with open(r"C:\src\Claude-APWin\check.txt", "w") as f:
    f.write("\n".join(out))
