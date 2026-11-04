# English Anki

This repository stores a **local, restorable snapshot** of the English learning system and a small speaking pilot. The collection inspected on **2026-11-04 (Asia/Ho_Chi_Minh)** contains a deck named **`English Grammar`**. The requested spelling `English Gramar` was not present; no deck was renamed.

## What is where

| Asset | Location | Purpose | Git |
|---|---|---|---|
| Complete collection and media | `private/backups/2026-11-04-baseline/` | Exact recovery, including IDs and review history | Ignored |
| Full collection package | `private/backups/2026-11-04-baseline/full-collection-with-media.colpkg` | Anki's native whole-collection recovery format | Ignored |
| Original grammar source | `source/english-grammar/` | Readable note type, templates, CSS, raw HTML fields, note IDs and GUIDs | Tracked; review before any public push |
| Original grammar `.apkg` | `private/imports/English Grammar-pristine.apkg` | Import deck into another profile, **without** scheduling | Ignored |
| Pilot source | `source/pilot/pilot.json` | Editable, diffable authored cards | Tracked |
| Pilot `.apkg` | `private/imports/English Speaking Pilot.apkg` | Import the pilot into a separate profile first | Ignored |
| Audit and design | `reports/`, `docs/` | Evidence, decisions, learning workflow | Tracked |

An `.apkg` can include scheduling if exported that way, but the package here intentionally does not. The complete backup and `.colpkg` are the recovery route for review history. [Anki's export manual](https://docs.ankiweb.net/exporting.html) describes the different package modes; [its backup manual](https://docs.ankiweb.net/backups.html) notes that automatic backups omit media.

**Keep `private/` in an encrypted personal backup outside this machine.** It is ignored to avoid accidentally publishing collection history, personal content, third-party decks, and media. A Git clone can rebuild the grammar deck's content and template from `source/english-grammar/`, but cannot recover original scheduling or the full collection. The grammar source was screened for common email, URL, phone, and API-key patterns, but needs human content and licensing review before any public push. No remote is configured here.

## Setup

The tested environment is Anki 26.5, AnkiConnect API 6, Python 3.13, macOS. The scripts use the standard library except for `anki` (isolated restore/import checks) and `genanki` (pilot package).

```sh
cd ~/Developer/Personal/english-anki
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

## Back up and verify

For a new dated backup, choose an **empty** output directory. The script uses SQLite's online backup API, copies media, records SHA-256 for every file, checks database integrity, and records missing source media. It never writes to the live collection. If Anki is actively adding media during the copy, repeat after closing Anki. A known missing image in `Hackers Speaking Phrases::U09` is documented in the audit.

```sh
.venv/bin/python tools/anki_repo.py backup \
  --profile "$HOME/Library/Application Support/Anki2/User 1" \
  --out private/backups/YYYY-MM-DD-HHMM
.venv/bin/python tools/anki_repo.py verify \
  --backup private/backups/2026-11-04-baseline
```

The present backup's manifest has 3,792 notes, 5,497 cards, 1,590 review log rows, 12,264 media files (468,073,502 bytes), and database integrity `ok`. The source collection already had one missing referenced image; this is a source-data issue, not a copy mismatch. The copied media was also compared with the live media using `rsync -anrc`, with no differences at the time of audit.
The `.colpkg` has a separate SHA-256 sidecar and passed ZIP CRC verification. It was imported into an isolated Anki 26.5 profile with 3,792 notes, 5,497 cards, 1,590 review rows, and 12,264 media files. The staged database restore was also opened and checked separately.

## Export and validate the original deck

`export-source` reads a **snapshot** for note content and uses AnkiConnect only to read the current model templates/CSS. It preserves raw HTML field values, note IDs, and GUIDs in local JSONL. This source is for inspection and controlled reconstruction; the complete backup is the exact recovery mechanism.

```sh
.venv/bin/python tools/anki_repo.py export-source \
  --backup private/backups/2026-11-04-baseline \
  --deck 'English Grammar' --out source/english-grammar
.venv/bin/python tools/anki_repo.py validate-source \
  --source source/english-grammar \
  --media private/backups/2026-11-04-baseline/collection.media
.venv/bin/python tools/anki_repo.py export-package \
  --deck 'English Grammar' \
  --out 'private/imports/English Grammar-new-export.apkg'
.venv/bin/python tools/make_grammar_from_source.py \
  --source source/english-grammar \
  --out 'private/imports/English Grammar-rebuilt-from-source.apkg'
```

`export-package` requires AnkiConnect and refuses to overwrite a package. It exports **without scheduling**. It reads the live deck, so export again after any intentional changes.
The rebuilt package uses the saved note type, fields, templates, CSS, deck ID and GUIDs. Import can assign different note/card IDs, so it is **not** an exact replacement for the full collection backup.

## Restore safely

First verify the complete backup. Stage it under a **new path**. Opening the staged copy does not touch the daily profile. The test script opens the staged collection with Anki 26.5, then imports grammar and pilot packages into another new collection and renders all pilot cards.

```sh
.venv/bin/python tools/anki_repo.py stage-restore \
  --backup private/backups/2026-11-04-baseline \
  --out private/restore-test-new
.venv/bin/python tools/test_restore.py \
  --backup private/backups/2026-11-04-baseline \
  --staged private/restore-test-new \
  --grammar-apkg 'private/imports/English Grammar-pristine.apkg' \
  --pilot-apkg 'private/imports/English Speaking Pilot.apkg' \
  --import-test private/import-test-new/collection.anki2 \
  --colpkg private/backups/2026-11-04-baseline/full-collection-with-media.colpkg \
  --colpkg-test private/colpkg-import-test-new
```

For actual loss, close Anki, make a separate copy of whatever remains in the active profile, and restore the full collection using Anki's File > Import for the `.colpkg` with media. **That replaces the active collection.** Alternatively, use Anki's profile manager to open the staged profile as a separate profile and inspect it before replacing anything. Do not import the `.apkg` as a substitute for a history-preserving backup. The tested staged copy retained all 1,590 review log rows; the grammar `.apkg` imported 581 notes and zero review rows in a fresh collection.

## Pilot and learning use

```sh
.venv/bin/python tools/make_pilot.py \
  --out 'private/imports/English Speaking Pilot-new.apkg'
```

The pilot has **17 cards** in three modes: Transform (6), Situation (6), Repair (5). It has one card per note and no JavaScript or media dependencies. Its model answer is an example, not an exact-match key. Say the answer aloud before revealing it; then produce a different valid version or apply the transfer prompt. The package has only been imported into isolated test collections, **not** the main collection.

See [audit](reports/audit-2026-11-04.md), [grammar design](docs/grammar-design.md), [learning architecture](docs/learning-system.md), and [pilot guide](docs/pilot.md).

## Repeatable checks

```sh
.venv/bin/python tools/anki_repo.py audit --backup private/backups/2026-11-04-baseline
.venv/bin/python tools/anki_repo.py verify --backup private/backups/2026-11-04-baseline
.venv/bin/python tools/anki_repo.py validate-source --source source/english-grammar \
  --media private/backups/2026-11-04-baseline/collection.media
```

The scripts refuse to overwrite populated backup, restore, import-test, and package output paths. They do not delete or change any live deck, note, template, or scheduling data.
