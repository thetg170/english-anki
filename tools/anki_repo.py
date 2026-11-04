#!/usr/bin/env python3
"""Read-only Anki snapshot, backup verification, and local source extraction.

Never opens a live collection for writing. The only AnkiConnect calls are read-only
model metadata requests; collection backup uses SQLite's online backup API.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import sqlite3
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path


def connect(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    db.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold()) - (a.casefold() < b.casefold()))
    return db


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def counts(db: sqlite3.Connection) -> dict:
    return {table: db.execute(f"select count(*) from {table}").fetchone()[0]
            for table in ("notes", "cards", "revlog", "decks", "notetypes")}


def media_references(db: sqlite3.Connection) -> set[str]:
    result = set()
    for (fields,) in db.execute("select flds from notes"):
        result.update(re.findall(r"\[sound:([^\]]+)\]", fields))
        result.update(html.unescape(x) for x in re.findall(r'<(?:img|audio|video|source)\b[^>]*?\bsrc=["\']([^"\']+)', fields, re.I))
    return {x for x in result if not x.startswith(("http:", "https:", "data:"))}


def build_manifest(folder: Path) -> dict:
    db = connect(folder / "collection.anki2")
    ok = db.execute("pragma integrity_check").fetchone()[0]
    refs = media_references(db)
    result = {"format": 1, "collection_sha256": sha256(folder / "collection.anki2"),
              "collection_integrity": ok, "counts": counts(db),
              "media_file_count": 0, "media_bytes": 0, "media_sha256": {},
              "referenced_media_count": len(refs), "missing_referenced_media": []}
    db.close()
    media = folder / "collection.media"
    for file in sorted(media.rglob("*")):
        if file.is_file():
            rel = file.relative_to(media).as_posix()
            result["media_sha256"][rel] = sha256(file)
            result["media_file_count"] += 1
            result["media_bytes"] += file.stat().st_size
    result["missing_referenced_media"] = sorted(x for x in refs if not (media / x).is_file())
    return result


def backup(profile: Path, out: Path) -> None:
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Refusing to overwrite populated backup: {out}")
    out.mkdir(parents=True, exist_ok=True)
    source = connect(profile / "collection.anki2")
    target = sqlite3.connect(out / "collection.anki2")
    target.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold()) - (a.casefold() < b.casefold()))
    source.backup(target)
    target.close()
    source.close()
    shutil.copytree(profile / "collection.media", out / "collection.media", dirs_exist_ok=True)
    manifest = build_manifest(out)
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in manifest.items() if k != "media_sha256"}, ensure_ascii=False, indent=2))
    if manifest["collection_integrity"] != "ok":
        raise SystemExit("Backup collection failed integrity check")
    if manifest["missing_referenced_media"]:
        print("WARNING: source collection already references missing media")


def verify(folder: Path) -> None:
    expected = json.loads((folder / "manifest.json").read_text())
    actual = build_manifest(folder)
    if expected != actual:
        raise SystemExit("Backup manifest mismatch; inspect hashes, counts and media")
    if actual["collection_integrity"] != "ok":
        raise SystemExit("Backup collection failed integrity check")
    print(f"Verified collection, {actual['counts']}, {actual['media_file_count']} media files; "
          f"{len(actual['missing_referenced_media'])} source references lack media")


def stage_restore(folder: Path, out: Path) -> None:
    verify(folder)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Refusing to overwrite populated restore target: {out}")
    profile = out / "User 1"
    profile.mkdir(parents=True, exist_ok=True)
    shutil.copy2(folder / "collection.anki2", profile / "collection.anki2")
    shutil.copytree(folder / "collection.media", profile / "collection.media")
    assert sha256(profile / "collection.anki2") == sha256(folder / "collection.anki2")
    print(f"Staged isolated Anki profile at {out}; do not point a running primary profile here")


def anki_connect(action: str, params: dict) -> object:
    req = urllib.request.Request("http://127.0.0.1:8765",
        json.dumps({"action": action, "version": 6, "params": params}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.load(response)
    if data["error"]:
        raise RuntimeError(data["error"])
    return data["result"]


def export_source(folder: Path, deck: str, out: Path) -> None:
    db = connect(folder / "collection.anki2")
    row = db.execute("select id from decks where name=?", (deck.replace("::", "\x1f"),)).fetchone()
    if not row:
        raise SystemExit(f"Deck not found exactly: {deck}")
    did = row[0]
    mids = [x[0] for x in db.execute("select distinct n.mid from notes n join cards c on c.nid=n.id where c.did=?", (did,))]
    if len(mids) != 1:
        raise SystemExit(f"Expected one note type, found {mids}")
    mid = mids[0]
    model = db.execute("select name from notetypes where id=?", (mid,)).fetchone()[0]
    field_names = [x[0] for x in db.execute("select name from fields where ntid=? order by ord", (mid,))]
    template = anki_connect("modelTemplates", {"modelName": model})
    style = anki_connect("modelStyling", {"modelName": model})
    out.mkdir(parents=True, exist_ok=True)
    (out / "notetype.json").write_text(json.dumps({"id": mid, "name": model, "fields": field_names,
        "templates": template, "style": style}, ensure_ascii=False, indent=2) + "\n")
    with (out / "notes.jsonl").open("w") as fh:
        for nid, guid, tags, flds in db.execute("select n.id,n.guid,n.tags,n.flds from notes n join cards c on c.nid=n.id where c.did=? order by n.id", (did,)):
            obj = {"id": nid, "guid": guid, "tags": tags.split(), "fields": dict(zip(field_names, flds.split("\x1f")))}
            fh.write(json.dumps(obj, ensure_ascii=False) + "\n")
    (out / "deck.json").write_text(json.dumps({"id": did, "name": deck, "note_type_id": mid,
        "note_count": db.execute("select count(distinct nid) from cards where did=?", (did,)).fetchone()[0]},
        ensure_ascii=False, indent=2) + "\n")
    db.close()
    validate_source(out, folder / "collection.media")


def export_package(deck: str, out: Path) -> None:
    if out.exists():
        raise SystemExit(f"Refusing to overwrite package: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)
    result = anki_connect("exportPackage", {"deck": deck, "path": str(out), "includeSched": False})
    if result is not True or not out.is_file():
        raise SystemExit("AnkiConnect package export failed")
    print(f"Exported importable deck package: {out} (without scheduling)")


def validate_source(source: Path, media: Path | None) -> None:
    spec = json.loads((source / "notetype.json").read_text())
    fields = spec["fields"]
    ids, guids, keys = set(), set(), set()
    missing = set()
    notes = 0
    for line in (source / "notes.jsonl").read_text().splitlines():
        obj = json.loads(line)
        assert set(obj["fields"]) == set(fields), f"Field mismatch on {obj['id']}"
        assert obj["id"] not in ids and obj["guid"] not in guids, "Duplicate ID/GUID"
        ids.add(obj["id"]); guids.add(obj["guid"]); notes += 1
        key = obj["fields"].get("Key")
        if key:
            assert key not in keys, f"Duplicate key: {key}"
            keys.add(key)
        if media:
            for value in obj["fields"].values():
                for filename in re.findall(r"\[sound:([^\]]+)\]", value):
                    if not (media / filename).is_file():
                        missing.add(filename)
    assert not missing, f"Missing media: {sorted(missing)[:10]}"
    for template in spec["templates"].values():
        for side in ("Front", "Back"):
            used = re.findall(r"{{(?:[#/^]|type:|tts[^:}]*:)?([^}]+)}}", template[side])
            unknown = {x for x in used if x not in fields and x not in ("FrontSide", "Tags", "Deck", "Subdeck", "Card", "Type")}
            assert not unknown, f"Unknown template fields: {unknown}"
    print(f"Validated {notes} notes, {len(spec['templates'])} templates, no missing referenced audio")


def audit(folder: Path) -> None:
    db = connect(folder / "collection.anki2")
    decks = {i: name.replace("\x1f", "::") for i, name in db.execute("select id,name from decks")}
    models = dict(db.execute("select id,name from notetypes"))
    rows = db.execute("select c.did,n.mid,n.id,c.id,c.type,c.queue,c.reps,c.lapses from cards c join notes n on n.id=c.nid").fetchall()
    groups = defaultdict(list)
    for row in rows:
        groups[decks[row[0]].split("::")[0]].append(row)
    print("TOTAL", json.dumps(counts(db), ensure_ascii=False))
    for group, cards in sorted(groups.items()):
        print(json.dumps({"deck_group": group, "notes": len({r[2] for r in cards}), "cards": len(cards),
            "models": dict(Counter(models[r[1]] for r in cards)),
            "queues": dict(Counter(r[5] for r in cards)),
            "review_actions": db.execute("select count(*) from revlog where cid in (%s)" % ",".join("?" * len(cards)), [r[3] for r in cards]).fetchone()[0]}, ensure_ascii=False))
    db.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("backup"); p.add_argument("--profile", type=Path, required=True); p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("verify"); p.add_argument("--backup", type=Path, required=True)
    p = sub.add_parser("stage-restore"); p.add_argument("--backup", type=Path, required=True); p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("export-source"); p.add_argument("--backup", type=Path, required=True); p.add_argument("--deck", required=True); p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("export-package"); p.add_argument("--deck", required=True); p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("validate-source"); p.add_argument("--source", type=Path, required=True); p.add_argument("--media", type=Path)
    p = sub.add_parser("audit"); p.add_argument("--backup", type=Path, required=True)
    a = parser.parse_args()
    if a.command == "backup": backup(a.profile, a.out)
    elif a.command == "verify": verify(a.backup)
    elif a.command == "stage-restore": stage_restore(a.backup, a.out)
    elif a.command == "export-source": export_source(a.backup, a.deck, a.out)
    elif a.command == "export-package": export_package(a.deck, a.out)
    elif a.command == "validate-source": validate_source(a.source, a.media)
    elif a.command == "audit": audit(a.backup)


if __name__ == "__main__": main()
