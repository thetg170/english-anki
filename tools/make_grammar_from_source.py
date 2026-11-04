#!/usr/bin/env python3
"""Rebuild an importable grammar deck from the private, readable source.

This cannot guarantee original note/card IDs or restore scheduling. Use the
complete collection backup for exact recovery.
"""
import argparse
import json
from pathlib import Path

import genanki


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    a = parser.parse_args()
    if a.out.exists():
        raise SystemExit(f"Refusing to overwrite {a.out}")
    spec = json.loads((a.source / "notetype.json").read_text())
    deck_info = json.loads((a.source / "deck.json").read_text())
    templates = [{"name": name, "qfmt": data["Front"], "afmt": data["Back"]}
                 for name, data in spec["templates"].items()]
    model = genanki.Model(spec["id"], spec["name"],
                          fields=[{"name": name} for name in spec["fields"]],
                          templates=templates, css=spec["style"]["css"])
    deck = genanki.Deck(deck_info["id"], deck_info["name"])
    for line in (a.source / "notes.jsonl").read_text().splitlines():
        obj = json.loads(line)
        fields = [obj["fields"][name] for name in spec["fields"]]
        deck.add_note(genanki.Note(model=model, fields=fields, guid=obj["guid"], tags=obj["tags"]))
    assert len(deck.notes) == deck_info["note_count"]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(deck).write_to_file(str(a.out))
    print(f"Rebuilt {len(deck.notes)} notes as importable package at {a.out}")


if __name__ == "__main__":
    main()
