# Question-card and QB-A catalogue bible

**Scope:** accepted design evidence for `GAME-001`, `GAME-002`, and
`GPI-001`–`GPI-005`. It defines a finite editorial package, not a claim that
the cards below are published game content. A runtime package may contain only
the records that pass the release gate in this document.

## Release boundary and original-expression rule

`QB-A` ("Kickoff Mix") is exactly the 48 stable IDs `QB-A-01` through
`QB-A-48`, divided into four named 12-card batches. The IDs are permanent:
a correction increments the revision and preserves the ID; a withdrawn card is
not silently replaced. No other `QB-A-*` ID is in the first release.

The catalogue's question intents and canonical answers below are authored for
this game. At production, the copy editor writes a fresh, concise prompt and
explanation from the stated facts; authors must not reproduce source wording,
answer-option sets, headlines, tables, or any reference-product expression.
The declared sources verify facts only and grant no permission to copy their
expression. A content record with uncertain source permission, attribution, or
rights is `blocked`, never published.

## `GPI-001`: card grammar and release record

Every field below is required unless its condition says otherwise. Player text
is localisable by key; answer matching uses canonical IDs and configured answer
rules (the detailed normalisation policy is owned by `GPI-006`).

| Field | Rule / purpose |
| --- | --- |
| `id`, `revision`, `batchId`, `status` | Stable ID, positive revision, one named batch, and lifecycle: `draft → fact_checked → accessibility_edited → second_reviewed → published`; alternatively `blocked` or `withdrawn`. Only `published` is eligible. |
| `originalityRecord` | Author ID/creation date, independently-authored confirmation, and a non-copying check. It records inspiration boundaries, never reference-product text. |
| `promptKey`, `promptText`, `instructionKey` | One independently written, single-fact prompt plus a format-appropriate, plain-language instruction. Prompt text must be answerable without an image, sound, colour, time limit, or unstated context. |
| `format` | Exactly one of `four_option_select`, `true_false`, `ordered_pair`, or `short_typed_answer`. |
| `category`, `topic`, `era`, `competitionScopes`, `clubIds`, `difficultyBand`, `tags` | Discovery and quota fields. `difficultyBand` is integer 1–3; all material competition/club references must be listed to enforce caps. |
| `answerOptions` | Required only for select/true-false. Select has exactly four unique option IDs and one `correct`; true/false has canonical `true`/`false` IDs. Options are text-labelled and have non-colour selection/result states. |
| `canonicalAnswer` and `acceptedAnswerRule` | Select/true-false use canonical option IDs; ordered pair specifies exactly two ordered canonical IDs; typed answer provides canonical display answer, normalised accepted aliases, and no fuzzy match. Empty aliases and aliases that could mean another answer are invalid. |
| `explanationKey`, `explanationText` | Short fact-first explanation shown after resolution, including canonical answer where useful. It must explain why rather than merely say "correct". |
| `accessibility` | `screenReaderPrompt`, `screenReaderOptions` where applicable, `answerStateText`, `explanationTextEquivalent`, reading-order/focus requirement, and text-size/contrast review. No visual or audio-only clue may be needed. |
| `provenanceId`, `factualAssertions[]` | Links each assertion to permitted durable sources/research records, source locator, checked date, and conflict/correction history. All assertions must be supported. |
| `reviews[]` | Two distinct completed reviews: factual/rights review and accessibility/copy review. Each carries reviewer ID/role, decision, date, findings, and revision reviewed. |
| `localeKeys`, `createdAt`, `updatedAt`, `withdrawal` | Externalised player strings and audit timestamps. Withdrawal requires reason, effective date, and replacement relationship only when one exists. |

**Format accessibility rules.** Four-option select renders every option as a
labelled button and never uses position as the only clue. True/false spells out
both values. Ordered pair labels first/second positions and supports reorder by
keyboard and touch. Typed answer announces validation requirements, preserves
entered text on rejected submission, and always exposes the canonical answer
and explanation after resolution. Every format supports touch, pointer,
keyboard, and gamepad-equivalent selection; no format relies on a timer.

## Provenance and two-review workflow

Each inventory row references a source family below; the eventual card's
`provenanceId` is `PROV-<card ID>` and must contain the precise page/document
URL, retrieval date, factual-assertion mapping, and correction log before it
can leave `draft`. The source family is a research route, not a substituted
source record.

| Key | Permitted durable primary route |
| --- | --- |
| `FIFA` | FIFA competition archives, match reports, and official records |
| `UEFA` | UEFA competition archives and official match reports/records |
| `CONMEBOL` | CONMEBOL tournament archives and official records |
| `AFC` | Asian Football Confederation tournament archives and official records |
| `PL` | Premier League official history, match, and competition records |
| `LALIGA` | LALIGA official history, match, and competition records |
| `SERIEA` | Lega Serie A official history, match, and competition records |
| `DFL` / `LFP` | DFL Bundesliga and Ligue de Football Professionnel official history/competition records |
| `FF` | France Football's official Ballon d'Or records |
| `CLUB` | The relevant club's official history/records page, cross-checked against its competition organiser where the assertion concerns a competition |

For each card revision, reviewer `R1` (factual/rights editor) verifies every
assertion against the exact provenance locator, source permission and original
expression record. Reviewer `R2` (accessibility/copy editor), a different
person, verifies unambiguous language, answer options/aliases, explanation,
screen-reader text, non-colour state wording, and localisation keys. R1's
accepted decision moves the record to `fact_checked`; R2's accepted decision
moves it to `second_reviewed`; only the release editor may then set
`published`. A rejection or later dispute sets `blocked`; a published error
sets `withdrawn` until both reviews approve a new revision. Reviewer identity,
date, revision, decision, and finding are mandatory, making absent or duplicate
reviews mechanically rejectable.

## `GPI-002`–`GPI-005`: bounded batch inventory

Legend: `FO` = four-option select; `TF` = true/false; `OP` = ordered pair;
`TA` = short typed answer. Each row is a required future card record with
`status: draft`, `revision: 1`, `provenanceId: PROV-<ID>`, and two pending
review records; this evidence does not falsely mark research as completed.
The “fact intent / canonical answer” is the editorial fact to verify, not
player-facing copy.

### `GPI-002` — QB-A World Tournament History (`QB-A-WORLD-01`)

| ID | Format | Band | Topic / fact intent / canonical answer | Scope | Source |
| --- | --- | --- | --- | --- | --- |
| QB-A-01 | FO | 1 | 2018 FIFA World Cup winner — France | FIFA World Cup | FIFA |
| QB-A-02 | TF | 1 | 1966 FIFA World Cup host — England | FIFA World Cup | FIFA |
| QB-A-03 | OP | 1 | Order 2008 and 2016 UEFA European champions — Spain, Portugal | UEFA European Championship | UEFA |
| QB-A-04 | TA | 1 | 2021 Copa América winner — Argentina | Copa América | CONMEBOL |
| QB-A-05 | FO | 2 | 1998 FIFA World Cup final venue — Stade de France | FIFA World Cup | FIFA |
| QB-A-06 | TF | 2 | Japan won the 2011 AFC Asian Cup — true | AFC Asian Cup | AFC |
| QB-A-07 | OP | 2 | Order 2011 and 2015 AFC Asian Cup winners — Japan, Australia | AFC Asian Cup | AFC |
| QB-A-08 | TA | 2 | 2004 UEFA European Championship winner — Greece | UEFA European Championship | UEFA |
| QB-A-09 | FO | 3 | 2019 AFC Asian Cup winner — Qatar | AFC Asian Cup | AFC |
| QB-A-10 | TF | 3 | The 2007 Copa América final was Argentina v Brazil — true | Copa América | CONMEBOL |
| QB-A-11 | OP | 3 | Order 1984 and 2000 UEFA European champions — France, France | UEFA European Championship | UEFA |
| QB-A-12 | TA | 3 | 1991 Copa América winner — Argentina | Copa América | CONMEBOL |

### `GPI-003` — QB-A Domestic League Moments (`QB-A-DOMESTIC-01`)

| ID | Format | Band | Topic / fact intent / canonical answer | Scope | Source |
| --- | --- | --- | --- | --- | --- |
| QB-A-13 | FO | 1 | 2015–16 Bundesliga champion — Bayern Munich | Bundesliga | DFL |
| QB-A-14 | TF | 1 | Real Madrid won 2023–24 LALIGA — true | LALIGA | LALIGA |
| QB-A-15 | OP | 1 | Order 2019–20 and 2020–21 Serie A champions — Juventus, Internazionale | Serie A | SERIEA |
| QB-A-16 | TA | 1 | 2022–23 Ligue 1 champion — Paris Saint-Germain | Ligue 1 | LFP |
| QB-A-17 | FO | 2 | Premier League’s first champion (1992–93) — Manchester United | Premier League | PL |
| QB-A-18 | TF | 2 | Athletic Club won 2023–24 Copa del Rey — true | LALIGA | LALIGA |
| QB-A-19 | OP | 2 | Order 1999–2000 and 2000–01 Serie A champions — Lazio, Roma | Serie A | SERIEA |
| QB-A-20 | TA | 2 | 2003–04 Premier League unbeaten champions — Arsenal | Premier League | PL |
| QB-A-21 | FO | 3 | 2023–24 LALIGA Pichichi winner — Artem Dovbyk | LALIGA | LALIGA |
| QB-A-22 | TF | 3 | Napoli won 2022–23 Serie A — true | Serie A | SERIEA |
| QB-A-23 | OP | 3 | Order 2011–12 and 2013–14 Bundesliga champions — Bayern Munich, Bayern Munich | Bundesliga | DFL |
| QB-A-24 | TA | 3 | 2009–10 Serie A champions — Internazionale | Serie A | SERIEA |

### `GPI-004` — QB-A Club, Manager, and Identity (`QB-A-CLUB-01`)

| ID | Format | Band | Topic / fact intent / canonical answer | Scope / club | Source |
| --- | --- | --- | --- | --- | --- |
| QB-A-25 | FO | 1 | Liverpool’s home stadium — Anfield | Liverpool | CLUB |
| QB-A-26 | TF | 1 | FC Barcelona’s home stadium is Camp Nou — true | Barcelona | CLUB |
| QB-A-27 | OP | 1 | Order AC Milan's 1999 and 2004 Serie A titles — 1999, 2004 | AC Milan / Serie A | CLUB + SERIEA |
| QB-A-28 | TA | 1 | Liverpool manager for the 2019 UEFA Champions League win — Jürgen Klopp | Liverpool / UEFA Champions League | CLUB + UEFA |
| QB-A-29 | FO | 2 | Barcelona manager for 2008–09 UEFA Champions League win — Pep Guardiola | Barcelona / UEFA Champions League | CLUB + UEFA |
| QB-A-30 | TF | 2 | AC Milan won the 1994 UEFA Champions League final — true | AC Milan / UEFA Champions League | CLUB + UEFA |
| QB-A-31 | OP | 2 | Order Liverpool's English top-flight titles in 1990 and 2020 — 1990, 2020 | Liverpool / English top flight | CLUB |
| QB-A-32 | TA | 2 | AC Milan's home stadium — San Siro | AC Milan | CLUB |
| QB-A-33 | FO | 3 | Barcelona’s 1992 European Cup final venue — Wembley Stadium | Barcelona / European Cup | CLUB + UEFA |
| QB-A-34 | TF | 3 | Liverpool won the 2005 UEFA Champions League final — true | Liverpool / UEFA Champions League | CLUB + UEFA |
| QB-A-35 | OP | 3 | Order Barcelona’s 2009 and 2011 UEFA Champions League wins — 2009, 2011 | Barcelona / UEFA Champions League | CLUB + UEFA |
| QB-A-36 | TA | 3 | AC Milan manager for the 2004 Serie A title — Carlo Ancelotti | AC Milan / Serie A | CLUB + SERIEA |

### `GPI-005` — QB-A Players and Records (`QB-A-PLAYER-01`)

| ID | Format | Band | Topic / fact intent / canonical answer | Scope | Source |
| --- | --- | --- | --- | --- | --- |
| QB-A-37 | FO | 1 | 2022 FIFA World Cup Golden Boot winner — Kylian Mbappé | FIFA World Cup | FIFA |
| QB-A-38 | TF | 1 | Cristiano Ronaldo is Portugal men's most-capped player — true | Portugal national team | FIFA |
| QB-A-39 | OP | 1 | Order Lionel Messi's 2009 and 2010 Ballon d'Or wins — 2009, 2010 | Ballon d'Or | FF |
| QB-A-40 | TA | 1 | Premier League all-time top scorer (as official record) — Alan Shearer | Premier League | PL |
| QB-A-41 | FO | 2 | 2018 FIFA World Cup Golden Ball winner — Luka Modrić | FIFA World Cup | FIFA |
| QB-A-42 | TF | 2 | Lionel Messi won The Best FIFA Men's Player award for 2022 — true | The Best FIFA Football Awards | FIFA |
| QB-A-43 | OP | 2 | Order Mohamed Salah's Premier League Golden Boots in 2018 and 2019 — 2018, 2019 | Premier League | PL |
| QB-A-44 | TA | 2 | 2019–20 Premier League Golden Boot co-winner — Pierre-Emerick Aubameyang | Premier League | PL |
| QB-A-45 | FO | 3 | 2006 FIFA World Cup Golden Boot winner — Miroslav Klose | FIFA World Cup | FIFA |
| QB-A-46 | TF | 3 | Robert Lewandowski won The Best FIFA Men's Player award for 2020 — true | The Best FIFA Football Awards | FIFA |
| QB-A-47 | OP | 3 | Order the 2018 and 2019 Ballon d'Or winners — Luka Modrić, Lionel Messi | Ballon d'Or | FF |
| QB-A-48 | TA | 3 | Premier League single-season goal record holder (38-match season) — Erling Haaland | Premier League | PL |

## Mechanical release checks

## GD0002 editorial acceptance register

[`qba-editorial-acceptance-register.json`](qba-editorial-acceptance-register.json)
is the durable, machine-readable ledger for all existing `QB-A-01`–`QB-A-48`
revision-1 records. It intentionally records no fictional acceptance: every
record is individually listed with its existing batch and source-family route,
and inherits five explicit pending reasons for un-authored original expression,
missing resolvable provenance, each distinct review, and the incomplete release
transition. Its `selectionEligible: false` default is a hard audit assertion,
not a future promise; a selector must reject every record until current-revision
evidence replaces every pending item and the lifecycle reaches `published`.

The register's `batches`, `records`, and `validation` fields make the finite
boundary inspectable without changing it: exactly four named batches, exactly
12 IDs in each, exactly 48 unique IDs matching `QB-A-01…48`, and no extra
record. A future editor must add card-specific evidence rather than changing a
default or accepting the manifest; a blocked, rejected, conflicted, withdrawn,
or still-pending revision remains `selectionEligible: false` with its reason.

The editorial validator must derive, rather than trust, the following report
from published card records and their provenance/review records:

| Check | Required result |
| --- | --- |
| ID/boundary | Exactly 48 unique IDs, exactly `QB-A-01…48`, exactly four named batches of 12; no extra QB-A card. |
| Category | World tournament history, domestic league moments, club/manager/identity, and players/records each equal 12. |
| Difficulty | Each category contains exactly four band-1, four band-2, and four band-3 cards. |
| Format | Each named batch contains exactly three FO, three TF, three OP, and three TA cards; therefore the release has 12 of each format. |
| Competition | No `competitionScopes` value appears on more than six cards: the declared maximums are FIFA World Cup 6, UEFA European Championship 3, Copa América 3, AFC Asian Cup 3, Premier League 6, LALIGA 4, Serie A 6, UEFA Champions League 6, and Ballon d'Or 2. |
| Club | No `clubIds` value appears on more than four cards: Liverpool, Barcelona, and AC Milan each appear four times; other cards have no club quota participant. |
| Eligibility | Every card is `published`, has all grammar fields, a resolvable provenance record with a checked date, no unresolved conflict, two distinct accepted reviews of its current revision, and no withdrawal. |
| Originality/accessibility | Every card has accepted originality and accessibility/copy review findings, required text equivalents, and no player-facing copied/source text. |

The sample inventory intentionally remains `draft` until per-card research and
review are completed. Thus it is bounded and independently auditable now, while
the validator will correctly reject it as a shippable package until its
provenance and both reviews are supplied.
