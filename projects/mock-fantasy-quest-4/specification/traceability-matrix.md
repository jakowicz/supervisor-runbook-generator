# Requirements traceability matrix

`IMP-*` and implementation-runbook IDs are intentionally **unassigned**: F012 owns that allocation. “Planned evidence” names the eventual independently reviewable evidence; it is not current implementation proof.

| Requirements | Journeys | Components / contracts | Planned implementation IDs | Final evidence |
| --- | --- | --- | --- | --- |
| REQ-0001–0002, REQ-0008 | J1–J3 | content/campaign/scene; FDN-05, FEX-02,03,13 | DM-03,04,08,11,14; IMP unassigned | content validation, reachability, provenance review, playthrough |
| REQ-0003 | J2 | combat/rewards; FDN-05, FEX-04 | DM-09,14; IMP unassigned | deterministic combat and browser journey |
| REQ-0004 | J4 | inventory/party/rewards; FEX-05 | DM-10,14; IMP unassigned | inventory fixtures and UI journey |
| REQ-0005 | J1–J2 | tutorial/shell; FEX-01,04 | DM-08,13,14; IMP unassigned | tutorial first-battle/save evidence |
| REQ-0006, NFR-0002–0003 | J5 | save/session/recovery; FDN-06, FEX-10,11, QOR-04 | DM-05,06,07,12; IMP unassigned | atomic/fault/migration/quarantine tests |
| REQ-0007, NFR-0004–0005 | J1,J6 | shell/input/settings/a11y; FDN-04, FEX-06–09 | DM-13,15,16; IMP unassigned | accessibility scans, focused browser/manual evidence |
| REQ-0009–0010, NFR-0010 | J1,J6 | responsive shell/input adapters; FDN-03, FEX-06,07 | DM-13,15,16; IMP unassigned | input unit + responsive browser matrix |
| REQ-0011, NFR-0001, NFR-0011 | J7 | PWA/cache/release; FEX-12,14, QOR-04–05,08 | DM-17–20; IMP unassigned | offline/update/cache/rollback evidence |
| REQ-0012, NFR-0006 | J5,J7 | recovery/diagnostics; FDN-06, FEX-11, QOR-02–04 | DM-07,12,18–20; IMP unassigned | injected-error, consent/redaction evidence |
| NFR-0007 | J2–J5 | content validator; FDN-05, FEX-13 | DM-03,04; IMP unassigned | invalid-reference/reachability suite |
| NFR-0008 | J1–J7 | content/assets/release; FEX-09,13, QOR-06 | DM-04,18,20; IMP unassigned | provenance manifest + human review |
| NFR-0009, NFR-0012 | J1,J7 | quality/release controls; FDN-01–03, QOR-01,05–08 | DM-01,18–20; IMP unassigned | approved-matrix reports, gate records |
| REQ-0013–0015 | none (not P0) | exclusion seams; FDN-07,08, QOR-01 | no P0 runbook; IMP unassigned | decision/gate audit; approved future contract only |

All rows trace at least one requirement. A later author must replace `IMP unassigned` only by adding immutable IDs; they must not renumber REQ/NFR IDs or mark planned evidence as passed.
