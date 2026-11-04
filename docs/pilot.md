# Speaking pilot: 17 cards

The canonical source is [notes.csv](../source/pilot/notes.csv), with its [schema](../source/pilot/notes.schema.json). [pilot.json](../source/pilot/pilot.json) remains as the initial design record. The package is `private/imports/English Speaking Pilot.apkg`. It was imported and rendered in a separate collection only. Do not import it into the active learning profile until you choose to trial it there.

## Note type and card behavior

One note creates one `Speak` card, with fields `Key`, `Mode`, `Context`, `Task`, `Constraint`, `Model`, `Alternatives`, `Check`, `Transfer`, `Unit`. The JSON source additionally records a difficulty `level` (1 or 2), exported as a tag. The front shows context, task, constraint, and **“Speak aloud before revealing the answer.”** The back shows one model, acceptable alternatives, a grading checklist, and a transfer prompt. CSS is self-contained, without JavaScript or media. The package is rebuilt with a stable model ID, deck ID, and GUID derived from `Key`.

| Mode | Count | Example front | Example back / grading | Progression and risk |
|---|---:|---|---|---|
| **Transform** | 6 | “We left late, so we missed the train. Say how the result could have been different. Use a third conditional.” | “If we'd left earlier, we wouldn't have missed the train.” Also acceptable: reversed clause order. Check past perfect + would have + past participle. | Begin with one changed feature; later change context or supply no starter sentence. Risk: mechanical tense swap without meaning. |
| **Situation** | 6 | “You arrive at a restaurant with a friend, no reservation. Ask the host for a table.” | “Could we have a table for two, please?” Alternatives include “Do you have a table for two?” Grade clear intention and polite tone, not exact words. | Add a follow-up, objection, or different listener. Risk: rehearsing a script that fails when the reply changes. |
| **Repair** | 5 | “I look forward to hear from you. Correct it.” | “I look forward to hearing from you.” Check `look forward to + V-ing`; say full sentence. | Move from supplied errors to errors captured from your own speech; later fix without a hint. Risk: becoming good at spotting someone else's error without avoiding it in live speech. |

All model sentences and alternatives are examples. A different natural answer is correct when it meets the checklist and communicative intent. If unsure, mark the card Hard and check with a reliable source or tutor; avoid forcing exact-match scoring. Say the full response **before** flipping. After flipping, say a second version or do the `Transfer` task on one card per session. A silent mental answer is practice, but does not satisfy the pilot's speaking criterion.

Suggested self-grading: **Again** if unable to say a meaningful sentence or the target structure failed; **Hard** if correct only after a long pause or heavy cue use; **Good** if said aloud naturally enough and met the checklist; **Easy** only if a new variation also came easily. This rubric is a pilot convention, not a claim that Anki grades speaking automatically.

After two weeks, keep only cards that expose a real gap or transfer to new prompts. Before expanding beyond 17 cards, compare recorded responses on unseen prompts using [the measurement plan](learning-system.md). New Repair cards should come from recurring personal errors, with one error per card and a fresh transfer cue. No bulk card generation is planned.
