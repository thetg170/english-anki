import csv, json, subprocess, sys, tempfile, unittest
from pathlib import Path

from anki.collection import Collection
from anki.importing import AnkiPackageImporter
from anki.lang import set_lang
from openpyxl import load_workbook

ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'tools/cards.py'
PACKAGE=ROOT/'private/imports/English Speaking Pilot.apkg'

class RoundTrip(unittest.TestCase):
    def run_cli(self,*args):
        return subprocess.run([sys.executable,str(CLI),*map(str,args)],cwd=ROOT,text=True,capture_output=True)

    def test_export_excel_update_add_idempotence_conflict(self):
        set_lang('en_US')
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp);profile=base/'profile';profile.mkdir();(profile/'collection.media').mkdir()
            db=profile/'collection.anki2';c=Collection(str(db))
            AnkiPackageImporter(c,str(PACKAGE)).run()
            card=c.get_card(c.find_cards('deck:"English Speaking Pilot"')[0]);card.reps=3;card.ivl=7;c.update_card(card)
            card_id=card.id;before=(card.reps,card.ivl);c.close()
            csvpath=base/'notes.csv';xlsx=base/'notes.xlsx'
            self.assertEqual(self.run_cli('export','--collection',db,'--deck','English Speaking Pilot','--csv',csvpath,'--xlsx',xlsx).returncode,0)
            self.assertEqual(self.run_cli('validate','--csv',csvpath,'--xlsx',xlsx).returncode,0)
            with csvpath.open(newline='') as fh: rows=list(csv.DictReader(fh));headers=list(rows[0])
            rows[0]['field:Model']='A valid changed model answer.'
            new={k:'' for k in headers};new.update({'_deck':'English Speaking Pilot','_notetype':'EN_Speaking_Pilot_v1',
                'field:Key':'test.new.001','field:Mode':'Situation','field:Context':'A new situation.',
                'field:Task':'Ask politely.','field:Constraint':'Speak aloud.','field:Model':'Could you help me?',
                'field:Alternatives':'Can you help?','field:Check':'Polite request.','field:Transfer':'Ask a friend.',
                'field:Unit':'Modal Verbs'})
            rows.append(new)
            with csvpath.open('w',newline='') as fh:
                w=csv.DictWriter(fh,fieldnames=headers);w.writeheader();w.writerows(rows)
            dry=self.run_cli('diff','--collection',db,'--csv',csvpath)
            self.assertEqual(dry.returncode,0,dry.stderr)
            self.assertIn('"ADD": 1',dry.stdout);self.assertIn('"UPDATE": 1',dry.stdout)
            self.assertEqual(self.run_cli('sync','--collection',db,'--csv',csvpath).returncode,0)
            c=Collection(str(db));self.assertEqual(c.note_count(),17);c.close()
            apply=self.run_cli('sync','--collection',db,'--csv',csvpath,'--apply','--backup-dir',base/'backup')
            self.assertEqual(apply.returncode,0,apply.stderr)
            c=Collection(str(db));self.assertEqual(c.note_count(),18)
            card=c.get_card(card_id);self.assertEqual((card.reps,card.ivl),before);c.close()
            again=self.run_cli('diff','--collection',db,'--csv',csvpath)
            self.assertIn('"SKIP": 18',again.stdout)
            excel_csv=base/'excel-notes.csv';excel_xlsx=base/'excel-notes.xlsx'
            self.assertEqual(self.run_cli('export','--collection',db,'--deck','English Speaking Pilot',
                                          '--csv',excel_csv,'--xlsx',excel_xlsx).returncode,0)
            wb=load_workbook(excel_xlsx);ws=wb.active
            model_col=list(next(ws.values)).index('field:Model')+1
            ws.cell(2,model_col).value='Edited in Excel.';wb.save(excel_xlsx)
            excel_dry=self.run_cli('import','--collection',db,'--csv',excel_csv,'--xlsx',excel_xlsx)
            self.assertIn('"UPDATE": 1',excel_dry.stdout)
            excel_apply=self.run_cli('import','--collection',db,'--csv',excel_csv,'--xlsx',excel_xlsx,
                                     '--apply','--backup-dir',base/'backup-excel')
            self.assertEqual(excel_apply.returncode,0,excel_apply.stderr)
            self.assertIn('"SKIP": 18',self.run_cli('diff','--collection',db,'--csv',excel_csv).stdout)
            with csvpath.open(newline='') as fh: rows=list(csv.DictReader(fh))
            rows[0]['field:Model']='Change from CSV again.'
            with csvpath.open('w',newline='') as fh:
                w=csv.DictWriter(fh,fieldnames=headers);w.writeheader();w.writerows(rows)
            c=Collection(str(db));n=c.get_note(int(rows[0]['_id']));n['Model']='Independent Anki edit.';c.update_note(n);c.close()
            conflict=self.run_cli('diff','--collection',db,'--csv',csvpath)
            self.assertNotEqual(conflict.returncode,0);self.assertIn('"CONFLICT": 1',conflict.stdout)

if __name__=='__main__':unittest.main()
