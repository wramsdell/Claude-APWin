import sys, os
paths = [
    r"C:\src\Claude-APWin\ping.txt",
    r"C:\Users\Public\ping.txt",
]
for p in paths:
    try:
        with open(p, "w") as f:
            f.write(f"ping from pid={os.getpid()} user={os.environ.get('USERNAME','?')} python={sys.version}\n")
        print(f"wrote {p}")
    except Exception as e:
        print(f"failed {p}: {e}")
