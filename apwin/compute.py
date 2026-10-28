"""Wrapper for the APWin Compute dispinterface."""
from __future__ import annotations


class Compute:
    """Post-sweep data transformations."""

    def __init__(self, com):
        self._com = com

    def avg(self):
        return self._com.Avg()

    def center(self):
        return self._com.Center()

    def delta(self):
        return self._com.Delta()

    def invert(self):
        return self._com.Invert()

    def linearity(self):
        return self._com.Linearity()

    def max(self):
        return self._com.Max()

    def min(self):
        return self._com.Min()

    def normalize(self):
        return self._com.Normalize()

    def sigma(self):
        return self._com.Sigma()

    def clear(self):
        return self._com.Clear()

    def smooth(self):
        return self._com.Smooth()

    def equalize(self):
        return self._com.Equalize()

    def status(self):
        return self._com.Status()
