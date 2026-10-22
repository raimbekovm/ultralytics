import json
import os
import pathlib
import subprocess
import sys

# usage: probe.py <role> <out.json>; forces the get_user_config_dir fallback and writes a setting
role, out = sys.argv[1], pathlib.Path(sys.argv[2])
os.environ["USERPROFILE"] = r"C:\probe_home_file"  # a FILE, so the primary AppData mkdir fails
os.environ["TEMP"] = os.environ["TMP"] = r"C:\probe_tmp"
os.environ["YOLO_OFFLINE"] = "1"
res = {"role": role, "py": sys.version.split()[0]}
groups = subprocess.run(["whoami", "/groups", "/fo", "csv"], capture_output=True, text=True).stdout
res["admin_group"] = [line for line in groups.splitlines() if "S-1-5-32-544" in line]
try:
    sys.path.insert(0, os.environ.get("PROBE_SRC", os.getcwd()))
    from ultralytics.utils import SETTINGS, USER_CONFIG_DIR

    res["config_dir"] = str(USER_CONFIG_DIR)
    SETTINGS.update(mlflow=(role == "elevated"))
    saved = json.loads((USER_CONFIG_DIR / "settings.json").read_text())
    res["persisted"] = saved["mlflow"] is (role == "elevated")
except Exception as e:
    res["error"] = f"{type(e).__name__}: {e}"
res["icacls"] = subprocess.run(["icacls", r"C:\probe_tmp\Ultralytics"], capture_output=True, text=True).stdout
out.write_text(json.dumps(res, indent=1))
