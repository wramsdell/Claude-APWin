"""Generate early-bound win32com stubs for APWin and show the Gen class."""
import sys, os

sys.path.insert(0, r"C:\src\Claude-APWin")

# Generate stubs into our package directory
gen_dir = r"C:\src\Claude-APWin\win32com_gen"
os.makedirs(gen_dir, exist_ok=True)

from win32com.client import gencache
import win32com.client.makepy as makepy

# Generate from the CLSID / ProgID
print("Generating stubs for APWIN.Application ...")
makepy.GenerateFromTypeLibSpec("APWIN.Application", verboseLevel=1)

# Find the generated file
import win32com.client.gencache as gc
print("\nGenerated cache dir:", gc.GetGeneratePath())

# Show a snippet of the Gen class from the stubs
cache_dir = gc.GetGeneratePath()
for fn in os.listdir(cache_dir):
    if fn.endswith(".py"):
        path = os.path.join(cache_dir, fn)
        txt = open(path).read()
        if "def Freq" in txt or "Freq =" in txt:
            # Print lines around Freq
            lines = txt.splitlines()
            for i, line in enumerate(lines):
                if "Freq" in line:
                    start = max(0, i-1)
                    end = min(len(lines), i+6)
                    print(f"\n--- {fn} line {i+1} ---")
                    print("\n".join(lines[start:end]))
            break
