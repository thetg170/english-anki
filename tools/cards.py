#!/usr/bin/env python3
"""CSV-first note editor. No card deletion or scheduling writes."""
import argparse, csv, hashlib, json, shutil, sys, tempfile
from pathlib import Path
from openpyxl import Workbook, load_workbook

META = ['_id','_guid','_deck','_notetype','_tags','_base_hash']

def digest(row, fields):
    obj = {'deck':row['_deck'],'notetype':row['_notetype'],'tags':sorted(row['_tags'].split()),
           'fields':{f:row['field:'+f] for f in fields}}
    return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def read_table(path):
    if path.suffix.lower()=='.xlsx':
        ws=load_workbook(path,read_only=True,data_only=False).active
        data=list(ws.values)
        if not data: raise ValueError('Empty spreadsheet')
        headers=[str(x or '') for x in data[0]]
        rows=[dict(zip(headers,[str(v) if v is not None else '' for v in values])) for values in data[1:] if any(v is not None for v in values)]
    else:
        with path.open(newline='',encoding='utf-8-sig') as fh:
            reader=csv.DictReader(fh);headers=reader.fieldnames or [];rows=list(reader)
    return headers,rows

def write_table(path,headers,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.suffix.lower()=='.xlsx':
        wb=Workbook();ws=wb.active;ws.title='Notes';ws.append(headers)
        for row in rows: ws.append([row.get(h,'') for h in headers])
        ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions;wb.save(path)
    else:
        with path.open('w',newline='',encoding='utf-8') as fh:
            w=csv.DictWriter(fh,fieldnames=headers,lineterminator='\n');w.writeheader();w.writerows(rows)

def validate(headers,rows,schema):
    errors=[];fields=schema['fields'];expected=META+['field:'+x for x in fields]
    if headers!=expected: errors.append(f'Header mismatch: expected {expected}')
    seen_id=set();seen_guid=set();seen_first=set()
    for n,row in enumerate(rows,2):
        if row.get('_deck')!=schema['deck'] or row.get('_notetype')!=schema['notetype']:
            errors.append(f'row {n}: deck/note type mismatch')
        first=row.get('field:'+fields[0],'').strip()
        if not first: errors.append(f'row {n}: missing first field')
        for key,seen in [('_id',seen_id),('_guid',seen_guid)]:
            v=row.get(key,'')
            if v and v in seen: errors.append(f'row {n}: duplicate {key} {v}')
            seen.add(v)
        if first in seen_first: errors.append(f'row {n}: duplicate first field {first}')
        seen_first.add(first)
        if row.get('_base_hash') and (len(row['_base_hash'])!=64 or any(x not in '0123456789abcdef' for x in row['_base_hash'])):
            errors.append(f'row {n}: malformed base hash')
    return errors

class Offline:
    def __init__(self,path):
        from anki.collection import Collection
        self.col=Collection(str(path));self.deck=None
    def close(self): self.col.close()
    def records(self,deck):
        d=self.col.decks.by_name(deck)
        if not d: return []
        self.deck=d
        result=[]
        for nid in self.col.find_notes('deck:"'+deck.replace('"','\\"')+'"'):
            note=self.col.get_note(nid);model=self.col.models.get(note.mid)
            if any(self.col.get_card(cid).did!=d['id'] for cid in note.card_ids()):
                raise ValueError(f'Note {nid} spans decks; export separately')
            result.append({'_id':str(nid),'_guid':note.guid,'_deck':deck,'_notetype':model['name'],
                           '_tags':' '.join(sorted(note.tags)),**{'field:'+k:note[k] for k in note.keys()}})
        return result
    def fields(self,name):
        m=self.col.models.by_name(name)
        if not m: return None
        return [f['name'] for f in m['flds']]
    def spec(self,name):
        m=self.col.models.by_name(name)
        return {'templates':{t['name']:{'Front':t['qfmt'],'Back':t['afmt']} for t in m['tmpls']},'css':m['css']}
    def ensure(self,schema):
        if not self.col.models.by_name(schema['notetype']):
            if not schema.get('templates'):raise ValueError('No template in schema for new note type')
            m=self.col.models.new(schema['notetype']);m['css']=schema['css']
            for name in schema['fields']:self.col.models.add_field(m,self.col.models.new_field(name))
            for name,t in schema['templates'].items():
                card=self.col.models.new_template(name);card['qfmt']=t['Front'];card['afmt']=t['Back']
                self.col.models.add_template(m,card)
            self.col.models.add(m)
        self.col.decks.id(schema['deck'])
    def add(self,row,fields):
        note=self.col.new_note(self.col.models.by_name(row['_notetype']))
        for f in fields: note[f]=row['field:'+f]
        note.tags=row['_tags'].split();self.col.add_note(note,self.deck['id'])
        return str(note.id),note.guid
    def update(self,row,fields):
        note=self.col.get_note(int(row['_id']))
        for f in fields: note[f]=row['field:'+f]
        note.tags=row['_tags'].split();self.col.update_note(note)

class Connect:
    def __init__(self,profile):
        from anki_repo import anki_connect,connect
        self.call=anki_connect;self.deck=None;self.profile=profile;self.sql_connect=connect
    def close(self): pass
    def fields(self,name):
        return self.call('modelFieldNames',{'modelName':name}) if name in self.call('modelNames',{}) else None
    def spec(self,name):
        return {'templates':self.call('modelTemplates',{'modelName':name}),
                'css':self.call('modelStyling',{'modelName':name})['css']}
    def ensure(self,schema):
        if schema['notetype'] not in self.call('modelNames',{}):
            if not schema.get('templates'):raise ValueError('No template in schema for new note type')
            self.call('createModel',{'modelName':schema['notetype'],'inOrderFields':schema['fields'],
                'cardTemplates':[{'Name':n,**v} for n,v in schema['templates'].items()],
                'css':schema['css']})
        if schema['deck'] not in self.call('deckNames',{}):self.call('createDeck',{'deck':schema['deck']})
    def records(self,deck):
        if deck not in self.call('deckNames',{}): return []
        self.deck=deck;ids=self.call('findNotes',{'query':'deck:"'+deck.replace('"','\\"')+'"'})
        result=[]
        db=self.sql_connect(self.profile/'collection.anki2')
        guids=dict(db.execute('select id,guid from notes'));db.close()
        for i in range(0,len(ids),100):
            for note in self.call('notesInfo',{'notes':ids[i:i+100]}):
                result.append({'_id':str(note['noteId']),'_guid':guids[note['noteId']], '_deck':deck,
                    '_notetype':note['modelName'],'_tags':' '.join(sorted(note['tags'])),
                    **{'field:'+k:v['value'] for k,v in note['fields'].items()}})
        return result
    def add(self,row,fields):
        nid=self.call('addNote',{'note':{'deckName':row['_deck'],'modelName':row['_notetype'],
             'fields':{f:row['field:'+f] for f in fields},'tags':row['_tags'].split()}})
        db=self.sql_connect(self.profile/'collection.anki2')
        guid=db.execute('select guid from notes where id=?',(nid,)).fetchone()[0];db.close()
        return str(nid),guid
    def update(self,row,fields):
        nid=int(row['_id'])
        self.call('updateNoteFields',{'note':{'id':nid,'fields':{f:row['field:'+f] for f in fields}}})
        old=self.call('notesInfo',{'notes':[nid]})[0]['tags'];new=row['_tags'].split()
        remove=set(old)-set(new);add=set(new)-set(old)
        if remove:self.call('removeTags',{'notes':[nid],'tags':' '.join(remove)})
        if add:self.call('addTags',{'notes':[nid],'tags':' '.join(add)})

def plan(rows,live,fields):
    byid={r['_id']:r for r in live};byfirst={r['field:'+fields[0]]:r for r in live};actions=[]
    for row in rows:
        current=byid.get(row['_id']) if row['_id'] else byfirst.get(row['field:'+fields[0]])
        if row['_id'] and not current: action='CONFLICT';reason='ID missing'
        elif not current: action='ADD';reason='new first field'
        elif row['_guid'] and current['_guid']!=row['_guid']: action='CONFLICT';reason='GUID mismatch'
        elif current['_notetype']!=row['_notetype'] or current['_deck']!=row['_deck']: action='CONFLICT';reason='schema/deck mismatch'
        elif digest(row,fields)==digest(current,fields): action='SKIP';reason='already equal'
        elif row['_base_hash'] and digest(current,fields)==row['_base_hash']: action='UPDATE';reason='source changed, Anki unchanged'
        else: action='CONFLICT';reason='Anki differs from baseline or matching first field'
        actions.append((action,reason,row,current))
    return actions

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='cmd',required=True)
    e=sub.add_parser('export');e.add_argument('--deck',required=True);e.add_argument('--csv',type=Path,required=True);e.add_argument('--xlsx',type=Path)
    for name in ['validate','diff','sync','import']:
        q=sub.add_parser(name);q.add_argument('--csv',type=Path,required=True);q.add_argument('--xlsx',type=Path)
        if name in ['sync','import']:q.add_argument('--apply',action='store_true');q.add_argument('--backup-dir',type=Path)
    b=sub.add_parser('backup');b.add_argument('--profile',type=Path);b.add_argument('--out',type=Path,required=True)
    b.add_argument('--kind',choices=['collection','deck'],required=True);b.add_argument('--deck')
    for name in ['export','diff','sync','import']:
        q=sub.choices[name];q.add_argument('--collection',type=Path);q.add_argument('--connect',action='store_true');q.add_argument('--profile',type=Path)
        if name in ['sync','import']:q.add_argument('--allow-grammar-edits',action='store_true')
    a=p.parse_args()
    if a.cmd=='backup':
        from anki_repo import backup,export_package,sha256
        if a.kind=='deck':
            if not a.deck or a.out.suffix!='.apkg':raise ValueError('Deck backup needs --deck and .apkg output')
            export_package(a.deck,a.out);return 0
        if not a.profile:raise ValueError('Collection backup needs --profile')
        from anki.collection import Collection
        from anki.exporting import AnkiCollectionPackageExporter
        from anki.lang import set_lang
        backup(a.profile,a.out)
        package=a.out/'full-collection-with-media.colpkg'
        with tempfile.TemporaryDirectory(prefix='anki-colpkg-stage-') as temp:
            stage=Path(temp)
            shutil.copy2(a.out/'collection.anki2',stage/'collection.anki2')
            shutil.copytree(a.out/'collection.media',stage/'collection.media')
            set_lang('en_US');col=Collection(str(stage/'collection.anki2'))
            exporter=AnkiCollectionPackageExporter(col);exporter.includeMedia=True;exporter.exportInto(str(package))
        (a.out/(package.name+'.sha256')).write_text(sha256(package)+'  '+package.name+'\n')
        print(f'COLPKG {package}');return 0
    if a.cmd=='validate':
        schema=json.loads(a.csv.with_suffix('.schema.json').read_text());h,r=read_table(a.xlsx or a.csv)
        errors=validate(h,r,schema)
        print('\n'.join(errors) if errors else f'VALID {len(r)} rows');return 1 if errors else 0
    if bool(a.collection)==bool(a.connect): raise ValueError('Choose exactly one: --collection or --connect')
    if a.connect and not a.profile:raise ValueError('--profile required with --connect')
    adapter=Offline(a.collection) if a.collection else Connect(a.profile)
    try:
        if a.cmd=='export':
            if a.csv.exists() or (a.xlsx and a.xlsx.exists()):raise ValueError('Refusing to overwrite export')
            live=adapter.records(a.deck);types={r['_notetype'] for r in live}
            if len(types)!=1:raise ValueError('Export one note type at a time')
            name=types.pop();fields=adapter.fields(name);headers=META+['field:'+f for f in fields]
            for row in live:row['_base_hash']=digest(row,fields)
            write_table(a.csv,headers,live)
            a.csv.with_suffix('.schema.json').write_text(json.dumps({'deck':a.deck,'notetype':name,'fields':fields,
                **adapter.spec(name)},ensure_ascii=False,indent=2)+'\n')
            if a.xlsx:write_table(a.xlsx,headers,live)
            print(f'EXPORTED {len(live)} notes');return 0
        schema=json.loads(a.csv.with_suffix('.schema.json').read_text())
        h,rows=read_table(a.xlsx or a.csv);errors=validate(h,rows,schema)
        if errors:raise ValueError('\n'.join(errors))
        fields=schema['fields'];live=adapter.records(schema['deck'])
        existing_fields=adapter.fields(schema['notetype'])
        if existing_fields is not None and existing_fields!=fields:raise ValueError('Anki note type fields changed')
        actions=plan(rows,live,fields)
        for action,reason,row,_ in actions:
            if action!='SKIP':print(action,row['field:'+fields[0]],reason)
        counts={x:sum(a==x for a,_,_,_ in actions) for x in ['ADD','UPDATE','SKIP','CONFLICT']}
        print(json.dumps(counts))
        if a.cmd=='diff' or not a.apply:print('DRY RUN; use --apply with --backup-dir to write');return 1 if counts['CONFLICT'] else 0
        if counts['CONFLICT']:raise ValueError('Conflicts must be resolved before apply')
        if not a.backup_dir:raise ValueError('--backup-dir required before apply')
        if a.connect and schema['deck']=='English Grammar' and not a.allow_grammar_edits:
            raise ValueError('Original grammar deck is protected; --allow-grammar-edits required')
        from anki_repo import backup
        profile=a.collection.parent if a.collection else a.profile
        adapter.close();backup(profile,a.backup_dir)
        adapter=Offline(a.collection) if a.collection else Connect(a.profile)
        adapter.ensure(schema)
        actions=plan(rows,adapter.records(schema['deck']),fields)
        if any(action=='CONFLICT' for action,_,_,_ in actions):
            raise ValueError('Conflict appeared after backup; nothing was applied')
        for action,_,row,current in actions:
            if action=='ADD':row['_id'],row['_guid']=adapter.add(row,fields)
            elif action=='UPDATE':adapter.update(row,fields)
            if action in ('ADD','UPDATE') or (action=='SKIP' and current):
                row['_base_hash']=digest(row,fields)
        write_table(a.csv,h,rows)
        print('APPLIED; CSV rebased; scheduling untouched')
        return 0
    finally: adapter.close()

if __name__=='__main__':sys.exit(main())
