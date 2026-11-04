import csv, subprocess, sys, tempfile, unittest
from collections import Counter
from pathlib import Path

from anki.collection import Collection
from anki.importing import AnkiPackageImporter
from anki.lang import set_lang

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'source/everyday-english/notes.csv'

class EverydayBatch(unittest.TestCase):
    def test_content_and_package(self):
        with SOURCE.open(newline='',encoding='utf-8') as fh:rows=list(csv.DictReader(fh))
        self.assertEqual(len(rows),72)
        self.assertEqual(set(Counter(r['field:Topic'] for r in rows).values()),{8})
        self.assertEqual(len({r['field:Key'] for r in rows}),72)
        self.assertEqual(len({r['field:Answer'] for r in rows}),72)
        for row in rows:
            self.assertLessEqual(len(row['field:Answer'].split()),12)
            self.assertEqual(len(row['field:Variations'].split('<br>')),2)
            self.assertTrue(all(row['field:'+f].strip() for f in
                ['SituationVI','Answer','Pattern','Variations','NoteVI','PracticeVI']))
        with tempfile.TemporaryDirectory() as temp:
            package=Path(temp)/'everyday.apkg'
            result=subprocess.run([sys.executable,str(ROOT/'tools/package_csv.py'),'--csv',str(SOURCE),
                                   '--out',str(package)],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            set_lang('en_US');c=Collection(str(Path(temp)/'collection.anki2'))
            AnkiPackageImporter(c,str(package)).run()
            ids=c.find_cards('deck:"Everyday English"')
            self.assertEqual((c.note_count(),len(ids)),(72,72))
            topic_decks=[x.name for x in c.decks.all_names_and_ids() if x.name.startswith('Everyday English::')]
            self.assertEqual(len(topic_decks),9)
            for deck in topic_decks:self.assertEqual(len(c.find_cards('deck:"'+deck+'"')),8)
            for cid in ids:
                card=c.get_card(cid)
                self.assertNotIn('{{',card.question());self.assertNotIn('{{',card.answer())
            c.close()

if __name__=='__main__':unittest.main()
