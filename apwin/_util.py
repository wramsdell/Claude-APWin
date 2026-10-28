"""COM dispatch helpers for APWin's indexed property puts."""
import pythoncom


def set_prop(com_obj, prop_name: str, unit: str, value: float) -> None:
    """
    Set an indexed IDispatch property by name.

    AP's unit-string properties (e.g. Gen.Freq) are defined in the type
    library as:
        [propget] Freq(UnitString: BSTR) -> R8
        [propput] Freq(UnitString: BSTR, value: R8)

    The getter returns the numeric value in the given unit; the setter
    takes the unit string as an index parameter plus a separate float.

    IDispatch indexed PROPERTYPUT convention:
      - Index arg (UnitString) is a positional arg
      - The value being put is the DISPID_PROPERTYPUT named arg (last arg)
    In pywin32 this is: Invoke(dispid, 0, PROPERTYPUT, 0, unit, value)
    """
    dispid = com_obj._oleobj_.GetIDsOfNames(0, prop_name)
    com_obj._oleobj_.Invoke(
        dispid, 0,
        pythoncom.DISPATCH_PROPERTYPUT,
        0,
        unit, float(value)
    )
