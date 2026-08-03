# Runbook-generation quality gate

Run this after each B-series authoring wave:

```zsh
python3 projects/mock-fantasy-quest-4/planning/validate_runbook_generation.py
```

Use `--wave B0004` for a checkpoint through one batch. The validator reads the
canonical specification, catalogue, manifest, B writers, and generated R
contracts. It is structural evidence only: it does not build, test, review,
deploy, or release the product.

## Checks

- Unique, ordered B/R IDs; dependency closure/cycles; manifest output ownership;
  requirement links; and exact, canonical provenance links.
- Required R front matter (including `requirement_ids`) and matching manifest
  metadata, an explicit Asset assessment section, and verification ownership.
  Missing, duplicate, blocked, unverified, and unallocated IDs are printed with
  catalogue, manifest, and specification coverage counts.
- Explicit asset assessments. Asset-required work needs unique stable `ASSET-*`
  IDs, an asset brief, and a visual-style version; non-asset work may not reserve
  IDs or silently introduce asset work.
- Unique browser test paths and browser-impact metadata only for web/PWA
  behaviour. A web/PWA target alone does not require browser metadata.

The initial foundation wave correctly fails until B writers create their
reserved R files; that is a missing authoring artefact, not product failure.

## Recovery and human review

1. Rerun only the failed B writer using its manifest context packet; retain its
   B/R IDs and change only assigned R paths.
2. Repair a bounded R range through its owning B writer(s), then rerun this
   command through the final affected `--wave` value. Never regenerate accepted
   work or renumber IDs.
3. Checkpoint accepted work and resume the dispatcher at the manifest's first
   unaccepted B batch.

Stop for human review on gates, credentials, paid services, legal/compliance or
licensing decisions, device access, store/certification actions, deployment,
publishing, or release approval. Mark work blocked and retain IDs.
