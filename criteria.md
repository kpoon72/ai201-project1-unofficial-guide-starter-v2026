# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
Most of my questions have their answer in one short post, but the Kestrel Commons lunch-wait question has competition: there are two Kestrel posts and twelve more posts about the other six dining halls, most of which give wait times in almost the same words. I allow one miss because that one could plausibly slip, but not two, because with only 88 short chunks and five results per question, missing on most of them would mean retrieval itself is broken.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
This is all five, not four, because naming a source doesn't depend on retrieval luck: the grounding instruction already tells the model to name the file, and the starter prints a "Source:" line. If even one answer skips it, the prompt or the answer format is broken, not the data. (A refusal from the gate is not an answer, so it doesn't count against this.)

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->
I wrote this before measuring any distances, so the reason is a guess to check in Milestone 4. The five out-of-scope questions (Mongolia, diesel engines, the World Cup, ibuprofen, Rust) are about as far from student life as I can get, so I expect most to be far from every chunk. I allow one miss because the ibuprofen question could land near `health_center.txt`, and a miss on that would be a real overlap in the data rather than a broken gate.

---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

At least 4 of 5 chunks I read with `python app.py chunks -n 5` cover a single subject (for example laundry cost, or noise, but not both) and could answer a question without the rest of their post.

**Why this target:**
The starter kept each post whole, which is fine for short ones like `admin_dining_dollars.txt` but puts four topics in one chunk for the longer housing posts (Innisfree Hall and Old Brewhouse each cover layout, laundry cost, noise and heating together), so a laundry question only matches a quarter of that text. I picked 4 of 5, not 5 of 5, because a sample of five is small and one chunk that sits between two related facts shouldn't fail the whole strategy; I picked a plain count of five over a length limit because the shortest posts (about 180 characters) are already complete and a minimum length would wrongly count them as bad.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

For at least 4 of my 5 test questions, the source file named in the answer is a file that actually contains that question's `expects` phrase.

**Why this target:**
Criterion 2 only checks that a source is named, but this corpus has many near-duplicate posts (seven dining halls, seven housing halls, nine courses), so an answer can name a real file that is the wrong one. Naming the right file is what makes the answer checkable by a student, so I care about it more than the other criteria. I set it at 4 of 5 rather than 5 of 5 because the Kestrel Commons wait time also appears in `dining_kestrel_commons_followup.txt`, so a question can legitimately cite more than one file, and I don't want to fail a correct answer on that technicality.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
