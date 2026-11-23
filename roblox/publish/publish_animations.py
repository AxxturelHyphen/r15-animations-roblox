"""Publish the 27 clips to Roblox in one go and fill in roblox/src/shared/AnimationIds.luau.

Uses the Open Cloud Assets API (https://create.roblox.com/docs/cloud/guides/usage-assets), so you need an
API key from your own account (one-time, about 2 minutes, see roblox/GUIA.md section 7.1):
  create.roblox.com -> Open Cloud -> API Keys -> Create API Key
  Access permissions: "Assets" API, operations Read and Write. Accepted IP addresses: 0.0.0.0/0 (or yours).

    $env:ROBLOX_API_KEY = "<the key>"                                 # PowerShell
    python roblox/publish/publish_animations.py --user-id 123456789   # your user ID (number in your profile URL)
    python roblox/publish/publish_animations.py --group-id 987654     # or a group, if the game belongs to one

Options: --dry-run (convert and show what would be uploaded), --only wave,dance (a subset).
Clips that already have a non-zero ID in AnimationIds.luau are skipped, so it can be re-run after an error.
The animations must belong to the same owner as the game (user or group), or they won't play in it.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IDS_FILE = os.path.join(ROOT, "roblox", "src", "shared", "AnimationIds.luau")
RBXM_DIR = os.path.join(ROOT, "build", "rbxm")
API = "https://apis.roblox.com/assets/v1"
ENTRY = re.compile(r"^(\t)([a-z_]+)( = )(\d+)(,.*)$", re.M)


def find_lune() -> str:
    found = shutil.which("lune") or os.path.join(os.path.expanduser("~"), ".rokit", "bin", "lune.exe")
    if not os.path.exists(found) and not shutil.which("lune"):
        sys.exit("lune not found: run `rokit install` in the repo (see roblox/GUIA.md)")
    return found


def read_ids() -> dict[str, int]:
    with open(IDS_FILE, encoding="utf-8") as f:
        return {m.group(2): int(m.group(4)) for m in ENTRY.finditer(f.read())}


def write_id(clip: str, asset_id: int) -> None:
    with open(IDS_FILE, encoding="utf-8") as f:
        text = f.read()
    text, n = re.subn(rf"^(\t{clip} = )\d+(,.*)$", rf"\g<1>{asset_id}\g<2>", text, flags=re.M)
    if n != 1:
        raise RuntimeError(f"{clip}: entry not found in AnimationIds.luau")
    with open(IDS_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def request(method: str, url: str, key: str, body: bytes | None = None, content_type: str | None = None) -> dict:
    headers = {"x-api-key": key}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"HTTP {e.code}: {detail}") from None


def upload(clip: str, path: str, creator: dict, key: str) -> int:
    meta = {
        "assetType": "Animation",
        "displayName": f"AnimationForge {clip}",
        "description": f"R15 '{clip}' clip from the R15 Animation Forge pack.",
        "creationContext": {"creator": creator},
    }
    boundary = uuid.uuid4().hex
    with open(path, "rb") as f:
        content = f.read()
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"request\"\r\n\r\n{json.dumps(meta)}\r\n"
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"fileContent\"; filename=\"{clip}.rbxm\"\r\n"
        f"Content-Type: model/x-rbxm\r\n\r\n"
    ).encode() + content + f"\r\n--{boundary}--\r\n".encode()
    op = request("POST", f"{API}/assets", key, body, f"multipart/form-data; boundary={boundary}")
    op_id = op.get("operationId") or op.get("path", "").split("/")[-1]
    for _ in range(60):
        if op.get("done"):
            break
        time.sleep(1.5)
        op = request("GET", f"{API}/operations/{op_id}", key)
    if not op.get("done"):
        raise RuntimeError("upload still processing after 90 s; re-run later (finished clips are kept)")
    if "error" in op:
        raise RuntimeError(json.dumps(op["error"]))
    return int(op["response"]["assetId"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    owner = parser.add_mutually_exclusive_group(required=True)
    owner.add_argument("--user-id", type=int)
    owner.add_argument("--group-id", type=int)
    parser.add_argument("--only", help="comma-separated clip names")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    key = os.environ.get("ROBLOX_API_KEY", "")
    if not key and not args.dry_run:
        sys.exit("Set ROBLOX_API_KEY first (see the top of this file or roblox/GUIA.md section 7.1)")
    creator = {"userId": str(args.user_id)} if args.user_id else {"groupId": str(args.group_id)}

    subprocess.run([find_lune(), "run", "roblox/publish/to_rbxm.luau", RBXM_DIR], cwd=ROOT, check=True)
    ids = read_ids()
    wanted = args.only.split(",") if args.only else sorted(ids)
    todo = [c for c in wanted if ids.get(c, 0) == 0]
    print(f"{len(ids)} clips in AnimationIds.luau, {len(todo)} to publish as {creator}")
    failures = []
    for clip in todo:
        path = os.path.join(RBXM_DIR, f"{clip}.rbxm")
        if not os.path.exists(path):
            failures.append((clip, "no .rbxm (missing from output/rbxmx)"))
            continue
        if args.dry_run:
            print(f"  would upload {clip} ({os.path.getsize(path)} bytes)")
            continue
        try:
            asset_id = upload(clip, path, creator, key)
        except RuntimeError as e:
            failures.append((clip, str(e)))
            print(f"  {clip}: FAILED {e}")
            continue
        write_id(clip, asset_id)
        print(f"  {clip}: {asset_id}")
    if failures:
        print(f"{len(failures)} failed; fix the cause and re-run (published clips are skipped):")
        for clip, why in failures:
            print(f"  {clip}: {why}")
        sys.exit(1)
    if not args.dry_run:
        print("Done. AnimationIds.luau is filled in; rebuild (rojo build) or let `rojo serve` sync it.")


if __name__ == "__main__":
    main()
