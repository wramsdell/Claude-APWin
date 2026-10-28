"""Wrappers for the APWin File and Log dispinterfaces."""
from __future__ import annotations


class APFile:
    """File open/save operations for tests, data, and waveforms."""

    def __init__(self, com):
        self._com = com

    def open_test(self, filename: str):
        """Load a .at2 test file."""
        self._com.OpenTest(filename)

    def save_test(self):
        """Save the current test (overwrite)."""
        self._com.SaveTest()

    def save_test_as(self, filename: str):
        self._com.SaveTestAs(filename)

    def save_as(self, filename: str):
        self._com.SaveAs(filename)

    def save_all(self):
        self._com.SaveAll()

    def open_data(self, filename: str):
        self._com.OpenData(filename)

    def save_data_as(self, filename: str):
        self._com.SaveDataAs(filename)

    def append_data(self, filename: str):
        self._com.AppendData(filename)

    def open_macro(self, filename: str):
        self._com.OpenMacro(filename)

    def save_macro_as(self, filename: str):
        self._com.SaveMacroAs(filename)

    def open_wfm(self, filename: str, option1: int = 0, option2: int = 0):
        self._com.OpenWfm(filename, option1, option2)

    def save_wfm(self, filename: str, option1: int = 0, option2: int = 0):
        self._com.SaveWfm(filename, option1, option2)

    def save_wfm_as(self, filename: str, option1: int = 0, option2: int = 0):
        self._com.SaveWfmAs(filename, option1, option2)

    def import_ascii_data(self, filename: str):
        self._com.ImportASCIIData(filename)

    def export_ascii_data(self, filename: str):
        self._com.ExportASCIIData(filename)

    def export_graphic(self, filename: str, file_type: int):
        """Export graph as image. file_type: 1=BMP, 2=WMF, etc."""
        self._com.ExportGraphic(filename, file_type)

    def import_dos_s1_test(self, filename: str, ignore_attached: bool = False):
        self._com.ImportDOSS1Test(filename, ignore_attached)

    def __repr__(self) -> str:
        return "<APFile>"


class Log:
    """APWin result log — add entries, view, and print the log file."""

    def __init__(self, com):
        self._com = com

    @property
    def filename(self) -> str:
        return str(self._com.Filename)

    @filename.setter
    def filename(self, value: str):
        self._com.Filename = value

    @property
    def test_name(self) -> str:
        return str(self._com.TestName)

    @test_name.setter
    def test_name(self, value: str):
        self._com.TestName = value

    @property
    def enable(self) -> bool:
        return bool(self._com.Enable)

    @enable.setter
    def enable(self, value: bool):
        self._com.Enable = value

    @property
    def data(self) -> bool:
        return bool(self._com.Data)

    @data.setter
    def data(self, value: bool):
        self._com.Data = value

    @property
    def error_messages(self) -> bool:
        return bool(self._com.ErrorMessages)

    @error_messages.setter
    def error_messages(self, value: bool):
        self._com.ErrorMessages = value

    @property
    def pass_fail_messages(self) -> bool:
        return bool(self._com.PassFailMessages)

    @pass_fail_messages.setter
    def pass_fail_messages(self, value: bool):
        self._com.PassFailMessages = value

    def clear(self):
        self._com.Clear()

    def add_entry(self, text: str):
        self._com.AddEntry(text)

    def add_entry_no_timestamp(self, text: str):
        self._com.AddEntryWithoutTimeDate(text)

    def view(self):
        self._com.View()

    def print_log_file(self):
        self._com.PrintLogFile()

    def __repr__(self) -> str:
        return f"<Log enabled={self.enable}>"
