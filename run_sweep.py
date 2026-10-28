"""
Run a frequency sweep: 20 Hz – 20 kHz, log, 100 steps.
Measures Ch A level (dBV) vs frequency.
Writes results to run_sweep.txt.
"""
import sys, traceback, time
sys.path.insert(0, r"C:\src\Claude-APWin")

OUTS = [r"C:\src\Claude-APWin\run_sweep.txt", r"C:\Users\Public\run_sweep.txt"]
lines = []

def log(s=""):
    lines.append(str(s))
    try: print(s)
    except Exception: pass

try:
    log("--- run_sweep.py starting ---")
    import win32com.client, pythoncom
    PROPPUT = pythoncom.DISPATCH_PROPERTYPUT

    # -- Connect ----------------------------------------------------------
    try:
        app_com = win32com.client.GetActiveObject("APWIN.Application")
        log("Connected via GetActiveObject")
    except Exception:
        app_com = win32com.client.Dispatch("APWIN.Application")
        log("Connected via Dispatch")

    sweep_com  = win32com.client.Dispatch(app_com.Sweep())
    source_com = win32com.client.Dispatch(sweep_com.Source1())
    gen_com    = win32com.client.Dispatch(app_com.Gen())
    anlr_com   = win32com.client.Dispatch(app_com.Anlr())

    # -- Read current Source1 state ---------------------------------------
    log(f"Source1.Id:      {source_com.Id}")
    log(f"Source1.LogLin:  {source_com.LogLin}")
    log(f"Source1.Steps:   {source_com.Steps}")
    try:
        log(f"Source1.Start:   {source_com.Start('Hz')} Hz")
        log(f"Source1.Stop:    {source_com.Stop('Hz')} Hz")
    except Exception as e:
        log(f"Source1 Start/Stop read: {e}")
    log()

    # Source1.Id = 5087 (Gen.Freq) confirmed — sweep axis already correct.

    # -- Configure sweep axis ---------------------------------------------
    start_dispid    = source_com._oleobj_.GetIDsOfNames(0, "Start")
    stop_dispid     = source_com._oleobj_.GetIDsOfNames(0, "Stop")

    source_com._oleobj_.Invoke(start_dispid, 0, PROPPUT, 0, "Hz", 20.0)
    log(f"Start set 20 Hz  → read back: {source_com.Start('Hz'):.1f} Hz")

    source_com._oleobj_.Invoke(stop_dispid, 0, PROPPUT, 0, "Hz", 20000.0)
    log(f"Stop set 20 kHz → read back:  {source_com.Stop('Hz'):.1f} Hz")

    source_com.LogLin = 1       # 1 = log spacing
    log(f"LogLin: {source_com.LogLin}")

    source_com.Steps = 100
    log(f"Steps: {source_com.Steps}")
    log()

    # -- Make sure generator is on at 0.1 Vrms, sine wave ----------------
    freq_dispid = gen_com._oleobj_.GetIDsOfNames(0, "Freq")
    ampl_dispid = gen_com._oleobj_.GetIDsOfNames(0, "Ampl")

    # Set sine waveform so Ampl control is active
    wfm_name = str(gen_com.WfmName).lower()
    log(f"WfmName: {wfm_name}")
    if "sin" not in wfm_name:
        for wid in (0, 1, 2):
            try:
                gen_com.Wfm(wid, 0)
                wfm_name = str(gen_com.WfmName)
                log(f"  Wfm({wid},0) → '{wfm_name}'")
                if "sin" in wfm_name.lower():
                    break
            except Exception as e:
                log(f"  Wfm({wid},0): {e}")

    gen_com._oleobj_.Invoke(freq_dispid, 0, PROPPUT, 0, "Hz", 20.0)
    try:
        gen_com._oleobj_.Invoke(ampl_dispid, 0, PROPPUT, 0, "Vrms", 0.1)
        log(f"Ampl: {gen_com.Ampl('Vrms'):.4f} Vrms")
    except Exception as e:
        log(f"Ampl set failed (proceeding anyway): {e}")
    gen_com.Output = True
    log(f"Gen: freq={gen_com.Freq('Hz'):.1f} Hz, out={gen_com.Output}")
    log()

    # -- Configure Data1 measurement source (Ch A Level) -----------------
    data1_com = win32com.client.Dispatch(sweep_com.Data1())
    log(f"Data1.Id before: {data1_com.Id}")
    log(f"Data1.LogLin:    {data1_com.LogLin}")

    # Get the DISPID of ChALevelRdg — this is what Data1.Id should be set to
    anlr_level_dispid = anlr_com._oleobj_.GetIDsOfNames(0, "ChALevelRdg")
    log(f"Anlr.ChALevelRdg DISPID = {anlr_level_dispid}")

    if data1_com.Id == 0 or data1_com.Id != anlr_level_dispid:
        try:
            data1_com.Id = anlr_level_dispid
            log(f"Data1.Id set to {data1_com.Id}")
        except Exception as e:
            log(f"Data1.Id set failed: {e}")
    log()

    # -- Run the sweep ----------------------------------------------------
    log("Starting sweep...")
    t0 = time.monotonic()
    sweep_com.StartNoWait()

    # Poll for completion (max 120 s)
    deadline = t0 + 120.0
    while True:
        running = sweep_com.IsRunning()
        if not running:
            break
        if time.monotonic() > deadline:
            sweep_com.Stop()
            log("TIMEOUT — sweep stopped after 120 s")
            break
        time.sleep(0.5)

    elapsed = time.monotonic() - t0
    log(f"Sweep complete in {elapsed:.1f} s")
    log()

    # -- Read sweep data --------------------------------------------------
    data_com = win32com.client.Dispatch(app_com.Data())

    # Try known dataset names
    for name in ("Data1", "Data 1", "data1", "Sweep1", ""):
        try:
            did = data_com.Id(name)
            ncols = data_com.ColNumOf(did)
            log(f"Dataset '{name}': id={did}, cols={ncols}")
            if ncols > 0:
                for col in range(ncols):
                    cname = data_com.ColName(did, col)
                    cunit = data_com.ColUnit(did, col)
                    csize = data_com.ColSize(did, col)
                    log(f"  col[{col}]: '{cname}' ({cunit}), {csize} pts")
                if ncols >= 2:
                    log(f"\nFirst 5 points:")
                    for i in range(min(5, data_com.ColSize(did, 0))):
                        x = data_com.Value(did, 0, i, "Hz")
                        y = data_com.Value(did, 1, i, "dBV")
                        log(f"  {x:.1f} Hz  {y:.2f} dBV")
                    sz = data_com.ColSize(did, 0)
                    log(f"...\nLast 5 points:")
                    for i in range(max(0, sz-5), sz):
                        x = data_com.Value(did, 0, i, "Hz")
                        y = data_com.Value(did, 1, i, "dBV")
                        log(f"  {x:.1f} Hz  {y:.2f} dBV")
                break
        except Exception as e:
            log(f"Dataset '{name}': {e}")

    log()
    log("Done.")

except Exception as e:
    log(f"\nFATAL: {e}")
    log(traceback.format_exc())
finally:
    import datetime
    content = f"\n=== {datetime.datetime.now()} ===\n" + "\n".join(lines)
    for out in OUTS:
        try:
            with open(out, "a") as f:
                f.write(content + "\n")
        except Exception:
            pass
