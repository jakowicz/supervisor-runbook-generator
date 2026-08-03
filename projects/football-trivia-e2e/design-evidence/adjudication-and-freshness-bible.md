# Adjudication and freshness bible

**Scope:** accepted evidence for `GAME-003`, `GAME-004`, `GPI-006`, and
`GPI-007`. This is a deterministic future-core contract, not implementation or
published content. A result is calculated only from stated input; it is never
inferred or guessed.

## GPI-006 — answer adjudication

Every resolved attempt is immutable and records `attemptId`, `cardId`,
`cardRevision`, `format`, submitted value, `outcome`, `reasonCode`,
canonical answer, and explanation key. Feedback reopening cannot recompute
against a later revision. A card withdrawn after presentation may resolve that
presented attempt; it cannot enter a new selection.

| Format | Comparison | Accept only when | Reject examples |
| --- | --- | --- | --- |
| `four_option_select` | Exact option ID | It equals the one correct option ID. | `blank`, `unknown_option_id`, `incorrect_option` |
| `true_false` | Exact canonical ID | It is exact `true` or `false` and correct. | `blank`, `malformed_boolean_id`, `incorrect_option` |
| `ordered_pair` | Exact two-item ordered ID array | It has two known IDs in configured order, including intentional repeats. | `blank`, `wrong_arity`, `unknown_option_id`, `wrong_order` |
| `short_typed_answer` | Normalised text vs. canonical display answer plus aliases | It equals one unique configured normalised value. | `blank`, `normalises_empty`, `unconfigured_variant`, `ambiguous_alias` |

A rejected submission always exposes canonical answer and explanation. A
configuration error (including duplicate normalised alias) makes the card
ineligible; it never accepts, guesses, or silently maps an answer.

### Typed-answer normalisation and aliases

Apply these steps, in order, to submitted text and every authored canonical
answer/alias when validating a card revision:

1. Convert input to Unicode NFC.
2. Apply Unicode default case folding (locale-independent).
3. Replace each Unicode whitespace sequence with one ASCII space and trim.
4. Decompose to Unicode NFD, remove combining marks, and recompose to NFC.
5. Remove only Unicode punctuation. Letters, numbers, and symbols remain; no
   transliteration, word substitution, reordering, stemming, phonetics,
   edit-distance threshold, AI, or fuzzy matching occurs.
6. Collapse whitespace again and trim. An empty key rejects as
   `normalises_empty`.

The key is comparison-only. An alias is accepted only if deliberately authored
for that revision, non-empty after normalisation, and unique in the card answer
domain. Validator failure rejects aliases colliding with another answer, another
alias/distractor, or multiple possible answers. Any canonical wording, alias, or
normalisation-version change creates a new revision, review, and validation; it
cannot change a resolved attempt.

Thus `Jürgen Klopp`, `JURGEN   KLOPP`, and `Jürgen-Klopp` share
`jurgen klopp`; `PSG` matches Paris Saint-Germain only if authored as an
alias. `M. Salah`, `Salahh`, or a missing first name never matches unless
explicitly configured and reviewed.

### Twenty deterministic adjudication fixtures

Each row specifies all material input. `C` is canonical value; braces contain
the complete alias set.

| ID | Format / configured answer | Submitted | Expected result |
| --- | --- | --- | --- |
| ADJ-01 | Select, C=`france` | `france` | accepted / `canonical_match` |
| ADJ-02 | Select, C=`france` | `argentina` | rejected / `incorrect_option` |
| ADJ-03 | Select, C=`france` | empty | rejected / `blank` |
| ADJ-04 | Select, C=`france` | `France` | rejected / `unknown_option_id` |
| ADJ-05 | Select, C=`france` | `fra` | rejected / `unknown_option_id` |
| ADJ-06 | True/false, C=`true` | `true` | accepted / `canonical_match` |
| ADJ-07 | True/false, C=`true` | `false` | rejected / `incorrect_option` |
| ADJ-08 | True/false, C=`false` | `True` | rejected / `malformed_boolean_id` |
| ADJ-09 | True/false, C=`true` | `yes` | rejected / `malformed_boolean_id` |
| ADJ-10 | True/false, C=`false` | empty | rejected / `blank` |
| ADJ-11 | Ordered pair, C=`[japan,australia]` | `[japan,australia]` | accepted / `ordered_match` |
| ADJ-12 | Ordered pair, C=`[japan,australia]` | `[australia,japan]` | rejected / `wrong_order` |
| ADJ-13 | Ordered pair, C=`[france,france]` | `[france,france]` | accepted / `ordered_match` |
| ADJ-14 | Ordered pair, C=`[japan,australia]` | `[japan]` | rejected / `wrong_arity` |
| ADJ-15 | Ordered pair, C=`[japan,australia]` | `[japan,qatar]` | rejected / `unknown_option_id` |
| ADJ-16 | Typed, C=`Jürgen Klopp`, aliases={`klopp`} | `  JURGEN---KLOPP ` | accepted / `normalised_canonical_match` |
| ADJ-17 | Typed, C=`Jürgen Klopp`, aliases={`klopp`} | `Klopp` | accepted / `normalised_alias_match` |
| ADJ-18 | Typed, C=`Jürgen Klopp`, aliases={`klopp`} | `Jurgen Klop` | rejected / `unconfigured_variant` |
| ADJ-19 | Typed, C=`Paris Saint-Germain`, aliases={`psg`} | `P.S.G.` | accepted / `normalised_alias_match` |
| ADJ-20 | Typed, invalid aliases={`inter`} for two answers | `Inter` | rejected / `ambiguous_alias`; ineligible card |

Whitespace-only typed input is `normalises_empty`. ADJ-20 is a failed
validation configuration, not releasable content: ambiguity is surfaced, never
guessed. An answer against `QB-A-28@r1` uses r1 values, never corrected r2.

## GPI-007 — reproducible editorial lifecycle

A transition input is `(cardId, currentRevision, event, evidenceRefs,
actorRole, occurredAt)`. It emits an append-only event and either next state or
validation failure. Time is recorded UTC and never supplies a missing
transition. A revision is immutable after leaving `draft`; correction creates
a successor revision under the same stable ID.

| Current state | Permitted event / required evidence | Next state | Eligible |
| --- | --- | --- | --- |
| `draft` | `submit_factual_check`: provenance, originality, accepted factual review | `fact_checked` | no |
| `fact_checked` | `accept_accessibility_copy`: different reviewer, accepted revision review | `accessibility_edited` | no |
| `accessibility_edited` | `accept_second_review`: distinct reviewer, grammar/alias validation | `second_reviewed` | no |
| `second_reviewed` | `publish`: release editor, all release checks pass | `published` | yes |
| pre-publication | `block`: dispute, missing rights, or validation failure | `blocked` | no |
| `published` | `withdraw`: reason, effective UTC time, evidence | `withdrawn` | no |
| `blocked` or `withdrawn` | `revise`: creates r+1 and preserves history/correction note | `draft` (r+1) | no |

No other transition is allowed: no direct draft-to-published, self-review, or
silent reopen. Each event records from-state, to-state, card/revision, event,
reason/evidence, actor ID/role, and UTC time. Replay from draft reproduces
state; invalid events remain rejected audit entries and change no state.

A reported conflict blocks an unpublished card or withdraws a published card
immediately. Withdrawal records `factual_correction`, `source_rights`,
`ambiguity`, or `accessibility_defect`, effective time, evidence, and an
optional replacement. It does not silently replace cards or rewrite past rounds.
New selection excludes it from that time; a presented attempt resolves against
its presented revision. Only a corrected, newly reviewed revision may publish.

## Seeded anti-repeat and shortage policy

For `(catalogueSnapshotId, seed, requestedCount, filter, ledger)`, freeze the
published eligible catalogue at the snapshot, apply filter, then remove
blocked/withdrawn cards. `recent` is the union of IDs in the two latest
*completed* rounds, sorting rounds by `(completedAtUtc, roundId)` descending.
Draft, abandoned, and in-progress rounds do not count.

Set `fresh = candidates − recent`. Assign each candidate
`SHA-256(seed + "|" + catalogueSnapshotId + "|" + cardId)`, then sort
ascending by `(key, cardId)`. Take the first
`min(requestedCount, fresh.length)`; fill only the remainder from
`reuse = candidates ∩ recent` in the same order. Whenever reuse occurs or
eligible cards are too few, record:

`{ requestedCount, freshAvailable, eligibleAvailable, reusedCardIds,
unfilledCount, disclosureKey: "selection_shortage_reuse_disclosed" }`.

Show this plain-language disclosure before round start whenever reuse or an
unfilled count exists. No clock, random source, network response, unpublished
card, or iteration order affects selection. Equal full input has equal IDs and
shortage record.

### Eight seeded selection fixtures

Candidate lists are frozen, filtered, and published; R1/R2 are newest completed
rounds. Implementation fixtures calculate the specified SHA-256 ordering and
assert selected IDs, shortage fields, and disclosure key.

| ID | Snapshot / seed / count | Candidates; R1; R2 | Expected result |
| --- | --- | --- | --- |
| SEL-01 | `S1` / `alpha` / 2 | A,B,C,D; A; B | selected `D,C`; no reuse/shortage |
| SEL-02 | `S1` / `alpha` / 3 | A,B,C,D; A; B | selected `D,C,B`; reused `B`; disclose |
| SEL-03 | `S1` / `beta` / 3 | A,B,C,D; A; B | selected `D,C,A`; reused `A`; disclose |
| SEL-04 | `S2` / `alpha` / 3 | A,B,C; A; B | selected `C,A,B`; reused `A,B`; disclose |
| SEL-05 | `S2` / `alpha` / 4 | A,B,C; A; B | selected `C,A,B`; `unfilledCount=1`; disclose |
| SEL-06 | `S3` / `gamma` / 2 | A,B; A; B | selected `A,B`; both reused; disclose |
| SEL-07 | `S4` / `delta` / 2 | A,B,C; A; R2 abandoned | selected `B,C`; no reuse |
| SEL-08 | `S5` / `epsilon` / 2 | A,B,C; A; B withdrawn | selected `C,A`; B excluded; disclose |

## Release checks

Eligibility requires published frozen-snapshot state, correct answer rule, no
alias collision, current provenance, two distinct accepted reviews, and no
effective withdrawal. The fixture suite requires exactly ADJ-01–ADJ-20 and
SEL-01–SEL-08. Failed validation blocks release; it cannot create a fallback
answer or undisclosed repeat.
