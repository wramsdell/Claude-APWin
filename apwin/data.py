"""Wrapper for the APWin Data dispinterface (sweep results)."""
from __future__ import annotations
from typing import List, Optional


class Data:
    """
    Access sweep result data by dataset id, column, and row index.

    Dataset IDs are string names (e.g. ``"Data1"``) as shown in the APWin
    data editor.  Column numbers are 1-based.
    """

    def __init__(self, com):
        self._com = com

    # ------------------------------------------------------------------
    # Dataset information
    # ------------------------------------------------------------------

    def id(self, dataname: str) -> int:
        """Return the numeric id for a named dataset."""
        return int(self._com.Id(dataname))

    def col_num_of(self, id: int) -> int:
        """Number of columns in dataset *id*."""
        return int(self._com.ColNumOf(id))

    def col_name(self, id: int, column: int) -> str:
        """Name of column *column* in dataset *id*."""
        return str(self._com.ColName(id, column))

    def col_unit(self, id: int, column: int) -> str:
        """Unit string of column *column* in dataset *id*."""
        return str(self._com.ColUnit(id, column))

    def col_size(self, id: int, column: int) -> int:
        """Number of rows in column *column* of dataset *id*."""
        return int(self._com.ColSize(id, column))

    # ------------------------------------------------------------------
    # Reading values
    # ------------------------------------------------------------------

    def value(self, id: int, column: int, index: int, unit: str = "") -> float:
        """Read a single value from row *index* (1-based) of *column*."""
        return float(self._com.Value(id, column, index, unit))

    def xfer_to_array(self, id: int, column: int, unit: str = "") -> list:
        """
        Return all rows from *column* as a Python list.

        If numpy is available, returns a numpy array instead.
        """
        raw = self._com.XferToArray(id, column, unit)
        try:
            import numpy as np
            return np.array(raw)
        except ImportError:
            return list(raw)

    def column_values(self, id: int, column: int, unit: str = "") -> list:
        """Convenience: read every row of *column* individually."""
        n = self.col_size(id, column)
        return [self.value(id, column, i + 1, unit) for i in range(n)]

    # ------------------------------------------------------------------
    # Status / limits
    # ------------------------------------------------------------------

    def status(self, id: int, column: int, index: int):
        return self._com.Status(id, column, index)

    def upper_limit_error(self, id: int) -> bool:
        return bool(self._com.UpperLimitError(id))

    def lower_limit_error(self, id: int) -> bool:
        return bool(self._com.LowerLimitError(id))

    def limit_error(self, id: int) -> bool:
        return bool(self._com.LimitError(id))

    def col_limit_error(self, id: int, column: int) -> bool:
        return bool(self._com.ColLimitError(id, column))

    def col_upper_limit_error(self, id: int, column: int) -> bool:
        return bool(self._com.ColUpperLimitError(id, column))

    def col_lower_limit_error(self, id: int, column: int) -> bool:
        return bool(self._com.ColLowerLimitError(id, column))

    # ------------------------------------------------------------------
    # Display / editing
    # ------------------------------------------------------------------

    def update_display(self, id: int):
        self._com.UpdateDisplay(id)

    def optimize_display(self, id: int):
        self._com.OptimizeDisplay(id)

    def insert_row_before(self, id: int, row_num: int):
        self._com.InsertRowBefore(id, row_num)

    def insert_row_after(self, id: int, row_num: int):
        self._com.InsertRowAfter(id, row_num)

    def add_row_to_end(self, id: int):
        self._com.AddRowToEnd(id)

    def delete_row(self, id: int, row_num: int):
        self._com.DeleteRow(id, row_num)

    def __repr__(self) -> str:
        return "<Data>"
