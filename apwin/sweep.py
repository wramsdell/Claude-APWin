"""Wrapper for the APWin Sweep dispinterface."""
from __future__ import annotations
import time
from ._util import set_prop


class SweepSource:
    """Sweep source axis (Source1 or Source2)."""

    def __init__(self, com):
        self._com = com

    def get_start(self, unit: str = "Hz") -> float:
        return float(self._com.Start(unit))

    def set_start(self, value: float, unit: str = "Hz"):
        set_prop(self._com, "Start", unit, value)

    start = property(lambda self: self.get_start(), lambda self, v: self.set_start(v))

    def get_stop(self, unit: str = "Hz") -> float:
        return float(self._com.Stop(unit))

    def set_stop(self, value: float, unit: str = "Hz"):
        set_prop(self._com, "Stop", unit, value)

    stop = property(lambda self: self.get_stop(), lambda self, v: self.set_stop(v))

    def get_stepsize(self, unit: str = "Hz") -> float:
        return float(self._com.Stepsize(unit))

    def set_stepsize(self, value: float, unit: str = "Hz"):
        set_prop(self._com, "Stepsize", unit, value)

    stepsize = property(lambda self: self.get_stepsize(), lambda self, v: self.set_stepsize(v))

    @property
    def steps(self) -> int:
        return int(self._com.Steps)

    @steps.setter
    def steps(self, value: int):
        self._com.Steps = value

    @property
    def log_lin(self):
        return self._com.LogLin

    @log_lin.setter
    def log_lin(self, value):
        self._com.LogLin = value

    def set_table(self, filename: str, column: int = 1):
        self._com.Table(filename, column)


class SweepData:
    """Sweep data trace (Data1–Data6)."""

    def __init__(self, com):
        self._com = com

    def get_top(self, unit: str = "dBV") -> float:
        return float(self._com.Top(unit))

    def set_top(self, value, unit: str = "dBV"):
        self._com.Top = f"{value} {unit}" if isinstance(value, (int, float)) else value

    top = property(lambda self: self.get_top(), lambda self, v: self.set_top(v))

    def get_bottom(self, unit: str = "dBV") -> float:
        return float(self._com.Bottom(unit))

    def set_bottom(self, value, unit: str = "dBV"):
        self._com.Bottom = f"{value} {unit}" if isinstance(value, (int, float)) else value

    bottom = property(lambda self: self.get_bottom(), lambda self, v: self.set_bottom(v))

    @property
    def autoscale(self) -> bool:
        return bool(self._com.Autoscale)

    @autoscale.setter
    def autoscale(self, value: bool):
        self._com.Autoscale = value

    @property
    def color(self):
        return self._com.Color

    @color.setter
    def color(self, value):
        self._com.Color = value

    @property
    def log_lin(self):
        return self._com.LogLin

    @log_lin.setter
    def log_lin(self, value):
        self._com.LogLin = value

    def set_limits(self, filename: str, column: int, upper: bool):
        self._com.Limits(filename, column, upper)

    def upper_limit(self):
        return self._com.UpperLimit()

    def lower_limit(self):
        return self._com.LowerLimit()


class Sweep:
    """
    Sweep control — configure, start, monitor and stop sweeps.

    Typical usage::

        ap.sweep.source1.start = "20 Hz"
        ap.sweep.source1.stop = "20 kHz"
        ap.sweep.start()
        ap.sweep.wait()           # blocks until done
    """

    def __init__(self, com):
        self._com = com

    # ------------------------------------------------------------------
    # Sub-objects
    # ------------------------------------------------------------------

    def source1(self) -> SweepSource:
        return SweepSource(self._com.Source1())

    def source2(self) -> SweepSource:
        return SweepSource(self._com.Source2())

    def data(self, n: int) -> SweepData:
        """Return SweepData for trace n (1–6)."""
        if n < 1 or n > 6:
            raise ValueError("n must be 1–6")
        return SweepData(getattr(self._com, f"Data{n}")())

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @property
    def append(self) -> bool:
        return bool(self._com.Append)

    @append.setter
    def append(self, value: bool):
        self._com.Append = value

    @property
    def repeat(self) -> bool:
        return bool(self._com.Repeat)

    @repeat.setter
    def repeat(self, value: bool):
        self._com.Repeat = value

    @property
    def single_point(self) -> bool:
        return bool(self._com.SinglePoint)

    @single_point.setter
    def single_point(self, value: bool):
        self._com.SinglePoint = value

    @property
    def stereo(self) -> bool:
        return bool(self._com.Stereo)

    @stereo.setter
    def stereo(self, value: bool):
        self._com.Stereo = value

    @property
    def create_graph(self) -> bool:
        return bool(self._com.CreateGraph)

    @create_graph.setter
    def create_graph(self, value: bool):
        self._com.CreateGraph = value

    @property
    def create_table(self) -> bool:
        return bool(self._com.CreateTable)

    @create_table.setter
    def create_table(self, value: bool):
        self._com.CreateTable = value

    def get_timeout(self, unit: str = "s") -> float:
        return float(self._com.Timeout(unit))

    def set_timeout(self, value: float, unit: str = "s"):
        set_prop(self._com, "Timeout", unit, value)

    timeout = property(lambda self: self.get_timeout(), lambda self, v: self.set_timeout(v))

    # ------------------------------------------------------------------
    # Sweep control
    # ------------------------------------------------------------------

    def start(self):
        """Start sweep and block until complete."""
        self._com.Start()

    def start_no_wait(self):
        """Start sweep and return immediately."""
        self._com.StartNoWait()

    def start_with_append(self):
        self._com.StartWithAppend()

    def start_with_repeat(self):
        self._com.StartWithRepeat()

    def stop(self):
        self._com.Stop()

    def is_running(self) -> bool:
        return bool(self._com.IsRunning())

    def wait(self, poll_interval: float = 0.1, timeout: float = 300.0):
        """
        Block until the sweep completes or *timeout* seconds elapse.

        Raises ``TimeoutError`` if the sweep is still running after *timeout*.
        """
        deadline = time.monotonic() + timeout
        while self.is_running():
            if time.monotonic() > deadline:
                raise TimeoutError(f"Sweep did not complete within {timeout}s")
            time.sleep(poll_interval)

    def run(self, timeout: float = 300.0, poll_interval: float = 0.1):
        """Start sweep and wait for it to finish."""
        self.start_no_wait()
        self.wait(poll_interval=poll_interval, timeout=timeout)

    # ------------------------------------------------------------------
    # Post-processing
    # ------------------------------------------------------------------

    def recompare(self):
        self._com.Recompare()

    def retransform(self):
        self._com.Retransform()

    def reprocess(self):
        self._com.Reprocess()

    def copy_data1_to_2(self):
        self._com.CopyData1to2()

    def copy_data2_to_1(self):
        self._com.CopyData2to1()

    def reverse_channels(self, reversed_: bool):
        self._com.ReverseChannels(reversed_)

    def __repr__(self) -> str:
        try:
            return f"<Sweep running={self.is_running()}>"
        except Exception:
            return "<Sweep>"
