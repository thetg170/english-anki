#!/usr/bin/env python3
"""Build a small importable pilot package without contacting the live Anki profile."""
import argparse
import csv
from pathlib import Path

import genanki

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ["Key", "Mode", "Context", "Task", "Constraint", "Model", "Alternatives", "Check", "Transfer", "Unit"]
MODEL_ID = 1794000000001
DECK_ID = 1794000000002
CSS = """.card {font-family:system-ui,sans-serif;background:#f5f5f7;color:#202126;text-align:left;font-size:19px;line-height:1.45;padding:20px}
.wrap{max-width:650px;margin:auto}.mode{font-size:13px;font-weight:700;color:#3b5dab;text-transform:uppercase}.context{margin:14px 0;padding:12px;background:#e8eaf1;border-radius:9px}.task{font-size:24px;font-weight:650}.constraint{margin-top:12px;color:#555}.speak{margin-top:24px;font-weight:700;color:#9a3154}.answer{font-size:23px;font-weight:650;color:#1b7547}.label{font-size:13px;text-transform:uppercase;color:#777;margin-top:20px}.nightMode .card,.card.nightMode{background:#1c1d21;color:#eee}.nightMode .context{background:#333743}.nightMode .constraint{color:#bbb}hr{border:0;border-top:1px solid #aaa;margin:22px 0}"""
FRONT = """<div class=wrap><div class=mode>{{Mode}} · {{Unit}}</div><div class=context>{{Context}}</div><div class=task>{{Task}}</div><div class=constraint>{{Constraint}}</div><div class=speak>Speak aloud before revealing the answer.</div></div>"""
BACK = """<div class=wrap>{{FrontSide}}<hr><div class=label>One natural answer</div><div class=answer>{{Model}}</div><div class=label>Also acceptable</div><div>{{Alternatives}}</div><div class=label>Grade yourself</div><div>{{Check}}</div><div class=label>Transfer it</div><div>{{Transfer}}</div></div>"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    with (ROOT / "source/pilot/notes.csv").open(newline="", encoding="utf-8") as fh:
        data = list(csv.DictReader(fh))
    keys = [x["field:Key"] for x in data]
    assert len(keys) == len(set(keys)), "Duplicate pilot keys"
    assert len(data) <= 25, "Pilot should remain small"
    for row in data:
        assert all(row["field:" + f].strip() for f in FIELDS)
    model = genanki.Model(MODEL_ID, "EN_Speaking_Pilot_v1",
        fields=[{"name": name} for name in FIELDS],
        templates=[{"name": "Speak", "qfmt": FRONT, "afmt": BACK}], css=CSS)
    deck = genanki.Deck(DECK_ID, "English Speaking Pilot")
    for row in data:
        values = [row["field:" + f] for f in FIELDS]
        note = genanki.Note(model=model, fields=values, guid=row["_guid"] or genanki.guid_for(row["field:Key"]),
                            tags=row["_tags"].split())
        deck.add_note(note)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(deck).write_to_file(str(args.out))
    print(f"Created {args.out} with {len(data)} notes/cards")


if __name__ == "__main__":
    main()
