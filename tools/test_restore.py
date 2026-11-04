#!/usr/bin/env python3
"""Open a staged collection and import packages into an isolated new collection."""
import argparse
import json
from pathlib import Path

from anki.collection import Collection
from anki.importing import AnkiPackageImporter
from anki.lang import set_lang

from anki_repo import connect, counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backup", type=Path, required=True)
    parser.add_argument("--staged", type=Path, required=True, help="Existing staged profile directory, never the live profile")
    parser.add_argument("--grammar-apkg", type=Path, required=True)
    parser.add_argument("--pilot-apkg", type=Path, required=True)
    parser.add_argument("--import-test", type=Path, required=True, help="New, empty collection path")
    a = parser.parse_args()
    if a.import_test.exists():
        raise SystemExit("Refusing to overwrite an import test collection")
    expected = counts(connect(a.backup / "collection.anki2"))
    set_lang("en_US")
    staged_path = a.staged / "User 1" / "collection.anki2"
    staged = Collection(str(staged_path))
    observed = {"notes": staged.note_count(), "cards": staged.card_count(),
                "revlog": staged.db.scalar("select count(*) from revlog"),
                "grammar": len(staged.find_notes('deck:"English Grammar"'))}
    staged.close()
    assert all(observed[k] == expected[k] for k in ("notes", "cards", "revlog"))
    assert observed["grammar"] == 581
    a.import_test.parent.mkdir(parents=True, exist_ok=True)
    target = Collection(str(a.import_test))
    for package in (a.grammar_apkg, a.pilot_apkg):
        AnkiPackageImporter(target, str(package)).run()
    grammar_count = len(target.find_notes('deck:"English Grammar"'))
    pilot_ids = target.find_cards('deck:"English Speaking Pilot"')
    assert grammar_count == 581 and len(pilot_ids) == 17
    assert target.db.scalar("select count(*) from revlog") == 0
    assert target.models.by_name("EN_Speaking_Pilot_v1")
    for card_id in pilot_ids:
        card = target.get_card(card_id)
        assert "{{" not in card.question() and "{{" not in card.answer()
    target.close()
    print(json.dumps({"restored_collection": observed, "imported_grammar": grammar_count,
                      "imported_pilot": len(pilot_ids), "imported_review_history": 0,
                      "pilot_templates_rendered": len(pilot_ids)}, indent=2))


if __name__ == "__main__":
    main()
