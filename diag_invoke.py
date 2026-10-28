"""
Diagnostic: brute-force all plausible IDispatch invocation patterns for
AP's parameterized property puts (e.g. Gen.Freq / Gen.Ampl).

Writes results to diag_invoke.txt so the output is visible from a
non-elevated context.
"""
import sys, traceback
sys.path.insert(0, r"C:\src\Claude-APWin")

OUT = r"C:\src\Claude-APWin\diag_invoke.txt"
lines = []

def log(msg=""):
    lines.append(msg)
    print(msg)

try:
    import pythoncom, pywintypes
    import win32com.client

    # -- Connect ----------------------------------------------------------
    log("Connecting to APWIN.Application ...")
    try:
        app = win32com.client.GetActiveObject("APWIN.Application")
        log("  GetActiveObject OK")
    except Exception:
        app = win32com.client.Dispatch("APWIN.Application")
        log("  Dispatch OK")

    gen_com = win32com.client.Dispatch(app.Gen())
    log(f"  Gen COM object: {gen_com}")

    # -- Read current state -----------------------------------------------
    try:
        cur_freq = gen_com.Freq("Hz")
        log(f"  Current Freq('Hz') = {cur_freq}")
    except Exception as e:
        log(f"  get Freq('Hz') FAILED: {e}")

    # -- Helper -----------------------------------------------------------
    def try_invoke(label, dispid, lcid, wFlags, bResult, *args):
        try:
            result = gen_com._oleobj_.Invoke(dispid, lcid, wFlags, bResult, *args)
            log(f"  [OK]  {label} -> {result}")
            return True
        except Exception as exc:
            log(f"  [ERR] {label} -> {exc}")
            return False

    # Get DISPID for Freq
    freq_dispid = gen_com._oleobj_.GetIDsOfNames(0, "Freq")
    log(f"\nFreq DISPID = {freq_dispid}")

    PROPPUT  = pythoncom.DISPATCH_PROPERTYPUT   # 4
    METHOD   = pythoncom.DISPATCH_METHOD        # 1
    BOTH     = PROPPUT | METHOD                 # 5

    # -- Pattern 1: simple PROPERTYPUT with the full AP unit string --------
    log("\n--- Pattern 1: PROPERTYPUT(dispid, 0, PROPPUT, 0, '1 kHz') ---")
    try_invoke("PROPPUT, '1 kHz'", freq_dispid, 0, PROPPUT, 0, "1 kHz")

    # -- Pattern 2: METHOD with the full string ---------------------------
    log("\n--- Pattern 2: METHOD(dispid, 0, METHOD, 0, '1 kHz') ---")
    try_invoke("METHOD, '1 kHz'", freq_dispid, 0, METHOD, 0, "1 kHz")

    # -- Pattern 3: BOTH flags with the full string -----------------------
    log("\n--- Pattern 3: BOTH(dispid, 0, BOTH, 0, '1 kHz') ---")
    try_invoke("BOTH, '1 kHz'", freq_dispid, 0, BOTH, 0, "1 kHz")

    # -- Pattern 4: indexed put — unit "Hz" as index, float as value ------
    # In COM indexed property put the args are reversed (value first in array,
    # then index), and DISPID_PROPERTYPUT names arg 0 in the array.
    log("\n--- Pattern 4: PROPPUT indexed — unit 'Hz' + float 1000.0 ---")
    try_invoke("PROPPUT, 'Hz', 1000.0", freq_dispid, 0, PROPPUT, 0, 1000.0, "Hz")

    # -- Pattern 5: indexed put, args in opposite order -------------------
    log("\n--- Pattern 5: PROPPUT indexed reversed — float 1000.0 + unit 'Hz' ---")
    try_invoke("PROPPUT, 1000.0, 'Hz'", freq_dispid, 0, PROPPUT, 0, "Hz", 1000.0)

    # -- Pattern 6: METHOD with separate args ----------------------------
    log("\n--- Pattern 6: METHOD with unit 'Hz' + float 1000.0 ---")
    try_invoke("METHOD, 'Hz', 1000.0", freq_dispid, 0, METHOD, 0, "Hz", 1000.0)

    # -- Pattern 7: METHOD float only (no unit) --------------------------
    log("\n--- Pattern 7: METHOD, just 1000.0 ---")
    try_invoke("METHOD, 1000.0", freq_dispid, 0, METHOD, 0, 1000.0)

    # -- Pattern 8: InvokeTypes with BSTR arg type -----------------------
    log("\n--- Pattern 8: InvokeTypes PROPPUT, VT_BSTR, '1 kHz' ---")
    try:
        gen_com._oleobj_.InvokeTypes(
            freq_dispid, 0, PROPPUT,
            (pythoncom.VT_EMPTY, None),   # return type
            ((pythoncom.VT_BSTR, None),), # arg types
            "1 kHz"
        )
        log("  [OK]  InvokeTypes VT_BSTR PROPPUT")
    except Exception as exc:
        log(f"  [ERR] InvokeTypes VT_BSTR PROPPUT -> {exc}")

    # -- Pattern 9: InvokeTypes as METHOD ---------------------------------
    log("\n--- Pattern 9: InvokeTypes METHOD, VT_BSTR, '1 kHz' ---")
    try:
        gen_com._oleobj_.InvokeTypes(
            freq_dispid, 0, METHOD,
            (pythoncom.VT_EMPTY, None),
            ((pythoncom.VT_BSTR, None),),
            "1 kHz"
        )
        log("  [OK]  InvokeTypes VT_BSTR METHOD")
    except Exception as exc:
        log(f"  [ERR] InvokeTypes VT_BSTR METHOD -> {exc}")

    # -- Pattern 10: InvokeTypes indexed put, BSTR + R8 ------------------
    log("\n--- Pattern 10: InvokeTypes PROPPUT, BSTR unit + R8 value ---")
    try:
        gen_com._oleobj_.InvokeTypes(
            freq_dispid, 0, PROPPUT,
            (pythoncom.VT_EMPTY, None),
            ((pythoncom.VT_R8, None), (pythoncom.VT_BSTR, None)),
            1000.0, "Hz"
        )
        log("  [OK]  InvokeTypes PROPPUT R8+BSTR")
    except Exception as exc:
        log(f"  [ERR] InvokeTypes PROPPUT R8+BSTR -> {exc}")

    # -- Check the result -------------------------------------------------
    log("\n--- Final Freq read ---")
    try:
        final_freq = gen_com.Freq("Hz")
        log(f"  Freq('Hz') = {final_freq}")
    except Exception as e:
        log(f"  Freq('Hz') FAILED: {e}")

    # -- Also try Ampl (same pattern) if any pattern worked ---------------
    log("\n--- Quick Ampl test with same patterns ---")
    ampl_dispid = gen_com._oleobj_.GetIDsOfNames(0, "Ampl")
    log(f"Ampl DISPID = {ampl_dispid}")
    for label, flags, args in [
        ("PROPPUT '100 mVrms'",  PROPPUT, ("100 mVrms",)),
        ("METHOD  '100 mVrms'",  METHOD,  ("100 mVrms",)),
        ("BOTH    '100 mVrms'",  BOTH,    ("100 mVrms",)),
    ]:
        try_invoke(label, ampl_dispid, 0, flags, 0, *args)

except Exception:
    log("\nFATAL:")
    log(traceback.format_exc())

# Write output file
with open(OUT, "w") as f:
    f.write("\n".join(lines))
print(f"\nResults written to {OUT}")
