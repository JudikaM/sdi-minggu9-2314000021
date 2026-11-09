"""Package source Python dan identitas build; jalankan setelah seluruh test lulus."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent


def main():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    commit = os.getenv("GITHUB_SHA")
    if not commit:
        try:
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT,
                text=True, stderr=subprocess.DEVNULL,
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            commit = "local"
    run = os.getenv("GITHUB_RUN_ID", "local")
    attempt = os.getenv("GITHUB_RUN_ATTEMPT", "local")
    name = f"sdi-m9-{version}-{commit[:12]}-{run}-{attempt}.zip"
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    archive = out / name
    metadata = {
        "version": version, "commit": commit,
        "build_run": run, "run_attempt": attempt,
    }
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(ROOT / "app.py", "app.py")
        z.write(ROOT / "VERSION", "VERSION")
        z.writestr("manifest.json", json.dumps(metadata, indent=2) + "\n")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (out / (name + ".sha256")).write_text(
        f"{digest}  {name}\n", encoding="utf-8"
    )
    print(archive.name)
    print(digest)


if __name__ == "__main__":
    main()
