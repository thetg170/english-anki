#!/usr/bin/env python3
"""Build one importable .apkg from a canonical CSV and its schema."""
import argparse, hashlib, json
from pathlib import Path

import genanki
from cards import read_table, validate

def stable_id(value):
    return int.from_bytes(hashlib.sha256(value.encode()).digest()[:6], 'big')

def main():
    p=argparse.ArgumentParser();p.add_argument('--csv',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.out.exists():raise SystemExit('Refusing to overwrite package')
    schema=json.loads(a.csv.with_suffix('.schema.json').read_text())
    headers,rows=read_table(a.csv);errors=validate(headers,rows,schema)
    if errors:raise SystemExit('\n'.join(errors))
    templates=[{'name':name,'qfmt':t['Front'],'afmt':t['Back']} for name,t in schema['templates'].items()]
    model=genanki.Model(stable_id('model:'+schema['notetype']),schema['notetype'],
        fields=[{'name':f} for f in schema['fields']],templates=templates,css=schema['css'])
    deck_names={schema['deck'],*(row['_deck'] for row in rows)}
    decks={name:genanki.Deck(stable_id('deck:'+name),name) for name in sorted(deck_names)}
    for row in rows:
        values=[row['field:'+f] for f in schema['fields']]
        decks[row['_deck']].add_note(genanki.Note(model=model,fields=values,
            guid=row['_guid'] or genanki.guid_for(schema['notetype'],values[0]),tags=row['_tags'].split()))
    a.out.parent.mkdir(parents=True,exist_ok=True)
    genanki.Package(list(decks.values())).write_to_file(str(a.out))
    print(f'Packaged {len(rows)} notes: {a.out}')

if __name__=='__main__':main()
