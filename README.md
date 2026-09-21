# The Unofficial Guide

**Corpus:** `campus_life` — 88 short posts about student life (dining, housing, courses, admin rules).

<!-- Add your name on this line. -->


> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:** posts of 350 characters or fewer stay whole; longer posts are cut into chunks of about 60–345 characters (average 189), never over 300 characters of body text. The cut points are topic boundaries, not a character count.
**Overlap:** 0. Every chunk instead repeats its post's title on the first line.

I read the `campus_life` posts in Milestone 1. Almost every one is a title plus one to three short paragraphs, and the useful fact sits in a single sentence ("Laundry costs $1.75 wash, $1.50 dry, card only."). The starter's fixed 800-character window therefore cut nothing: 88 documents became 88 chunks (317 characters on average). That is fine for a short post like `admin_dining_dollars.txt`, which is one thought. It is bad for the longer housing, course and dining posts (about 370–550 characters), which pack four or five separate topics into one chunk: layout, the good, the bad, laundry, noise. A question about laundry then only matches a fifth of the text.

So `split_documents` in [chunker.py](chunker.py) does three things:

1. **Short posts stay whole** (350 characters or fewer, `WHOLE_POST_LIMIT`). One post is already one thought, and cutting it would only remove context.
2. **Longer posts are cut where the topic changes.** A new chunk starts at a paragraph break, at a sentence that opens with a short lowercase label and a colon ("The good:", "On noise:", "Assessment:"), or at the dining posts' "The thing worth going for is..." and "The thing to know is...". A chunk over 300 characters is cut at a sentence end instead (`MAX_CHUNK_CHARS`), and one under 40 is joined to the next (`MIN_CHUNK_CHARS`).
3. **The title goes back on top of every chunk**, so "Laundry costs $1.75" still says which building it is about.

**Why overlap is 0:** overlap exists so a sentence isn't cut in half, but I cut only between sentences. Adjacent sentences in these posts are usually separate facts (laundry, then noise), so repeating the end of one chunk at the start of the next would drag a neighbouring topic in. The repeated title supplies the context overlap would have.

**I changed my mind twice.**
- My first version just packed sentences up to 200 characters. It looked reasonable but mixed topics: "The bad: ..." ended up in the same chunk as the laundry line. That is exactly what criterion 4 is meant to catch, so I made the boundaries follow the posts' own structure instead of a length.
- My second version treated any "words: text" as a label. That cut `transit_walking.txt` into one chunk per route, because "Fenwick Court to central campus: 18 minutes" matched. I now allow only lowercase words in a label, so proper nouns don't count.

**Known weak spot:** this is tuned to the way these posts are written. It relies on labels like "The good:" and would do little on posts without them. And a few chunks are short but complete: "Expect 8 to 10 hours a week outside class." is 66 characters with its title.

**Result:** 88 documents became 158 chunks (was 88), shortest 63, longest 345, average 189 characters (was 317). Producing function: `chunker.py::split_documents` (the original is kept as `chunker.py::fallback_split`).

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

A whole short post, left uncut (under 350 characters). One thought, stands alone.

**Chunk 2** — source: `course_cs_340.txt#2` — produced by: `chunker.py::split_documents`

```
CS 340 Databases

Expect 6 hours a week early, 15 in the last three weeks when the project lands.
```

Cut from `course_cs_340.txt` at a paragraph break. The title on top makes it stand alone as a workload answer.

**Chunk 3** — source: `course_phys_130_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

A whole short post (under 350 characters), from a separate workload file.

**Chunk 4** — source: `dining_verrill_street_grill.txt#2` — produced by: `chunker.py::split_documents`

```
Verrill Street Grill

The thing to know is that one register, so the queue is a single line no matter how busy.
```

Weakest of the five: the source sentence itself is clipped ("...is that one register"), and it is short. It is still one topic and names the place, but it is the kind of chunk I'd expect to answer a question badly.

**Chunk 5** — source: `housing_innisfree_hall.txt#4` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

Cut from `housing_innisfree_hall.txt` at the "On noise:" label. One topic, and the title says which building.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** How long is the wait at Kestrel Commons around lunchtime?

**Answer:**

```
  (best distance 0.180, cutoff 0.7)

Based on the documents, the wait time at Kestrel Commons is 20 to 25 minutes between 12:15 and 1:00, and under 5 minutes before 11:45.
Source: dining_kestrel_commons.txt (and dining_kestrel_commons_followup.txt)

Sources retrieved: dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt, dining_the_ridgeway_cafe_followup.txt
```

**My relevance cutoff:** 0.7 (`THRESHOLD` in [config.py](config.py)), up from the starter's 0.6.

I ran the five test questions from [questions.py](questions.py) and the five `OUT_OF_SCOPE` ones through retrieval and wrote down the best distance for each, using the new chunks. The two groups do not overlap and the gap is wide: everything the corpus covers is at 0.35 or below, and everything it doesn't is at 0.81 or above, so any cutoff between them passes all ten.

| Question | In corpus? | Best distance |
|---|---|---|
| How long does it take to walk from the library to the Ridgeway Café? | yes | 0.352 |
| How long is the wait at Kestrel Commons around lunchtime? | yes | 0.180 |
| How late in the semester can I declare a course pass/fail? | yes | 0.206 |
| Do my leftover dining dollars carry over from spring to the next autumn? | yes | 0.248 |
| How do I book a group study room? | yes | 0.279 |
| What is the capital of Mongolia? | no | 0.815 |
| How do I change the oil in a diesel engine? | no | 0.853 |
| Who won the 1994 World Cup? | no | 0.845 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.849 |
| How do I write a for loop in Rust? | no | 0.864 |

**Why 0.7 and not the midpoint of that gap (about 0.58).** Ten easy questions don't show where the risky zone is, so I also tried questions in between. Casually worded real questions got as far as 0.60 ("where can i study quietly" 0.599, "can i take a class pass fail" 0.435). Campus-sounding questions the corpus doesn't answer got 0.40 to 0.63 (campus bookstore hours 0.402, coffee shop 0.475, late-assignment policy 0.501, gym 0.515, parking ticket 0.629). Those two groups overlap, so no cutoff can separate them, and the gate can only stop clear misses. I chose 0.7 so a real question phrased loosely isn't refused (at 0.6 it sits on the edge), while staying well below the 0.81 where clearly off-topic questions start. The cost of 0.7 is that the near-misses reach the model, so the grounding instruction has to catch them.

**Grounding check.** I sent those five near-miss questions through the full pipeline at 0.7. The original instruction refused all of them with no invented facts, but the refusal wording varied and the coffee-shop reply added a tangential fact from the Ridgeway Café post. I tightened `GROUNDING_INSTRUCTION` in [generate.py](generate.py): refuse with the exact phrase "I don't have enough information about that", don't add related facts when refusing, and say which part is missing if only part is covered. Re-run, the gym and coffee-shop questions both returned that exact refusal. The off-topic Mongolia question is stopped by the gate and never reaches the model (0 model calls).

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
