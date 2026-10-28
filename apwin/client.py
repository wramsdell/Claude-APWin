"""APWin COM client — main entry point."""
from __future__ import annotations
from functools import cached_property
from typing import Optional

import win32com.client
import pywintypes
import pythoncom


class APWin:
    """
    Connection to a running Audio Precision APWin instance.

    Must be instantiated from an elevated (Administrator) process because
    APWin's COM server requires elevation.

    Usage::

        with APWin() as ap:
            ap.app.visible = True
            ap.gen.freq = "1 kHz"
            ap.gen.ampl = "0 dBV"
            ap.sweep.start()
    """

    def __init__(self, attach: bool = True, visible: Optional[bool] = None):
        """
        Connect to APWin.

        Parameters
        ----------
        attach:
            Try ``GetActiveObject`` first (connect to running instance).
            Falls back to ``Dispatch`` (launch a new instance) if that fails.
        visible:
            If not None, set ``Application.Visible`` after connecting.
        """
        pythoncom.CoInitialize()
        self._com = self._connect(attach)
        if visible is not None:
            self._com.Application().Visible = visible

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    @staticmethod
    def _connect(attach: bool):
        if attach:
            try:
                com = win32com.client.GetActiveObject("APWIN.Application")
                return com
            except pywintypes.com_error:
                pass
        return win32com.client.Dispatch("APWIN.Application")

    # ------------------------------------------------------------------
    # Sub-objects (lazy, cached)
    # ------------------------------------------------------------------

    @cached_property
    def app(self) -> "Application":
        from .application import Application
        return Application(self._com.Application())

    @cached_property
    def gen(self) -> "Gen":
        from .gen import Gen
        return Gen(self._com.Gen())

    @cached_property
    def dgen(self) -> "DGen":
        from .gen import DGen
        return DGen(self._com.DGen())

    @cached_property
    def anlr(self) -> "Anlr":
        from .anlr import Anlr
        return Anlr(self._com.Anlr())

    @cached_property
    def sweep(self) -> "Sweep":
        from .sweep import Sweep
        return Sweep(self._com.Sweep())

    @cached_property
    def data(self) -> "Data":
        from .data import Data
        return Data(self._com.Data())

    @cached_property
    def file(self) -> "APFile":
        from .file import APFile
        return APFile(self._com.File())

    @cached_property
    def log(self) -> "Log":
        from .file import Log
        return Log(self._com.Log())

    @cached_property
    def compute(self) -> "Compute":
        from .compute import Compute
        return Compute(self._com.Compute())

    @cached_property
    def s2dio(self) -> "S2Dio":
        from .digital import S2Dio
        return S2Dio(self._com.S2Dio())

    @cached_property
    def s2dsp(self) -> "S2Dsp":
        from .digital import S2Dsp
        return S2Dsp(self._com.S2Dsp())

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "APWin":
        return self

    def __exit__(self, *_):
        pass

    def quit(self):
        """Close APWin."""
        self._com.Quit()

    def __repr__(self) -> str:
        try:
            return f"<APWin {self._com.Application().Version()}>"
        except Exception:
            return "<APWin>"
