# Runaris SDLC Playbook (AI-native loop)

Principle: every stage commits an artifact the next stage reads. Humans own judgment calls; agents do the volume.

| Stage | Artifact | Agent does | Human decides | Gate |
|---|---|---|---|---|
| Plan | `intent.md` | Drafts from idea, challenges gaps | Scope, success metrics | Intent approved |
| Design | `specs/<feature>.md` | Requirements + design in one session | Data model, UX tradeoffs | Spec approved |
| Build | Branch + small diffs | Plan mode, implement, parallel subagents for independent parts | None routine | Tests green |
| Test | Eval results | Unit, property, render-perf, save/load round-trip evals | Thresholds | Evals pass |
| Deploy | PR + review findings | Agentic PR review, changelog | Data model, persistence, security changes | Hook gate + human sign-off on critical paths |
| Maintain | Metric report | Compares live metrics to control bands | Response to breach | Breach -> new `intent.md` entry |

## Evals (build first, cheap, continuous)
1. Save/load round-trip on fixture maps (0 loss)
2. Render benchmark at 100 / 1,000 / 5,000 nodes
3. Model invariants (no orphan edges, unique IDs, no cycles where forbidden)
4. Migration test: every old file version still opens

## Review tiers
- Agent review: all diffs
- Human review: data model, persistence, auth/sync, dependencies added

## Adoption sequence
1. Week 1: fill `intent.md` and `CLAUDE.md` [TBD]; run `/init`, trim result
2. Week 1: enable hook gate (`.claude/settings.json`)
3. Week 2: first feature through full loop using a `new-feature` spec template
4. Week 3: add evals 1-4 to CI
5. Ongoing: every agent mistake becomes a `CLAUDE.md` pitfall line

## Success of the playbook itself
Track: spec-to-merge lead time, review queue age, escaped defects, eval pass rate.
