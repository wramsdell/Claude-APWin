"""Wrappers for S2Dio and S2Dsp (digital I/O and DSP) dispinterfaces."""
from __future__ import annotations
from ._util import set_prop


class S2Dio:
    """
    S2 digital I/O — sample rate, jitter, voltage, and AES/EBU signal
    measurements for the SYS-2322's digital analyzer.
    """

    def __init__(self, com):
        self._com = com

    # ------------------------------------------------------------------
    # Input configuration
    # ------------------------------------------------------------------

    @property
    def in_format(self):
        return self._com.InFormat

    @in_format.setter
    def in_format(self, value):
        self._com.InFormat = value

    @property
    def in_impedance(self):
        return self._com.InImpedance

    @in_impedance.setter
    def in_impedance(self, value):
        self._com.InImpedance = value

    @property
    def in_monitor_mode(self):
        return self._com.InMonitorMode

    @in_monitor_mode.setter
    def in_monitor_mode(self, value):
        self._com.InMonitorMode = value

    # ------------------------------------------------------------------
    # Output configuration
    # ------------------------------------------------------------------

    @property
    def out_format(self):
        return self._com.OutFormat

    @out_format.setter
    def out_format(self, value):
        self._com.OutFormat = value

    @property
    def out_resolution(self):
        return self._com.OutResolution

    @out_resolution.setter
    def out_resolution(self, value):
        self._com.OutResolution = value

    def get_out_rate(self, unit: str = "Hz") -> float:
        return float(self._com.OutRate(unit))

    def set_out_rate(self, value: float, unit: str = "Hz"):
        set_prop(self._com, "OutRate", unit, value)

    def get_out_voltage(self, unit: str = "Vp") -> float:
        return float(self._com.OutVoltage(unit))

    def set_out_voltage(self, value: float, unit: str = "Vp"):
        set_prop(self._com, "OutVoltage", unit, value)

    # ------------------------------------------------------------------
    # Ready flags
    # ------------------------------------------------------------------

    @property
    def voltage_ready(self) -> bool:
        return bool(self._com.VoltageReady)

    @property
    def rate_ready(self) -> bool:
        return bool(self._com.RateReady)

    @property
    def jitter_ready(self) -> bool:
        return bool(self._com.JitterReady)

    @property
    def delay_ready(self) -> bool:
        return bool(self._com.DelayReady)

    @property
    def cha_peak_ready(self) -> bool:
        return bool(self._com.ChAPeakReady)

    @property
    def chb_peak_ready(self) -> bool:
        return bool(self._com.ChBPeakReady)

    # ------------------------------------------------------------------
    # Trigger methods
    # ------------------------------------------------------------------

    def voltage_trig(self):
        self._com.VoltageTrig()

    def rate_trig(self):
        self._com.RateTrig()

    def jitter_trig(self):
        self._com.JitterTrig()

    def delay_trig(self):
        self._com.DelayTrig()

    def cha_peak_trig(self):
        self._com.ChAPeakTrig()

    def chb_peak_trig(self):
        self._com.ChBPeakTrig()

    # ------------------------------------------------------------------
    # Readings
    # ------------------------------------------------------------------

    def voltage_rdg(self, unit: str = "Vp") -> float:
        return float(self._com.VoltageRdg(unit))

    def rate_rdg(self, unit: str = "Hz") -> float:
        return float(self._com.RateRdg(unit))

    def jitter_rdg(self, unit: str = "ns") -> float:
        return float(self._com.JitterRdg(unit))

    def delay_rdg(self, unit: str = "ns") -> float:
        return float(self._com.DelayRdg(unit))

    def cha_peak_rdg(self, unit: str = "dBFS") -> float:
        return float(self._com.ChAPeakRdg(unit))

    def chb_peak_rdg(self, unit: str = "dBFS") -> float:
        return float(self._com.ChBPeakRdg(unit))

    # ------------------------------------------------------------------
    # Error flags
    # ------------------------------------------------------------------

    def flag_invalid_rdg(self) -> bool:
        return bool(self._com.FlagInvalidRdg())

    def flag_lock_rdg(self) -> bool:
        return bool(self._com.FlagLockRdg())

    def flag_parity_rdg(self) -> bool:
        return bool(self._com.FlagParityRdg())

    def flag_coding_rdg(self) -> bool:
        return bool(self._com.FlagCodingRdg())

    def flag_confidence_rdg(self) -> bool:
        return bool(self._com.FlagConfidenceRdg())

    # ------------------------------------------------------------------
    # Settling
    # ------------------------------------------------------------------

    def voltage_settling(self, tolerance, floor, unit, points, delay, algorithm):
        self._com.VoltageSettling(tolerance, floor, unit, points, delay, algorithm)

    def rate_settling(self, tolerance, floor, unit, points, delay, algorithm):
        self._com.RateSettling(tolerance, floor, unit, points, delay, algorithm)

    def jitter_settling(self, tolerance, floor, unit, points, delay, algorithm):
        self._com.JitterSettling(tolerance, floor, unit, points, delay, algorithm)

    def __repr__(self) -> str:
        return "<S2Dio>"


class S2Dsp:
    """
    S2 DSP module access — returns sub-objects for FFT, Analyzer,
    FastTest, MLS, BitTest, and Intervu programs.
    """

    def __init__(self, com):
        self._com = com

    @property
    def program(self):
        return self._com.Program

    @program.setter
    def program(self, value):
        self._com.Program = value

    def fft(self):
        return self._com.FFT()

    def analyzer(self):
        return self._com.Analyzer()

    def fast_test(self):
        return self._com.FastTest()

    def mls(self):
        return self._com.Mls()

    def bit_test(self):
        return self._com.BitTest()

    def intervu(self):
        return self._com.Intervu()

    def get_ref_vfs(self, unit: str = "dBV") -> float:
        return float(self._com.RefVFS(unit))

    def set_ref_vfs(self, value: float, unit: str = "dBV"):
        set_prop(self._com, "RefVFS", unit, value)

    def get_ref_freq(self, unit: str = "Hz") -> float:
        return float(self._com.RefFreq(unit))

    def set_ref_freq(self, value: float, unit: str = "Hz"):
        set_prop(self._com, "RefFreq", unit, value)

    def __repr__(self) -> str:
        return "<S2Dsp>"
