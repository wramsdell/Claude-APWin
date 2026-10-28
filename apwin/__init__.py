"""
apwin — Python wrapper for the Audio Precision APWin COM interface.

Requires an elevated (Administrator) process and APWin installed.

Quick start::

    from apwin import APWin

    with APWin() as ap:
        print(ap.app.sys_type())       # e.g. 'SYS-2322'
        ap.gen.freq = "1 kHz"
        ap.gen.ampl = "0 dBV"
        ap.gen.output = True
        ap.anlr.cha_level_trig()
        print(ap.anlr.cha_level_rdg("dBV"))
"""
from .client import APWin
from .application import Application
from .gen import Gen, DGen
from .anlr import Anlr
from .sweep import Sweep, SweepSource, SweepData
from .data import Data
from .file import APFile, Log
from .compute import Compute
from .digital import S2Dio, S2Dsp

__all__ = [
    "APWin",
    "Application",
    "Gen", "DGen",
    "Anlr",
    "Sweep", "SweepSource", "SweepData",
    "Data",
    "APFile", "Log",
    "Compute",
    "S2Dio", "S2Dsp",
]
