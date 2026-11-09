# `English Grammar`: design analysis

This describes the deck observed on 2026-11-04. Its exact name remains `English Grammar`; the requested spelling `English Gramar` was not present. The original is preserved in a complete collection backup, an importable package, and local source JSONL. No live note or note type was edited during that initial audit. On 2026-11-09, 65 note prompts and matching answers were clarified in the live deck at the learner's request; the note type and template were unchanged.

## Structure

- 581 notes and 581 cards; one `Drill` card template, note type `EN_Grammar_Drill`.
- Fields: `Key`, `Front`, `Back`, `Say`, `Listen`, `Unit`.
- `Key` is a stable unique identifier. `Front` and `Back` contain HTML with prompt and feedback. `Say` gives a sentence for text-to-speech. `Listen` activates TTS and `{{type:Say}}` on 50 cards. `Unit` identifies one of 15 grammar units.
- CSS (4,754 characters) distinguishes prompt modes, answer, explanation, and self-check; it supports dark mode. The template has no JavaScript or literal local media reference. TTS requests Apple Samantha voices where available, so the listening experience can vary by device.
- `Say` is filled on 580 cards. The note with no `Say` does not break the template because `{{#Say}}` gates the answer audio.

The template, CSS, current field HTML, note IDs, and GUIDs are tracked in `source/english-grammar/`. The original complete collection backup is authoritative for the 2026-11-04 state. The backup immediately before the 2026-11-09 clarification is in `private/backups/2026-11-09-grammar-prompt-clarity/`.

## What makes it effective

The front asks a specific question and frequently says to answer **before flipping**. It uses distinct tasks: explain a rule, complete a form, choose, diagnose an error, interpret meaning, transcribe audio, or say a full sentence. The back often provides a short explanation, not just a word. The `kind::speak` prompt “Đây không phải lỗi của bạn — là lỗi của tôi (fault)” requires retrieving an English sentence; “It's not your fault. It's mine” is a model answer. `kind::form` asks for “My sister ___ in a bank (work)” and instructs the learner to say the entire sentence, adding oral output to a small form decision.

This is stronger than showing a rule and asking whether it looks familiar. The different prompt types also reveal different failure modes: recognizing the right form, recalling it, and producing a sentence are separate achievements.

## Where it stops short of spontaneous speech

| Task | Cards | Main demand | Possible shortcut |
|---|---:|---|---|
| Rule | 114 | State knowledge | Recite a rule without using it |
| Choose | 126 | Discriminate visible options | Recognize without generating |
| Form | 100 | Supply a word form | Complete a blank in a known sentence |
| Fix | 91 | Judge/correct | Say “correct” on unchanged examples |
| Meaning | 28 | Interpret | Explain in Vietnamese only |
| Listen | 50 | Perceive and type | Dictation, not own speech |
| Speak | 72 | Produce a sentence | Memorize one sentence tied to its Vietnamese cue |

These are task properties, not measured learner behavior. “Say it aloud” on a recognition card helps articulation but does not turn a multiple-choice question into open-ended production. The next layer should require a new context, a self-chosen wording, and a follow-up response. It should accept multiple correct formulations and be tested on unseen prompts.

## Principles carried into the pilot

1. One clear communicative purpose per card, with a small constraint tied to a grammar unit.
2. Speak before revealing. The answer is a model, while a checklist defines success.
3. Give at least one alternative and a transfer prompt; do not reward verbatim recall alone.
4. Keep explanations brief and concrete, as the existing deck does.
5. Use real errors for new repair cards when available; the pilot's example repairs are only starter material.

The 2026-11-09 clarification changed note text only. Card scheduling and review history were verified identical to the pre-change backup; all 581 notes retained their IDs, and a repeat diff reported 581 SKIP.
