"""Wrapper for the APWin Anlr (analog analyzer) dispinterface."""
from __future__ import annotations
from ._util import set_prop


class Anlr:
    """
    Analog analyzer — level, frequency, THD, and phase readings.

    Readings are triggered by calling ``*_trig()`` or by using the settling
    helpers, which poll until the reading stabilises.
    """

    def __init__(self, com):
        self._com = com

    # ------------------------------------------------------------------
    # Configuration vars
    # ------------------------------------------------------------------

    @property
    def func_mode(self):
        return self._com.FuncMode

    @func_mode.setter
    def func_mode(self, value):
        self._com.FuncMode = value

    @property
    def func_input(self):
        return self._com.FuncInput

    @func_input.setter
    def func_input(self, value):
        self._com.FuncInput = value

    @property
    def func_filter(self):
        return self._com.FuncFilter

    @func_filter.setter
    def func_filter(self, value):
        self._com.FuncFilter = value

    @property
    def func_detector(self):
        return self._com.FuncDetector

    @func_detector.setter
    def func_detector(self, value):
        self._com.FuncDetector = value

    @property
    def cha_input(self):
        return self._com.ChAInput

    @cha_input.setter
    def cha_input(self, value):
        self._com.ChAInput = value

    @property
    def chb_input(self):
        return self._com.ChBInput

    @chb_input.setter
    def chb_input(self, value):
        self._com.ChBInput = value

    @property
    def cha_coupling(self):
        return self._com.ChACoupling

    @cha_coupling.setter
    def cha_coupling(self, value):
        self._com.ChACoupling = value

    @property
    def chb_coupling(self):
        return self._com.ChBCoupling

    @chb_coupling.setter
    def chb_coupling(self, value):
        self._com.ChBCoupling = value

    @property
    def rdg_rate(self):
        return self._com.RdgRate

    @rdg_rate.setter
    def rdg_rate(self, value):
        self._com.RdgRate = value

    @property
    def cha_impedance(self):
        return self._com.ChAImpedance

    @cha_impedance.setter
    def cha_impedance(self, value):
        self._com.ChAImpedance = value

    @property
    def chb_impedance(self):
        return self._com.ChBImpedance

    @chb_impedance.setter
    def chb_impedance(self, value):
        self._com.ChBImpedance = value

    # ------------------------------------------------------------------
    # Ready flags
    # ------------------------------------------------------------------

    @property
    def func_ready(self) -> bool:
        return bool(self._com.FuncReady)

    @property
    def level_ready(self) -> bool:
        return bool(self._com.LevelReady)

    @property
    def cha_level_ready(self) -> bool:
        return bool(self._com.ChALevelReady)

    @property
    def chb_level_ready(self) -> bool:
        return bool(self._com.ChBLevelReady)

    @property
    def freq_ready(self) -> bool:
        return bool(self._com.FreqReady)

    @property
    def phase_ready(self) -> bool:
        return bool(self._com.PhaseReady)

    # ------------------------------------------------------------------
    # Trigger methods
    # ------------------------------------------------------------------

    def func_trig(self):
        self._com.FuncTrig()

    def level_trig(self):
        self._com.LevelTrig()

    def cha_level_trig(self):
        self._com.ChALevelTrig()

    def chb_level_trig(self):
        self._com.ChBLevelTrig()

    def freq_trig(self):
        self._com.FreqTrig()

    def cha_freq_trig(self):
        self._com.ChAFreqTrig()

    def chb_freq_trig(self):
        self._com.ChBFreqTrig()

    def phase_trig(self):
        self._com.PhaseTrig()

    # ------------------------------------------------------------------
    # Settling helpers
    # ------------------------------------------------------------------

    def func_settling(self, tolerance, floor, unit: str, points: int,
                      delay: float, algorithm: int):
        self._com.FuncSettling(tolerance, floor, unit, points, delay, algorithm)

    def level_settling(self, tolerance, floor, unit: str, points: int,
                       delay: float, algorithm: int):
        self._com.LevelSettling(tolerance, floor, unit, points, delay, algorithm)

    def freq_settling(self, tolerance, floor, unit: str, points: int,
                      delay: float, algorithm: int):
        self._com.FreqSettling(tolerance, floor, unit, points, delay, algorithm)

    def phase_settling(self, tolerance, floor, unit: str, points: int,
                       delay: float, algorithm: int):
        self._com.PhaseSettling(tolerance, floor, unit, points, delay, algorithm)

    # ------------------------------------------------------------------
    # Readings (getter only — readings come from the instrument)
    # ------------------------------------------------------------------

    def func_rdg(self, unit: str = "dBr") -> float:
        return float(self._com.FuncRdg(unit))

    def level_rdg(self, unit: str = "dBV") -> float:
        return float(self._com.LevelRdg(unit))

    def cha_level_rdg(self, unit: str = "dBV") -> float:
        return float(self._com.ChALevelRdg(unit))

    def chb_level_rdg(self, unit: str = "dBV") -> float:
        return float(self._com.ChBLevelRdg(unit))

    def freq_rdg(self, unit: str = "Hz") -> float:
        return float(self._com.FreqRdg(unit))

    def cha_freq_rdg(self, unit: str = "Hz") -> float:
        return float(self._com.ChAFreqRdg(unit))

    def chb_freq_rdg(self, unit: str = "Hz") -> float:
        return float(self._com.ChBFreqRdg(unit))

    def phase_rdg(self, unit: str = "Deg") -> float:
        return float(self._com.PhaseRdg(unit))

    # ------------------------------------------------------------------
    # Range
    # ------------------------------------------------------------------

    def get_cha_range(self, unit: str = "dBV") -> float:
        return float(self._com.ChARange(unit))

    def set_cha_range(self, value: float, unit: str = "dBV"):
        set_prop(self._com, "ChARange", unit, value)

    def get_chb_range(self, unit: str = "dBV") -> float:
        return float(self._com.ChBRange(unit))

    def set_chb_range(self, value: float, unit: str = "dBV"):
        set_prop(self._com, "ChBRange", unit, value)

    @property
    def cha_range_auto(self) -> bool:
        return bool(self._com.ChARangeAuto)

    @cha_range_auto.setter
    def cha_range_auto(self, value: bool):
        self._com.ChARangeAuto = value

    @property
    def chb_range_auto(self) -> bool:
        return bool(self._com.ChBRangeAuto)

    @chb_range_auto.setter
    def chb_range_auto(self, value: bool):
        self._com.ChBRangeAuto = value

    # ------------------------------------------------------------------
    # Reference levels
    # ------------------------------------------------------------------

    def get_ref_freq(self, unit: str = "Hz") -> float:
        return float(self._com.RefFreq(unit))

    def set_ref_freq(self, value: float, unit: str = "Hz"):
        set_prop(self._com, "RefFreq", unit, value)

    def ref_freq_auto(self):
        self._com.RefFreqAuto()

    def get_ref_dbr(self, unit: str = "dBV") -> float:
        return float(self._com.RefdBr(unit))

    def set_ref_dbr(self, value: float, unit: str = "dBV"):
        set_prop(self._com, "RefdBr", unit, value)

    def ref_dbr_auto(self):
        self._com.RefdBrAuto()

    def __repr__(self) -> str:
        try:
            return f"<Anlr level={self.cha_level_rdg('dBV'):.2f}dBV freq={self.freq_rdg('Hz'):.1f}Hz>"
        except Exception:
            return "<Anlr>"
