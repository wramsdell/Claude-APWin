# Claude-APWin

Python automation library for the Audio Precision APWin COM interface, targeting the AP SYS-2322 audio analyzer.

## Requirements

- Windows
- Audio Precision APWin 200 installed (`C:\Program Files (x86)\Audio Precision\Apwin200\Apwin.exe`)
- Python 3.9+
- APWin must be running **as Administrator** (the COM server requires elevation)

## Setup

After cloning, create and activate a virtual environment and install dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Connecting to APWin

APWin's COM server (`APWIN.Application`) requires an elevated process. Either:

- Run your script from an **Administrator** PowerShell/cmd, or
- Launch APWin via `Start-Process ... -Verb RunAs` and connect from an elevated shell

```python
import win32com.client

ap = win32com.client.GetActiveObject("APWIN.Application")
```
