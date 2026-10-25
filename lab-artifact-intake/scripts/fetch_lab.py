#!/usr/bin/env python3
"""Fetch BlackSwanLabz research-lab artifacts for the needs a person chose, with a manifest.
  python3 fetch_lab.py --needs curriculum,skills,sops,hr,kpi,grant --out <dir> [--clone <local clone>] [--check]
Needs: curriculum skills sops hr kpi grant all.  Always fetched: llms.txt, AGENTS.md, resources/using-with-your-ai.md.
Reads the public repo through the branch-proof URL (HEAD); falls back to a local clone if the network fails.
--check only tests that every mapped path still resolves (use it before trusting this map). Never writes outside --out."""
import sys, os, json, hashlib, argparse, urllib.request, datetime, re
OWNER_REPO = "lordwilsonDev/blackswanlabz-research-lab"
RAW = f"https://raw.githubusercontent.com/{OWNER_REPO}/HEAD/"
ALWAYS = ["llms.txt", "AGENTS.md", "resources/using-with-your-ai.md"]
MAP = {  # keep in sync with references/artifact-map.md
 "curriculum": ["skills/workforce-grant-readiness/SKILL.md", "08-operations/workforce-grant-os-v1.md", "08-operations/optional-trainer-introduction-how-to-ask-ai-v1.md", "08-operations/50-question-os-bootstrap-v1.md", "skills/workforce-grant-readiness-meta/SKILL.md"],
 "skills": ["skills/blackswanlabz-onboarding/SKILL.md", "skills/building-a-business/SKILL.md", "skills/workforce-grant-readiness/SKILL.md", "skills/workforce-grant-readiness-meta/SKILL.md", "resources/README.md"],
 "sops": ["08-operations/master-sop.md", "08-operations/operator-sop.md", "08-operations/day-to-day-operating-manual.md", "08-operations/complete-client-loop.md", "skills/building-a-business/references/functions-and-sops.md"],
 "hr": ["08-operations/black-swan-labs-research-group.md", "skills/building-a-business/references/functions-and-sops.md", "08-operations/day-to-day-operating-manual.md"],
 "kpi": ["skills/building-a-business/references/metrics.md", "skills/building-a-business/references/interview.md", "08-operations/north-star-architecture.md"],
 "grant": ["08-operations/workforce-grant-os-v1.md", "08-operations/workforce-grant-rubric-v1.yaml", "08-operations/workforce-grant-skills-harness-sop-v1.md", "08-operations/workforce-grant-readiness-meta-sop-v1.md", "skills/workforce-grant-readiness/SKILL.md", "scripts/workforce-grant-harness.md", "scripts/workforce_grant_harness.py", "scripts/fixtures/workforce_grant_case.example.json"],
}
def get(path, clone):
    try:
        with urllib.request.urlopen(urllib.request.Request(RAW + path, headers={"User-Agent": "lab-artifact-intake"}), timeout=30) as r: return r.read(), "remote"
    except Exception as e:
        if clone and os.path.exists(os.path.join(clone, path)): return open(os.path.join(clone, path), "rb").read(), "local-clone"
        raise RuntimeError(f"{path}: {getattr(e, 'code', e)}")
def from_history(stub_bytes):
    """An archived stub names the commit and path where the full text lives in the repo's own public history. Return (bytes, commit) or (None, None)."""
    t = stub_bytes.decode("utf-8", "replace"); m = re.search(r"commit\s+`([0-9a-f]{7,40})`\s*\(path\s+`([^`]+)`\)", t)
    if not m: return None, None
    try:
        with urllib.request.urlopen(urllib.request.Request(f"https://raw.githubusercontent.com/{OWNER_REPO}/{m.group(1)}/{m.group(2)}", headers={"User-Agent": "lab-artifact-intake"}), timeout=30) as r: return r.read(), m.group(1)
    except Exception: return None, None
def banner(b):
    t = b.decode("utf-8", "replace")[:1500]; m = re.search(r"^status:\s*(.+)$", t, re.M); return m.group(1).strip() if m else ""
ap = argparse.ArgumentParser(); ap.add_argument("--needs", default="all"); ap.add_argument("--out", required=False); ap.add_argument("--clone"); ap.add_argument("--check", action="store_true"); a = ap.parse_args()
needs = list(MAP) if a.needs == "all" else [n.strip() for n in a.needs.split(",") if n.strip()]
bad = [n for n in needs if n not in MAP]
if bad: sys.exit(f"unknown need(s): {bad}; choose from {list(MAP)} or all")
paths = list(dict.fromkeys(ALWAYS + [p for n in needs for p in MAP[n]])); man = []; fails = []
for p in paths:
    try:
        b, via = get(p, a.clone)
    except RuntimeError as e:
        fails.append(str(e)); print("FAIL", e); continue
    stub = None; note = ""
    if banner(b).lower().startswith("archived"):
        full, commit = from_history(b)
        if full: stub, b, via, note = b, full, f"git-history@{commit}", "archived page: full text recovered from the lab's own git history"
        else: note = "STUB: archived page; the full text is private or could not be recovered. Do not treat the stub as the document"
    man.append({"path": p, "note": note, "url": RAW + p, "via": via, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "status_banner": banner(b), "needs": [n for n in needs if p in MAP[n]]})
    if not a.check:
        dst = os.path.join(a.out, "lab", p); os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, "wb").write(b)
        if stub: open(dst + ".stub.md", "wb").write(stub)
    print("ok  ", via, f"{len(b):>8}", p, ("[" + man[-1]["status_banner"] + "]") if man[-1]["status_banner"] else "", ("<-- " + note) if note else "")
if not a.check:
    json.dump({"retrieved": datetime.datetime.now().isoformat(timespec="seconds"), "repo": OWNER_REPO, "needs": needs, "files": man, "failed": fails}, open(os.path.join(a.out, "MANIFEST.json"), "w"), indent=1)
    print(f"\nwrote {len(man)} files + MANIFEST.json to {a.out}")
sys.exit(1 if fails else 0)
