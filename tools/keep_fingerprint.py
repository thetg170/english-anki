#!/usr/bin/env python3
"""Read-only fingerprint of the two protected decks and their review history."""
import argparse, hashlib, json
from pathlib import Path
from anki_repo import connect

KEEP=('English Grammar','DE Knowledge')

def fingerprint(path):
    db=connect(path)
    dids={name:db.execute('select id from decks where name=?',(name,)).fetchone()[0] for name in KEEP}
    ids=tuple(dids.values());marks=','.join('?'*len(ids))
    card_ids=[r[0] for r in db.execute(f'select id from cards where did in ({marks})',ids)]
    note_ids=[r[0] for r in db.execute(f'select distinct nid from cards where did in ({marks})',ids)]
    ntids=[r[0] for r in db.execute('select distinct mid from notes where id in ('+','.join('?'*len(note_ids))+')',note_ids)]
    def hash_rows(query,args=()):
        h=hashlib.sha256();rows=db.execute(query,args).fetchall()
        for row in rows:
            h.update(repr(row).encode());h.update(b'\n')
        return {'rows':len(rows),'sha256':h.hexdigest()}
    card_marks=','.join('?'*len(card_ids));note_marks=','.join('?'*len(note_ids));nt_marks=','.join('?'*len(ntids))
    result={'decks':{},'fingerprints':{
        'notes':hash_rows(f'select * from notes where id in ({note_marks}) order by id',note_ids),
        'cards':hash_rows(f'select * from cards where id in ({card_marks}) order by id',card_ids),
        'revlog':hash_rows(f'select * from revlog where cid in ({card_marks}) order by id',card_ids),
        'notetypes':hash_rows(f'select * from notetypes where id in ({nt_marks}) order by id',ntids),
        'fields':hash_rows(f'select * from fields where ntid in ({nt_marks}) order by ntid,ord',ntids),
        'templates':hash_rows(f'select * from templates where ntid in ({nt_marks}) order by ntid,ord',ntids),
        'deck_rows':hash_rows(f'select * from decks where id in ({marks}) order by id',ids),
        'deck_config':hash_rows('select * from deck_config order by id')}}
    for name,did in dids.items():
        result['decks'][name]={'id':did,'notes':db.execute('select count(distinct nid) from cards where did=?',(did,)).fetchone()[0],
            'cards':db.execute('select count(*) from cards where did=?',(did,)).fetchone()[0],
            'review_rows':db.execute('select count(*) from revlog where cid in (select id from cards where did=?)',(did,)).fetchone()[0]}
    result['collection']={t:db.execute(f'select count(*) from {t}').fetchone()[0] for t in ('decks','notes','cards','revlog')}
    result['other_decks']=[n.replace('\x1f','::') for i,n in db.execute('select id,name from decks') if i not in ids]
    result['cross_deck_notes']=db.execute('select count(*) from (select nid from cards group by nid having count(distinct did)>1)').fetchone()[0]
    db.close();return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--collection',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    value=fingerprint(a.collection);a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'collection':value['collection'],'keep':value['decks'],'other_decks':len(value['other_decks']),
                      'cross_deck_notes':value['cross_deck_notes']},ensure_ascii=False))
