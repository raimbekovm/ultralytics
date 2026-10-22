import json
import os
import pathlib
import sys

# usage: control.py <elevated|basic> <dir> <700|default> <out.json>
role, d, mode, out = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3], pathlib.Path(sys.argv[4])
res = {"role": role, "dir": str(d), "mode": mode, "py": sys.version.split()[0]}
try:
    if role == "elevated":
        os.mkdir(d, 0o700) if mode == "700" else os.mkdir(d)
    (d / f"{role}.txt").write_text("x")
    res["write"] = "ok"
except Exception as e:
    res["write"] = f"{type(e).__name__}: {e}"
out.write_text(json.dumps(res))
