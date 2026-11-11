# English Anki

**Business Analysis (11/11/2026):** Đã nhập 108 thẻ IT BA theo 13 chủ đề vào Anki, tập trung vào khái niệm, áp dụng, tình huống và review requirements. Xem [curriculum và nguồn](docs/business-analysis.md) cùng [CSV nguồn](source/business-analysis/notes.csv). Một deck duy nhất, phân loại bằng tags; không có audio. Mặt thẻ chỉ hiện đáp án chính, phần định nghĩa/giải thích thêm có thể mở khi cần; nguồn chỉ lưu trong CSV.

**Học từ bài giải thích đến phản xạ:** Mở [mục lục 24 bài học](docs/README.md), đọc bài đúng chủ đề, tự tạo và nói vài câu, rồi mới ôn nhóm card được liên kết ở cuối bài. Quy trình: **Read Lesson → Understand Grammar → Practice Building Sentences → Review with Anki → Speak Aloud → Apply in AI Conversation**. Các bài Markdown chỉ giải thích và tham chiếu CSV; không thay đổi note, deck hay tiến trình học.

[Báo cáo rà soát nội dung ngữ pháp](docs/GRAMMAR_AUDIT.md) tóm tắt phần kiến thức bổ sung và các chủ đề có thể mở rộng sau này.

**Current Anki state (2026-11-09):** `English Grammar` (581 cards), `DE Knowledge` (322), `Everyday English` (95, including three suspended guided drills), and `English Essentials – Daily Reflex` (135) are in the live collection. Anki also retains an empty `Default` deck. The removed decks are recoverable from `private/backups/2026-11-04-pre-cleanup-v2/`; the snapshot immediately before expanding PDF day 1 is at `private/backups/2026-11-09-before-day01-expansion/`. See the [cleanup report](reports/cleanup-2026-11-04.md). The older Speaking Pilot remains source/package only.

**English Grammar prompt clarity (2026-11-09):** 65 existing notes were clarified in [the CSV](source/english-grammar/notes.csv) and synced to Anki. Ambiguous tense prompts now provide time or intent context; broad rule prompts specify the answer format. Several answers acknowledge valid alternatives. The pre-edit collection and media backup is at `private/backups/2026-11-09-grammar-prompt-clarity/`. A repeat diff reports 581 SKIP; card scheduling and review history were unchanged.

**New English trial:** [Everyday English](docs/everyday-english.md) has 72 original short sentence cards in [CSV](source/everyday-english/notes.csv), grouped into nine visible topic subdecks with eight cards each. Its dedicated `Everyday English - No Daily Cap` preset sets new and review limits to 9,999/day so the learner can choose the pace. The two existing deck presets were not changed. Twenty PDF day 1 sentence cards and three suspended guided drills were subsequently added to the same deck.

**Daily reflex:** `English Essentials – Daily Reflex` has 135 [CSV cards](source/daily-reflex/notes.csv) in one deck, grouped by nine `topic::*` tags. Look at the prompt, **say the answer aloud before flipping**, then check the preferred American reading and any alternate or British usage note. Its note type uses Anki's `en_US` text-to-speech on the answer; no audio files or Markdown lessons are needed. To check future edits, run `validate` and `diff` with `source/daily-reflex/notes.csv`, then `sync --apply --backup-dir` using the same workflow below. CSV stores note content only; preserve collection backups for scheduling and review history. The first import produced 135 ADD and a repeat diff produced 135 SKIP.

### PDF “1000 câu – 50 ngày” → Everyday English

The [source index](source/everyday-english/pdf-source.csv) maps all 1,000 sentences to day 01–50, sentence number, original topic and PDF page. **All 20 source sentences per day are now planned as cards.** It retains raw OCR beside corrected text, flags 50 OCR fixes and 172 close substitutions within a day. Days 1–2 have been visually checked; days 3–50 remain `ocr_needs_review` and cannot be staged yet. The PDF itself is not committed. Source file SHA-256: `162cfa65269e092735512a6044932c20754177183fa3c7a44ababe301977e31b`.

The [day 1 CSV](source/everyday-english/pdf-day-01.csv) contains all 20 Level 1 source sentences in Anki. Its three Level 2 [guided substitutions](source/everyday-english/pdf-guided.csv) are suspended until the sentence recall feels comfortable; none had been reviewed before suspension. The [day 2 CSV](source/everyday-english/pdf-day-02.csv) has 20 checked source sentences ready for a later import, but **has not been imported**. The note type keeps the back short and tags notes by day, level and origin. Stable `Key`, Anki IDs and hashes make repeat sync idempotent. Level 3 has one planned, inactive guided example.

The chosen pace is **20 PDF sentence cards per study day**. Import one checked day's CSV when ready; do not import all 1,000 at once. Say the sentence before flipping, then review old days normally. Guided drills are optional and separate from the 20 source sentences. If reviews pile up, pause the next day's import rather than deleting cards. For days 3–50, check all 20 English/Vietnamese pairs against their PDF page, fill `card_pattern`, and change their `review_status` to `visual_checked` and `selection` to `ready` in the source index. Then stage and preview only that day:

```sh
.venv/bin/python tools/pdf_daily.py audit
.venv/bin/python tools/pdf_daily.py stage --day 3 --out source/everyday-english/pdf-day-03.csv
.venv/bin/python tools/cards.py validate --csv source/everyday-english/pdf-day-03.csv
.venv/bin/python tools/cards.py diff --connect \
  --profile "$HOME/Library/Application Support/Anki2/User 1" \
  --csv source/everyday-english/pdf-day-03.csv
# After reviewing the diff, use sync --apply with a new empty --backup-dir.
```

The stage command refuses to overwrite an imported CSV or stage unreviewed content. `--extend` can append newly reviewed cards to an existing day while preserving imported IDs and hashes; it refuses to rewrite existing card content. Future staged CSVs use the existing `tools/cards.py` dry-run, backup and sync workflow. Keep the PDF as reference; OCR text is not a replacement for the page image.

**Progress check:** After the 50 days and ongoing reviews, draw 20 unseen prompts from several days. Aim to say at least 16 correctly within about 3–5 seconds each, then handle five minutes of short AI questions about daily situations. This measures useful recall and response speed; the card count alone is not the goal.

This repository stores a **local, restorable snapshot** of the English learning system and a small speaking pilot. The collection inspected on **2026-11-04 (Asia/Ho_Chi_Minh)** contains a deck named **`English Grammar`**. The requested spelling `English Gramar` was not present; no deck was renamed.

## What is where

| Asset | Location | Purpose | Git |
|---|---|---|---|
| Complete collection and media | `private/backups/2026-11-04-baseline/` | Exact recovery, including IDs and review history | Ignored |
| Before/after cleanup backups | `private/backups/2026-11-04-pre-cleanup-v2/`, `private/backups/2026-11-04-post-cleanup/` | Restore removed decks or current two-deck state | Ignored |
| Full collection package | `private/backups/2026-11-04-baseline/full-collection-with-media.colpkg` | Anki's native whole-collection recovery format | Ignored |
| Original grammar source | `source/english-grammar/notes.csv` | Canonical note content; note type, templates and CSS alongside it | Tracked; review before any public push |
| Original grammar `.apkg` | `private/imports/English Grammar-pristine.apkg` | Import deck into another profile, **without** scheduling | Ignored |
| Pilot source | `source/pilot/notes.csv` | Canonical editable notes; `pilot.json` retained as the initial design record | Tracked |
| Pilot `.apkg` | `private/imports/English Speaking Pilot.apkg` | Import the pilot into a separate profile first | Ignored |
| Audit and design | `reports/`, `docs/` | Evidence, decisions, learning workflow | Tracked |

An `.apkg` can include scheduling if exported that way, but the package here intentionally does not. The complete backup and `.colpkg` are the recovery route for review history. [Anki's export manual](https://docs.ankiweb.net/exporting.html) describes the different package modes; [its backup manual](https://docs.ankiweb.net/backups.html) notes that automatic backups omit media.

**Keep `private/` in an encrypted personal backup outside this machine.** It is ignored to avoid accidentally publishing collection history, personal content, third-party decks, and media. A Git clone can rebuild the grammar deck's content and template from `source/english-grammar/`, but cannot recover original scheduling or the full collection. The grammar source was screened for common email, URL, phone, and API-key patterns; content and licensing still require human review.

## CSV / Excel workflow

`notes.csv` is the source of truth for note content. Excel is an editing view of the same columns. Each deck CSV has a `.schema.json` sidecar describing the exact Anki note type and field order. Columns `_id`, `_guid` and `_base_hash` support stable matching and three-way conflict checks; `field:*` columns hold raw HTML field values. Keep `_base_hash` unchanged while editing. Do not edit `_id` or `_guid` for existing notes. New rows leave `_id`, `_guid` and `_base_hash` empty and must have a unique first field (for these decks, `Key`).

```sh
# Read-only export from the running Anki profile; export refuses to overwrite files.
.venv/bin/python tools/cards.py export --connect \
  --profile "$HOME/Library/Application Support/Anki2/User 1" \
  --deck 'English Grammar' --csv private/grammar-export.csv --xlsx private/grammar-edit.xlsx

# Edit the CSV directly, or edit the XLSX and use --xlsx in subsequent commands.
.venv/bin/python tools/cards.py validate --csv source/pilot/notes.csv
.venv/bin/python tools/cards.py diff --connect \
  --profile "$HOME/Library/Application Support/Anki2/User 1" --csv source/pilot/notes.csv
.venv/bin/python tools/cards.py sync --connect \
  --profile "$HOME/Library/Application Support/Anki2/User 1" --csv source/pilot/notes.csv
```

`sync` and `import` are **dry-run by default**. They print ADD, UPDATE, SKIP and CONFLICT counts, never DELETE. To apply after review, supply `--apply --backup-dir private/backups/NEW-EMPTY-DIR`; the tool makes a verified full snapshot **before** writing, then updates the CSV IDs, GUIDs and base hashes. For edited Excel, use `import --csv source/pilot/notes.csv --xlsx private/pilot-edit.xlsx` with the same target and apply flags; the imported spreadsheet is written back to canonical CSV only after successful application. Updates change fields/tags only, preserving card scheduling and review history. Deck and note type changes are reported as conflicts. The live `English Grammar` deck additionally requires `--allow-grammar-edits` for an apply, to prevent accidental changes to the preserved original.

For the new batch, review the [Everyday English design](docs/everyday-english.md), then run:

```sh
.venv/bin/python tools/cards.py validate --csv source/everyday-english/notes.csv
.venv/bin/python tools/cards.py diff --connect \
  --profile "$HOME/Library/Application Support/Anki2/User 1" \
  --csv source/everyday-english/notes.csv
.venv/bin/python tools/package_csv.py --csv source/everyday-english/notes.csv \
  --out 'private/imports/Everyday English-new.apkg'
```

The initial checked package is `private/imports/Everyday English-pilot.apkg` (36 cards). After the authorized imports, the source CSV holds the live IDs/GUIDs, base hashes and topic subdeck paths in `_deck` (for example, `Everyday English::Greetings`). Repeated sync reports 72 SKIP; no duplicate was created. Backups before the topic split and second 36-card batch are in `private/backups/2026-11-04-before-everyday-topics/` and `private/backups/2026-11-04-before-everyday-batch-2/`.

```sh
# Explicit live apply example for a reviewed non-grammar CSV; do not run until ready.
.venv/bin/python tools/cards.py sync --connect \
  --profile "$HOME/Library/Application Support/Anki2/User 1" \
  --csv source/pilot/notes.csv --apply --backup-dir private/backups/NEW-EMPTY-DIR

# Native whole-collection backup with media and history, or importable deck package.
.venv/bin/python tools/cards.py backup --kind collection \
  --profile "$HOME/Library/Application Support/Anki2/User 1" --out private/backups/NEW-EMPTY-DIR
.venv/bin/python tools/cards.py backup --kind deck \
  --deck 'English Grammar' --out 'private/imports/English Grammar-new.apkg'
```

The `.apkg` command exports one deck without scheduling; `.colpkg` is the full-collection backup with history and media. CSV/XLSX is **never** a backup for scheduling, templates, CSS or media. `--collection PATH` targets a separate Anki collection file for offline testing instead of `--connect --profile PATH`. Never point `--collection` at the open daily collection.

## Setup

The tested environment is Anki 26.5, AnkiConnect API 6, Python 3.13, macOS. Dependencies are `anki` (isolated collection operations), `genanki` (packages), and `openpyxl` (Excel).

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
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tools/cards.py validate --csv source/english-grammar/notes.csv
.venv/bin/python tools/cards.py validate --csv source/pilot/notes.csv
.venv/bin/python tools/anki_repo.py audit --backup private/backups/2026-11-04-baseline
.venv/bin/python tools/anki_repo.py verify --backup private/backups/2026-11-04-baseline
.venv/bin/python tools/anki_repo.py validate-source --source source/english-grammar \
  --media private/backups/2026-11-04-baseline/collection.media
```

The scripts refuse to overwrite populated backup, restore, import-test, and package output paths. They do not delete or change any live deck, note, template, or scheduling data.
