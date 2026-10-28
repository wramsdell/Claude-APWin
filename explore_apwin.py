"""
Explore the APWin COM interface and dump all available type library members.
Must be run from an elevated (Administrator) process.
"""
import sys
import traceback
import win32com.client
import pythoncom
import pywintypes

OUTPUT_FILE = r"C:\src\Claude-APWin\apwin_interface.txt"

lines = []

def out(s=""):
    print(s)
    lines.append(s)

def explore_typeinfo(typeinfo, name, depth=0):
    indent = "  " * depth
    try:
        ta = typeinfo.GetTypeAttr()
    except Exception as e:
        out(f"{indent}[{name}] could not get type attr: {e}")
        return

    kind_map = {0: "enum", 1: "struct", 2: "module", 3: "interface",
                4: "dispinterface", 5: "coclass", 6: "typedef",
                7: "union", 8: "max"}
    kind = kind_map.get(ta.typekind, str(ta.typekind))
    out(f"{indent}[{name}] typekind={kind}, funcs={ta.cFuncs}, vars={ta.cVars}, impls={ta.cImplTypes}")

    for i in range(ta.cFuncs):
        try:
            fd = typeinfo.GetFuncDesc(i)
            names = typeinfo.GetNames(fd.memid)
            fname = names[0] if names else f"<id={fd.memid}>"
            params = names[1:] if len(names) > 1 else []
            invoke = {1: "method", 2: "get", 4: "put", 8: "propget",
                      16: "propput", 32: "propputref"}.get(fd.invkind, str(fd.invkind))
            param_str = ", ".join(params) if params else ""
            out(f"{indent}  [{invoke}] {fname}({param_str})")
        except Exception as e:
            out(f"{indent}  [func {i}] error: {e}")

    for i in range(ta.cVars):
        try:
            vd = typeinfo.GetVarDesc(i)
            vnames = typeinfo.GetNames(vd.memid)
            vname = vnames[0] if vnames else f"<id={vd.memid}>"
            out(f"{indent}  [var] {vname}")
        except Exception as e:
            out(f"{indent}  [var {i}] error: {e}")


def explore_typelib(obj):
    try:
        ti = obj._oleobj_.GetTypeInfo(0)
        tl = ti.GetContainingTypeLib()
        typelib, idx = tl
        la = typelib.GetLibAttr()
        count = typelib.GetTypeInfoCount()
        out(f"Type library: {count} type(s)")
        out()
        for i in range(count):
            ti2 = typelib.GetTypeInfo(i)
            tname = typelib.GetDocumentation(i)[0]
            explore_typeinfo(ti2, tname)
            out()
    except Exception as e:
        out(f"Could not walk type library: {e}")
        traceback.print_exc()


def probe_properties(obj):
    out("--- Probing live properties ---")
    props = [
        "Visible", "Name", "Version", "FullName", "Path",
        "Documents", "ActiveDocument", "WindowState",
        "Measurement", "Results", "Graph", "Panel",
        "DefaultFilePath", "Caption", "Title", "Application",
    ]
    for p in props:
        try:
            val = getattr(obj, p)
            out(f"  {p} = {val!r}")
        except AttributeError:
            pass
        except Exception as e:
            out(f"  {p} -> {e}")


def main():
    pythoncom.CoInitialize()
    out("Connecting to APWin...")

    ap = None
    try:
        ap = win32com.client.GetActiveObject("APWIN.Application")
        out("Connected via GetActiveObject (running instance)")
    except pywintypes.com_error as e:
        out(f"GetActiveObject failed: {e}")

    if ap is None:
        try:
            ap = win32com.client.Dispatch("APWIN.Application")
            out("Connected via Dispatch (new or running instance)")
        except pywintypes.com_error as e:
            out(f"Dispatch failed: {e}")
            out()
            out("ERROR: Could not connect. Is APWin running as Administrator?")
            sys.exit(1)

    out()
    out("=== Type Library ===")
    explore_typelib(ap)
    out()
    probe_properties(ap)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    out()
    out(f"Output written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
