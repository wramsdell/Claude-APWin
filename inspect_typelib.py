"""
Inspect the APWin type library (registered, no server connection needed)
and print exact parameter info for propput methods.

Writes to inspect_typelib.txt.
"""
import pythoncom, pywintypes

OUT = r"C:\src\Claude-APWin\inspect_typelib.txt"
lines = []
def log(s=""): lines.append(s); print(s)

# APWin type library — same CLSID / ProgID as the server
APWIN_CLSID = "{A21188C0-6127-11CE-9A78-0800099681CA}"

try:
    # Find the EXE from the registry LocalServer32 key
    import winreg
    apwin_exe = None
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Classes\CLSID\{A21188C0-6127-11CE-9A78-0800099681CA}\LocalServer32")
        apwin_exe, _ = winreg.QueryValueEx(key, "")
        winreg.CloseKey(key)
    except Exception as e:
        log(f"Registry lookup failed: {e}")
    if not apwin_exe:
        # fall back to 64-bit view
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\WOW6432Node\Classes\CLSID\{A21188C0-6127-11CE-9A78-0800099681CA}\LocalServer32")
            apwin_exe, _ = winreg.QueryValueEx(key, "")
            winreg.CloseKey(key)
        except Exception as e2:
            log(f"WOW6432 registry lookup failed: {e2}")

    log(f"APWin EXE from registry: {apwin_exe}")

    # Load type lib from the EXE
    if apwin_exe:
        exe_path = apwin_exe.strip('"').split('"')[0]
        log(f"Loading type lib from: {exe_path}")
        tl = pythoncom.LoadTypeLib(exe_path)
    else:
        # Last resort: makepy knows how to find it
        import win32com.client.makepy as makepy
        from win32com.client import gencache
        makepy.GenerateFromTypeLibSpec("APWIN.Application", verboseLevel=0)
        raise RuntimeError("Couldn't load type lib directly; makepy stubs generated instead")

    log(f"Loaded: {tl}")

    log(f"TypeLib name: {tl.GetDocumentation(-1)}")
    log(f"TypeLib count: {tl.GetTypeInfoCount()}")
    log()

    INVKIND_NAMES = {
        1: "FUNC",
        2: "PROPERTYGET",
        4: "PROPERTYPUT",
        8: "PROPERTYPUTREF",
    }
    PARAMFLAG_NAMES = {
        0: "",
        1: "[in]",
        2: "[out]",
        3: "[in,out]",
        4: "[retval]",
        5: "[in,retval]",
    }

    # Walk every type, find funcs with "Freq" or "Ampl" in their name
    # that are PROPERTYPUT, and dump ALL parameter info
    for i in range(tl.GetTypeInfoCount()):
        ti = tl.GetTypeInfo(i)
        ta = ti.GetTypeAttr()
        type_name = ti.GetDocumentation(-1)[0]

        for j in range(ta.cFuncs):
            fd = ti.GetFuncDesc(j)
            # PyFUNCDESC: .args is a tuple of (type_tuple, paramflags) per param
            n_params = len(fd.args)
            func_name = ti.GetNames(fd.memid)[0]

            if fd.invkind == pythoncom.INVOKE_PROPERTYPUT and \
               func_name in ("Freq", "Ampl", "ChAAmpl", "ChBAmpl", "RefFreq", "Phase"):

                invkind_str = INVKIND_NAMES.get(fd.invkind, str(fd.invkind))
                log(f"[{type_name}] {invkind_str} {func_name}")
                log(f"  memid/dispid = {fd.memid}")
                log(f"  n_params (len args) = {n_params}")
                log(f"  cParamsOpt = {fd.cParamsOpt}")
                log(f"  wFuncFlags = {fd.wFuncFlags}")

                all_names = ti.GetNames(fd.memid)
                log(f"  names = {all_names}")

                for k, arg_tuple in enumerate(fd.args):
                    param_name = all_names[k+1] if k+1 < len(all_names) else f"<unnamed>"
                    log(f"  param[{k}] '{param_name}': raw={arg_tuple}")

                # Return type
                log(f"  retType: {fd.retType}")
                log()

except Exception as e:
    import traceback
    log(f"ERROR: {e}")
    log(traceback.format_exc())

with open(OUT, "w") as f:
    f.write("\n".join(lines))
print(f"\nWritten to {OUT}")
