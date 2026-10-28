"""Wrappers for the APWin Gen (analog) and DGen (digital) generators."""
from __future__ import annotations
from ._util import set_prop


class _GenBase:
    """Shared generator functionality."""

    def __init__(self, com):
        self._com = com

    # ------------------------------------------------------------------
    # Frequency
    # ------------------------------------------------------------------

    def get_freq(self, unit: str = "Hz") -> float:
        return float(self._com.Freq(unit))

    def set_freq(self, value: float, unit: str = "Hz"):
        """Set frequency.  set_freq(1000) or set_freq(1000, 'Hz')."""
        set_prop(self._com, "Freq", unit, value)

    # ------------------------------------------------------------------
    # Amplitude
    # ------------------------------------------------------------------

    def get_ampl(self, unit: str = "dBV") -> float:
        return float(self._com.Ampl(unit))

    def set_ampl(self, value: float, unit: str = "dBV"):
        """Set amplitude.  set_ampl(-20) or set_ampl(0.1, 'Vrms')."""
        set_prop(self._com, "Ampl", unit, value)

    # ------------------------------------------------------------------
    # Output on/off
    # ------------------------------------------------------------------

    @property
    def output(self) -> bool:
        return bool(self._com.Output)

    @output.setter
    def output(self, value: bool):
        self._com.Output = value

    # ------------------------------------------------------------------
    # Waveform
    # ------------------------------------------------------------------

    @property
    def wfm_name(self) -> str:
        return str(self._com.WfmName)

    def set_wfm(self, primary: int, secondary: int = 0):
        self._com.Wfm(primary, secondary)

    # ------------------------------------------------------------------
    # Reference levels
    # ------------------------------------------------------------------

    def get_ref_dbr(self, unit: str = "dBV") -> float:
        return float(self._com.RefdBr(unit))

    def set_ref_dbr(self, value: float, unit: str = "dBV"):
        set_prop(self._com, "RefdBr", unit, value)

    def ref_dbr_auto(self):
        self._com.RefdBrAuto()

    def get_ref_freq(self, unit: str = "Hz") -> float:
        return float(self._com.RefFreq(unit))

    def set_ref_freq(self, value: float, unit: str = "Hz"):
        set_prop(self._com, "RefFreq", unit, value)

    def ref_freq_auto(self):
        self._com.RefFreqAuto()

    # ------------------------------------------------------------------
    # Channel A / B amplitude
    # ------------------------------------------------------------------

    def get_cha_ampl(self, unit: str = "dBV") -> float:
        return float(self._com.ChAAmpl(unit))

    def set_cha_ampl(self, value: float, unit: str = "dBV"):
        set_prop(self._com, "ChAAmpl", unit, value)

    def get_chb_ampl(self, unit: str = "dBV") -> float:
        return float(self._com.ChBAmpl(unit))

    def set_chb_ampl(self, value: float, unit: str = "dBV"):
        set_prop(self._com, "ChBAmpl", unit, value)

    # ------------------------------------------------------------------
    # Phase
    # ------------------------------------------------------------------

    def get_phase(self, unit: str = "Deg") -> float:
        return float(self._com.Phase(unit))

    def set_phase(self, value: float, unit: str = "Deg"):
        set_prop(self._com, "Phase", unit, value)

    # ------------------------------------------------------------------
    # Burst
    # ------------------------------------------------------------------

    def get_burst_level(self, unit: str = "dBV") -> float:
        return float(self._com.BurstLevel(unit))

    def set_burst_level(self, value: float, unit: str = "dBV"):
        set_prop(self._com, "BurstLevel", unit, value)

    def get_burst_on_time(self, unit: str = "s") -> float:
        return float(self._com.BurstOnTime(unit))

    def set_burst_on_time(self, value: float, unit: str = "s"):
        set_prop(self._com, "BurstOnTime", unit, value)

    def get_burst_interval(self, unit: str = "s") -> float:
        return float(self._com.BurstInterval(unit))

    def set_burst_interval(self, value: float, unit: str = "s"):
        set_prop(self._com, "BurstInterval", unit, value)

    # ------------------------------------------------------------------
    # EQ curve
    # ------------------------------------------------------------------

    def set_eq_curve(self, filename: str, column: int = 1):
        self._com.EqCurve(filename, column)

    @property
    def eq_curve_filename(self) -> str:
        return str(self._com.EqCurveFilename())

    @property
    def eq_curve_column(self) -> int:
        return int(self._com.EqCurveColumn())

    # ------------------------------------------------------------------
    # Auto-on
    # ------------------------------------------------------------------

    @property
    def auto_on(self) -> bool:
        return bool(self._com.AutoOn)

    @auto_on.setter
    def auto_on(self, value: bool):
        self._com.AutoOn = value


class Gen(_GenBase):
    """Analog generator (Gen panel)."""

    @property
    def cha_output(self) -> bool:
        return bool(self._com.ChAOutput)

    @cha_output.setter
    def cha_output(self, value: bool):
        self._com.ChAOutput = value

    @property
    def chb_output(self) -> bool:
        return bool(self._com.ChBOutput)

    @chb_output.setter
    def chb_output(self, value: bool):
        self._com.ChBOutput = value

    @property
    def cha_invert(self) -> bool:
        return bool(self._com.ChAInvert)

    @cha_invert.setter
    def cha_invert(self, value: bool):
        self._com.ChAInvert = value

    @property
    def chb_invert(self) -> bool:
        return bool(self._com.ChBInvert)

    @chb_invert.setter
    def chb_invert(self, value: bool):
        self._com.ChBInvert = value

    @property
    def chb_track_a(self) -> bool:
        return bool(self._com.ChBTrackA)

    @chb_track_a.setter
    def chb_track_a(self, value: bool):
        self._com.ChBTrackA = value

    @property
    def config(self):
        return self._com.Config

    @config.setter
    def config(self, value):
        self._com.Config = value

    @property
    def impedance(self):
        return self._com.Impedance

    @impedance.setter
    def impedance(self, value):
        self._com.Impedance = value

    def __repr__(self) -> str:
        try:
            return f"<Gen freq={self.get_freq('Hz'):.1f}Hz ampl={self.get_ampl('dBV'):.2f}dBV out={self.output}>"
        except Exception:
            return "<Gen>"


class DGen(_GenBase):
    """Digital generator (DGen panel)."""

    @property
    def cha_output(self) -> bool:
        return bool(self._com.ChAOutput)

    @cha_output.setter
    def cha_output(self, value: bool):
        self._com.ChAOutput = value

    @property
    def chb_output(self) -> bool:
        return bool(self._com.ChBOutput)

    @chb_output.setter
    def chb_output(self, value: bool):
        self._com.ChBOutput = value

    @property
    def step_rate(self):
        return self._com.StepRate

    @step_rate.setter
    def step_rate(self, value):
        self._com.StepRate = value

    @property
    def dither_type(self):
        return self._com.DitherType

    @dither_type.setter
    def dither_type(self, value):
        self._com.DitherType = value

    def get_ref_vfs(self, unit: str = "dBV") -> float:
        return float(self._com.RefVFS(unit))

    def set_ref_vfs(self, value: float, unit: str = "dBV"):
        set_prop(self._com, "RefVFS", unit, value)

    def get_offset(self, unit: str = "dBFS") -> float:
        return float(self._com.OffSet(unit))

    def set_offset(self, value: float, unit: str = "dBFS"):
        set_prop(self._com, "OffSet", unit, value)

    def __repr__(self) -> str:
        try:
            return f"<DGen freq={self.get_freq('Hz'):.1f}Hz ampl={self.get_ampl('dBFS'):.2f}dBFS out={self.output}>"
        except Exception:
            return "<DGen>"
