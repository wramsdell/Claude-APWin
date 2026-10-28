"""Wrapper for the APWin Application dispinterface."""
from __future__ import annotations


class Application:
    """APWin application-level control."""

    def __init__(self, com):
        self._com = com

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def visible(self) -> bool:
        return bool(self._com.Visible)

    @visible.setter
    def visible(self, value: bool):
        self._com.Visible = value

    @property
    def working_dir(self) -> str:
        return str(self._com.WorkingDir)

    @working_dir.setter
    def working_dir(self, path: str):
        self._com.WorkingDir = path

    @property
    def suppress_errors(self) -> bool:
        return bool(self._com.SuppressErrorMessages)

    @suppress_errors.setter
    def suppress_errors(self, value: bool):
        self._com.SuppressErrorMessages = value

    @property
    def throw_errors(self) -> bool:
        return bool(self._com.ThrowErrors)

    @throw_errors.setter
    def throw_errors(self, value: bool):
        self._com.ThrowErrors = value

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def version(self) -> str:
        return str(self._com.Version())

    def name(self) -> str:
        return str(self._com.Name())

    def sys_type(self) -> str:
        """Return the connected instrument type string (e.g. 'SYS-2322')."""
        return str(self._com.SysType())

    def app_dir(self) -> str:
        return str(self._com.AppDir())

    def test_dir(self) -> str:
        return str(self._com.TestDir())

    def test_name(self) -> str:
        return str(self._com.TestName())

    def macro_dir(self) -> str:
        return str(self._com.MacroDir())

    def is_demo_mode(self) -> bool:
        return bool(self._com.IsDemoMode())

    def do_readings(self):
        """Trigger a single set of meter readings."""
        self._com.DoReadings()

    def clear_current_error(self):
        self._com.ClearCurrentError()

    def get_current_error(self) -> str:
        return str(self._com.GetCurrentErrorString())

    def display_current_error(self):
        self._com.DisplayCurrentError()

    def quit(self):
        self._com.Quit()

    def panel_open(self, panel_id: int):
        self._com.PanelOpen(panel_id)

    def panel_close(self, panel_id: int):
        self._com.PanelClose(panel_id)

    def panel_toolbar_visible(self, visible: bool):
        self._com.PanelToolbarVisible(visible)

    def copy_panel_to_clipboard(self):
        self._com.CopyPanelToClipboard()

    def set_watchdog_timer(self, timer: int, seconds: float, throw_error: bool = True):
        """Set watchdog timer 1 or 2."""
        if timer == 1:
            self._com.SetWatchDogTimer1(seconds, throw_error)
        elif timer == 2:
            self._com.SetWatchDogTimer2(seconds, throw_error)
        else:
            raise ValueError("timer must be 1 or 2")

    def __repr__(self) -> str:
        try:
            return f"<Application {self.sys_type()} v{self.version()}>"
        except Exception:
            return "<Application>"
