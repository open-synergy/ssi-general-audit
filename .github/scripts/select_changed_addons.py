#!/usr/bin/env python3
"""Pilih addon yang perlu dites dari berkas yang berubah di sebuah PR.

Dipakai langkah "Select addons to test" di `.github/workflows/test.yml`.
Hasilnya ditulis ke `$GITHUB_ENV`:

* `INCLUDE=a,b,c`  -> `oca_init_test_database` dan `oca_run_tests` hanya
  memasang dan menguji addon itu (variabel bawaan image OCA CI).
* `TEST_SKIP=true` -> tak ada addon yang perlu dites (hanya berkas lint/doc).
* tanpa keduanya  -> tes penuh, semua addon di repo.

Addon yang dites = addon yang berubah + semua addon di repo ini yang bergantung
padanya (langsung atau tidak langsung, lewat `depends` di manifest). Bila ada
berkas berubah di luar addon dan di luar daftar abaikan, diputuskan tes penuh.

Kompatibel Python 3.6 (image OCA CI py3.6). Hanya pustaka standar.
"""

import ast
import os
import subprocess
import sys

# Berkas yang tak memengaruhi hasil tes addon.
IGNORED_FILES = {
    "README.md",
    "LICENSE",
    ".gitignore",
    ".editorconfig",
    ".flake8",
    ".isort.cfg",
    ".eslintrc.yml",
    ".prettierrc.yml",
    ".pylintrc",
    ".pylintrc-mandatory",
    ".pre-commit-config.yaml",
    ".copier-answers.yml",
    ".github/workflows/pre-commit.yml",
    ".github/workflows/docstring-gate.yml",
    ".github/workflows/notify-telegram.yml",
    ".github/scripts/docstring_check.py",
}
IGNORED_PREFIXES = (".claude/",)


def read_depends(addon_dir):
    """Kembalikan daftar `depends` dari manifest sebuah addon."""
    with open(os.path.join(addon_dir, "__manifest__.py")) as handle:
        manifest = ast.literal_eval(handle.read())
    return list(manifest.get("depends", []))


def list_addons():
    """Petakan nama addon di repo -> daftar depends-nya."""
    result = {}
    for name in sorted(os.listdir(".")):
        if os.path.isfile(os.path.join(name, "__manifest__.py")):
            result[name] = read_depends(name)
    return result


def changed_files(base):
    """Daftar berkas yang berubah sejak merge-base dengan `base`."""
    out = subprocess.check_output(
        ["git", "diff", "--name-only", "{}...HEAD".format(base)],
        universal_newlines=True,
    )
    return [line for line in out.splitlines() if line]


def addon_of(path, addons):
    """Nama addon pemilik `path`, atau None bila bukan milik addon."""
    parts = path.split("/")
    if parts[0] in addons:
        return parts[0]
    if parts[0] == "setup" and len(parts) > 1 and parts[1] in addons:
        return parts[1]
    return None


def is_ignored(path):
    """Benar bila `path` tak memengaruhi tes addon mana pun."""
    return path in IGNORED_FILES or path.startswith(IGNORED_PREFIXES)


def reverse_closure(changed, addons):
    """Addon yang berubah ditambah semua addon yang bergantung padanya."""
    dependents = {}
    for name, depends in addons.items():
        for dep in depends:
            dependents.setdefault(dep, set()).add(name)
    selected = set(changed)
    queue = list(changed)
    while queue:
        current = queue.pop()
        for name in dependents.get(current, ()):
            if name not in selected:
                selected.add(name)
                queue.append(name)
    return selected


def decide(files, addons):
    """Putuskan mode: ("full", alasan), ("none", ...) atau ("selected", set)."""
    changed = set()
    for path in files:
        if is_ignored(path):
            continue
        owner = addon_of(path, addons)
        if owner is None:
            return "full", "berkas di luar addon: {}".format(path)
        changed.add(owner)
    if not changed:
        return "none", "hanya berkas yang diabaikan"
    return "selected", reverse_closure(changed, addons)


def export(lines):
    """Tulis pasangan KEY=VALUE ke $GITHUB_ENV (atau cetak bila lokal)."""
    target = os.environ.get("GITHUB_ENV")
    if not target:
        for line in lines:
            print("ENV " + line)
        return
    with open(target, "a") as handle:
        for line in lines:
            handle.write(line + "\n")


def summary(text):
    """Tulis ke ringkasan job GitHub Actions, selain ke log."""
    print(text)
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with open(target, "a") as handle:
            handle.write(text + "\n")


def main(argv):
    """Titik masuk: `select_changed_addons.py [--base REF]`."""
    base = ""
    if len(argv) >= 3 and argv[1] == "--base":
        base = argv[2]
    addons = list_addons()
    if not base:
        summary("Select addons: tes penuh ({} addon), tanpa basis "
                "pembanding.".format(len(addons)))
        return 0
    try:
        files = changed_files(base)
    except (subprocess.CalledProcessError, OSError) as error:
        summary("Select addons: tes penuh, gagal membaca diff ({}).".format(
            error))
        return 0
    mode, detail = decide(files, addons)
    if mode == "full":
        summary("Select addons: tes penuh, {}.".format(detail))
    elif mode == "none":
        export(["TEST_SKIP=true"])
        summary("Select addons: tidak ada addon dites, {}.".format(detail))
    else:
        names = sorted(detail)
        export(["INCLUDE=" + ",".join(names)])
        summary("Select addons: {} dari {} addon dites:\n{}".format(
            len(names), len(addons), "\n".join("- " + n for n in names)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
