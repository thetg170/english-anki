#!/usr/bin/env python3
"""Open a staged collection and import packages into an isolated new collection."""
import argparse
import json
from pathlib import Path

from anki._backend import RustBackend
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
    parser.add_argument("--colpkg", type=Path, help="Optional full collection package to import into a separate test profile")
    parser.add_argument("--colpkg-test", type=Path, help="New profile directory for the collection package test")
    a = parser.parse_args()
    if bool(a.colpkg) != bool(a.colpkg_test):
        raise SystemExit("Supply both --colpkg and --colpkg-test")
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
    result = {"restored_collection": observed, "imported_grammar": grammar_count,
                      "imported_pilot": len(pilot_ids), "imported_review_history": 0,
                      "pilot_templates_rendered": len(pilot_ids)}
    if a.colpkg:
        if a.colpkg_test.exists() and any(a.colpkg_test.iterdir()):
            raise SystemExit("Refusing to overwrite collection package test profile")
        a.colpkg_test.mkdir(parents=True, exist_ok=True)
        backend = RustBackend(langs=["en_US"])
        col_path = a.colpkg_test / "collection.anki2"
        media = a.colpkg_test / "collection.media"
        backend.import_collection_package(col_path=str(col_path), backup_path=str(a.colpkg),
                                          media_folder=str(media), media_db=str(a.colpkg_test / "collection.media.db2"))
        restored = Collection(str(col_path))
        package_counts = {"notes": restored.note_count(), "cards": restored.card_count(),
                          "revlog": restored.db.scalar("select count(*) from revlog"),
                          "grammar": len(restored.find_notes('deck:"English Grammar"')),
                          "media_files": sum(x.is_file() for x in media.iterdir())}
        restored.close()
        assert all(package_counts[k] == expected[k] for k in ("notes", "cards", "revlog"))
        assert package_counts["grammar"] == 581
        result["collection_package_import"] = package_counts
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
