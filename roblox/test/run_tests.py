"""Automated play-test of the Rojo project inside a real Roblox Studio (Windows).

    python roblox/test/run_tests.py            # solo, then 2 players
    python roblox/test/run_tests.py solo       # just one of them
    python roblox/test/run_tests.py multi

What it does:
  1. builds build/AFTest_<mode>.rbxl from default.project.json plus a ReplicatedStorage.__AFTest marker
  2. installs roblox/test/AFHarness.plugin.luau into %LOCALAPPDATA%/Roblox/Plugins (it only acts in places
     that have the marker)
  3. opens the place in Roblox Studio (you must be logged in to Studio), where the plugin starts a solo
     or 2-player test, plays the game with real key presses and clicks, and ends the test with a report
  4. reads the report from the Studio log, writes build/test_report_<mode>.json and prints a summary

Needs: Roblox Studio installed and logged in, and `rojo` on PATH (rokit install).
"""

from __future__ import annotations

import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILD = os.path.join(ROOT, "build")
LOCAL = os.environ.get("LOCALAPPDATA", "")
LOG_DIR = os.path.join(LOCAL, "Roblox", "logs")
PLUGIN_SRC = os.path.join(ROOT, "roblox", "test", "AFHarness.plugin.luau")
PLUGIN_DST = os.path.join(LOCAL, "Roblox", "Plugins", "AFHarness.lua")
TIMEOUT = {"solo": 420, "multi": 420}


def find_rojo() -> str:
    found = shutil.which("rojo")
    if found:
        return found
    candidate = os.path.join(os.path.expanduser("~"), ".rokit", "bin", "rojo.exe")
    if os.path.exists(candidate):
        return candidate
    sys.exit("rojo not found: run `rokit install` in the repo (see roblox/GUIA.md)")


def find_studio() -> str:
    exes = glob.glob(os.path.join(LOCAL, "Roblox", "Versions", "*", "RobloxStudioBeta.exe"))
    if not exes:
        sys.exit("Roblox Studio not found (install it from create.roblox.com)")
    return max(exes, key=os.path.getmtime)


def rebase_paths(node: dict) -> None:
    for key, value in list(node.items()):
        if key == "$path":
            node[key] = os.path.join("..", value).replace("\\", "/")
        elif isinstance(value, dict):
            rebase_paths(value)


def build_place(mode: str) -> str:
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(ROOT, "default.project.json"), encoding="utf-8") as f:
        project = json.load(f)
    rebase_paths(project["tree"])
    project["name"] = f"AFTest_{mode}"
    project["tree"]["ReplicatedStorage"]["__AFTest"] = {"$className": "Folder", "$attributes": {"Mode": mode}}
    project_path = os.path.join(BUILD, f"AFTest_{mode}.project.json")
    with open(project_path, "w", encoding="utf-8") as f:
        json.dump(project, f, indent=2)
    place = os.path.join(BUILD, f"AFTest_{mode}.rbxl")
    subprocess.run([find_rojo(), "build", project_path, "-o", place], check=True)
    return place


def install_plugin() -> None:
    os.makedirs(os.path.dirname(PLUGIN_DST), exist_ok=True)
    shutil.copyfile(PLUGIN_SRC, PLUGIN_DST)


def close_test_studios(pid: int) -> None:
    """Close the Studio processes that opened an AFTest place (never the user's other Studio windows)."""
    subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
    script = (
        "Get-CimInstance Win32_Process -Filter \"Name='RobloxStudioBeta.exe'\" | "
        "Where-Object { $_.CommandLine -like '*AFTest_*' } | "
        "ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", script], capture_output=True)


AFH = re.compile(r"\[FLog::(?:Creator)?Output\] \[AFH\] (.*)$")


def run(mode: str) -> dict | None:
    place = build_place(mode)
    install_plugin()
    started = time.time()
    proc = subprocess.Popen([find_studio(), place])
    print(f"[{mode}] Studio opened (pid {proc.pid}), waiting for the test...", flush=True)
    offsets: dict[str, int] = {}
    chunks: dict[int, str] = {}
    total = None
    finished = False
    seen_lines: set[str] = set()
    try:
        while time.time() - started < TIMEOUT[mode] and not finished:
            time.sleep(1.0)
            for path in glob.glob(os.path.join(LOG_DIR, "*Studio*.log")):
                if os.path.getctime(path) < started - 5:
                    continue  # only logs created by this run
                with open(path, encoding="utf-8", errors="replace") as f:
                    f.seek(offsets.get(path, 0))
                    data = f.read()
                    offsets[path] = f.tell()
                for line in data.splitlines():
                    m = AFH.search(line)
                    if not m:
                        continue
                    text = m.group(1)
                    if text in seen_lines:
                        continue  # Studio can open the place in a second process; report each line once
                    seen_lines.add(text)
                    if text.startswith("RESULT_CHUNK"):
                        _, part, body = text.split(" ", 2)
                        i, n = part.split("/")
                        chunks[int(i)] = body
                        total = int(n)
                    else:
                        print(f"  {text[:220]}", flush=True)
                    if text.startswith("FINISHED") or text.startswith("RESULT_ERROR"):
                        finished = True
    finally:
        close_test_studios(proc.pid)
    if total is None or len(chunks) != total:
        print(f"[{mode}] no complete report (timeout or crash)")
        return None
    report = json.loads("".join(chunks[i] for i in range(1, total + 1)))
    out = os.path.join(BUILD, f"test_report_{mode}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"[{mode}] {report['pass']} passed, {report['fail']} failed -> {out}")
    for r in report["results"]:
        if r["status"] == "FAIL":
            print(f"  FAIL {r['name']}: {json.dumps(r.get('detail'), ensure_ascii=False)[:400]}")
    return report


def main() -> None:
    modes = sys.argv[1:] or ["solo", "multi"]
    failed = False
    for mode in modes:
        report = run(mode)
        failed = failed or report is None or report["fail"] > 0
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
