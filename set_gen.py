"""
Turn on the analog generator: balanced, 1 kHz, 0.1 V RMS.
Writes full diagnostic output to set_gen.txt.
"""
import sys, traceback
sys.path.insert(0, r"C:\src\Claude-APWin")

OUT = r"C:\src\Claude-APWin\set_gen.txt"
lines = []

def log(s=""):
    lines.append(str(s))
    try:
        print(s)
    except Exception:
        pass

try:
    log("--- set_gen.py starting ---")
    import win32com.client, pythoncom
    log("win32com imported OK")

    # Connect to APWin
    try:
        app_com = win32com.client.GetActiveObject("APWIN.Application")
        log("Connected via GetActiveObject")
    except Exception as e1:
        log(f"GetActiveObject failed ({e1}), trying Dispatch...")
        app_com = win32com.client.Dispatch("APWIN.Application")
        log("Connected via Dispatch")

    gen_com = win32com.client.Dispatch(app_com.Gen())
    log(f"Gen COM object acquired")

    # ------------------------------------------------------------------
    # Read current state
    # ------------------------------------------------------------------
    try:
        log(f"WfmName:  {gen_com.WfmName}")
    except Exception as e:
        log(f"WfmName read failed: {e}")
    try:
        log(f"Config:   {gen_com.Config}")
    except Exception as e:
        log(f"Config read failed: {e}")
    try:
        log(f"Output:   {gen_com.Output}")
    except Exception as e:
        log(f"Output read failed: {e}")
    try:
        log(f"Freq Hz:  {gen_com.Freq('Hz')}")
    except Exception as e:
        log(f"Freq read failed: {e}")
    try:
        log(f"Ampl dBV: {gen_com.Ampl('dBV')}")
    except Exception as e:
        log(f"Ampl read failed: {e}")
    log()

    # ------------------------------------------------------------------
    # Set waveform to sine (try IDs 0 and 1 to find the right one)
    # ------------------------------------------------------------------
    freq_dispid = gen_com._oleobj_.GetIDsOfNames(0, "Freq")
    ampl_dispid = gen_com._oleobj_.GetIDsOfNames(0, "Ampl")
    PROPPUT = pythoncom.DISPATCH_PROPERTYPUT

    current_wfm = str(gen_com.WfmName).lower()
    log(f"Current waveform: '{current_wfm}'")

    if "sine" not in current_wfm and "sin" not in current_wfm:
        log("Waveform is not sine — attempting to set sine...")
        for wfm_id in (0, 1, 2):
            try:
                gen_com.Wfm(wfm_id, 0)
                new_name = str(gen_com.WfmName)
                log(f"  Wfm({wfm_id},0) → '{new_name}'")
                if "sine" in new_name.lower() or "sin" in new_name.lower():
                    log("  Sine waveform confirmed.")
                    break
            except Exception as e:
                log(f"  Wfm({wfm_id},0) failed: {e}")
    else:
        log("Already sine — no waveform change needed.")
    log()

    # ------------------------------------------------------------------
    # Config: 0 = balanced
    # ------------------------------------------------------------------
    try:
        gen_com.Config = 0
        log(f"Config set to 0 → read back: {gen_com.Config}")
    except Exception as e:
        log(f"Config set failed: {e}")

    # ------------------------------------------------------------------
    # Frequency: 1000 Hz
    # ------------------------------------------------------------------
    try:
        gen_com._oleobj_.Invoke(freq_dispid, 0, PROPPUT, 0, "Hz", 1000.0)
        log(f"Freq set 1000 Hz → read back: {gen_com.Freq('Hz'):.1f} Hz")
    except Exception as e:
        log(f"Freq set failed: {e}")

    # ------------------------------------------------------------------
    # Amplitude: 0.1 Vrms
    # ------------------------------------------------------------------
    ampl_set = False
    for unit, val in [("Vrms", 0.1), ("V", 0.1), ("dBV", -20.0)]:
        try:
            gen_com._oleobj_.Invoke(ampl_dispid, 0, PROPPUT, 0, unit, val)
            log(f"Ampl set {val} {unit} → read back: {gen_com.Ampl('Vrms'):.4f} Vrms  ({gen_com.Ampl('dBV'):.2f} dBV)")
            ampl_set = True
            break
        except Exception as e:
            log(f"Ampl set {val} {unit} failed: {e}")
    if not ampl_set:
        log("WARNING: Could not set amplitude.")

    # ------------------------------------------------------------------
    # Output on
    # ------------------------------------------------------------------
    try:
        gen_com.Output = True
        log(f"Output: {gen_com.Output}")
    except Exception as e:
        log(f"Output set failed: {e}")

    log()
    log(f"Final state:")
    log(f"  WfmName: {gen_com.WfmName}")
    log(f"  Config:  {gen_com.Config}")
    log(f"  Freq:    {gen_com.Freq('Hz'):.1f} Hz")
    try:
        log(f"  Ampl:    {gen_com.Ampl('Vrms'):.4f} Vrms  ({gen_com.Ampl('dBV'):.2f} dBV)")
    except Exception:
        pass
    log(f"  Output:  {gen_com.Output}")
    log()
    log("Done.")

except Exception as e:
    log(f"\nFATAL: {e}")
    log(traceback.format_exc())
finally:
    with open(OUT, "w") as f:
        f.write("\n".join(lines))
