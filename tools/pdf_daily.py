#!/usr/bin/env python3
"""Audit the 50-day PDF index and prepare one reviewed day for CSV-first Anki sync."""

import argparse
import csv
import json
import re
import shutil
from collections import Counter
from pathlib import Path

from cards import META, validate, write_table

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source/everyday-english/pdf-source.csv'
DRILLS = ROOT / 'source/everyday-english/pdf-guided.csv'
SCHEMA = ROOT / 'source/everyday-english/pdf-notes.schema.json'


def read(path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def normalize(text):
    return re.sub(r'[^a-z0-9]+', ' ', text.casefold()).strip()


def check(source, drills):
    errors = []
    numbers = [int(row['sentence_no']) for row in source]
    if numbers != list(range(1, 1001)):
        errors.append('Source must contain sentence numbers 1–1000 in order')
    for row in source:
        number = int(row['sentence_no'])
        day = (number - 1) // 20 + 1
        if int(row['day']) != day or int(row['sentence_in_day']) != (number - 1) % 20 + 1:
            errors.append(f'{row["source_id"]}: day/sequence mismatch')
        if int(row['pdf_page']) != 2 * day or not row['english'] or not row['vietnamese']:
            errors.append(f'{row["source_id"]}: page or text missing')
        if row['selection'] == 'ready' and (row['review_status'] != 'visual_checked' or not row['card_pattern']):
            errors.append(f'{row["source_id"]}: ready card needs visual review and pattern')
    keys = [row['key'] for row in drills]
    if len(set(keys)) != len(keys):
        errors.append('Duplicate drill key')
    source_ids = {row['source_id'] for row in source}
    for row in drills:
        if row['source_id'] not in source_ids or row['level'] not in {'level_2', 'level_3'}:
            errors.append(f'{row["key"]}: invalid source or level')
    existing = {normalize(row['field:Answer']) for row in read(ROOT / 'source/everyday-english/notes.csv')}
    for row in source:
        if row['selection'] == 'ready' and normalize(row['english']) in existing:
            errors.append(f'{row["source_id"]}: duplicates an existing Everyday English answer')
    for row in drills:
        if row['status'] == 'ready' and normalize(row['answer']) in existing:
            errors.append(f'{row["key"]}: duplicates an existing Everyday English answer')
    return errors


def stage(day, out, source, drills):
    if out.exists() or out.with_suffix('.schema.json').exists():
        raise ValueError('Refusing to overwrite a staged or imported CSV')
    schema = json.loads(SCHEMA.read_text())
    by_id = {row['source_id']: row for row in source}
    fields = schema['fields']
    headers = META + ['field:' + name for name in fields]
    staged = []

    def add(key, topic, prompt, answer, alternative, pattern, origin, source_row, level):
        tags = f'day_{day:02} {level} origin_{origin} pdf_1000'
        source_note = f'PDF trang {source_row["pdf_page"]} · ngày {day:02} · câu {source_row["sentence_no"]}'
        if origin == 'editorial_drill':
            source_note += ' · bài luyện biên soạn'
        elif prompt != source_row['vietnamese']:
            source_note += ' · gợi ý tiếng Việt biên tập'
        values = [key, topic, prompt, answer, alternative, pattern, source_note]
        staged.append(dict(zip(headers, ['', '', schema['deck'], schema['notetype'], tags, '', *values])))

    for row in source:
        if int(row['day']) != day or row['selection'] != 'ready':
            continue
        if row['review_status'] != 'visual_checked':
            raise ValueError(f'{row["source_id"]} has not been visually checked')
        add(f'pdf.d{day:02}.s{row["sentence_in_day"]}.l1', row['topic_original'],
            row['card_prompt'] or row['vietnamese'], row['english'], row['card_alternative'],
            row['card_pattern'], 'pdf', row, 'level_1')
    for drill in drills:
        if int(drill['day']) != day or drill['status'] != 'ready':
            continue
        base = by_id[drill['source_id']]
        if base['review_status'] != 'visual_checked':
            raise ValueError(f'{drill["key"]} refers to unreviewed PDF text')
        add(drill['key'], base['topic_original'], drill['prompt'], drill['answer'],
            drill['alternative'], drill['pattern'], 'editorial_drill', base, drill['level'])
    if not staged:
        raise ValueError(f'Day {day:02} has no reviewed cards ready to stage')
    errors = validate(headers, staged, schema)
    if errors:
        raise ValueError('\n'.join(errors))
    write_table(out, headers, staged)
    shutil.copyfile(SCHEMA, out.with_suffix('.schema.json'))
    print(f'STAGED day {day:02}: {len(staged)} cards at {out}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['audit', 'stage'])
    parser.add_argument('--day', type=int)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    source, drills = read(SOURCE), read(DRILLS)
    errors = check(source, drills)
    if errors:
        raise ValueError('\n'.join(errors))
    if args.command == 'audit':
        selected = Counter(row['selection'] for row in source)
        levels = Counter(row['level'] for row in drills)
        normalized = Counter(normalize(row['english']) for row in source)
        print(f'VALID source={len(source)} days=50 selected={dict(selected)} guided={dict(levels)} '
              f'exact_duplicates={sum(count - 1 for count in normalized.values())} '
              f'near_duplicates={sum(bool(row["near_duplicate_of"]) for row in source)}')
    else:
        if not args.day or not 1 <= args.day <= 50 or not args.out:
            parser.error('stage requires --day 1..50 and --out PATH')
        stage(args.day, args.out, source, drills)


if __name__ == '__main__':
    main()
