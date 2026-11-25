---
status: Accepted
date: 2026-11-25
scope: [.agents/rules/template-owned.md, .claude/settings.json, .copier-answers.yml, .github/workflows/build.yml, AGENTS.md, docs/adr/, pyproject.toml, renovate.json]
summary: This project follows the copier template todofixthis/cookiecutter-py, which writes and owns the files that .agents/rules/template-owned.md lists, and defers to its decisions in them, ADR tooling included (the phx plugin, never a repo-local generator, vendored copy or pre-commit hook running ADR tooling, as cookiecutter-py ADR 019 decides, pinned as its ADR 018 decides), with no restatement of a template decision here; diverging from a template decision on purpose needs an ADR here naming the cookiecutter-py ADR it departs from.
revisit-when: This project stops taking template updates; the template supersedes or renumbers one of the ADRs named here; a condition in cookiecutter-py ADR 019's revisit-when arises in this project.
---

# 003: Defer to cookiecutter-py's Template Decisions, ADR Tooling Included

## Context

[002-defer-to-cookiecutter-py-s-template-decisions.md][] defers to
[cookiecutter-py's copier template][] in the files it owns, each release
arriving as a Renovate PR running `copier update`
([cookiecutter-py ADR 015][]), and restates
[001-rely-on-the-phx-plugin-for-adr-tooling.md][]'s reliance on the phx
plugin for ADR tooling, because no template ADR then decided it. Its `revisit-when`
names that gap: "a cookiecutter-py ADR decides reliance on the phx plugin".

Template release 1.3.2 added [cookiecutter-py ADR 019][], which decides it for
every generated project: the plugin's hooks in sessions and `phx-adr` at a pin
in CI and AGENTS.md, never a repo-local generator, vendored copy or pre-commit
hook running ADR tooling. This project records 1.6.0 in `.copier-answers.yml`,
and its AGENTS.md and `adrs` job comment already cite ADR 019 for that rule
and [cookiecutter-py ADR 018][] for the pin, and ADR 019's Consequences say
"filters-iso's 004 and filters-django's 002 can drop their restatements".
002's claims that no template ADR
decides the reliance and that the `adrs` job comment credits ADR 009 no longer
hold.

002's revisit conditions on the plugin are now the template's: ADR 019 names a
rejected convention, ADRs routinely authored outside a session, releases
outrunning the pin and the plugin dropping its ADR tooling; ADR 018 names the
plugin dropping `phx-adr` and phx-claude-siat's `main` taking non-release
commits.

## Options

### Option 1: Do nothing

**Pros:** No change to the record.
**Cons:** Two ADRs in force record one decision, with revisit conditions
already drifting apart: ADR 019 adds "sessions can install the plugin at the
pinned release", which 002 lacks. 002's Context makes claims the template's
files contradict.

### Option 2: Restate 002's deferral alone, superseding 002 (Accepted)

**Pros:** One copy of the ADR-tooling decision, in the template.
**Cons:** A reader follows links to another repository for every reason behind
the ADR tooling, where 002 carried its core here.

### Option 3: Discharge 002's trigger, keeping 002 in force

**Pros:** No new ADR.
**Cons:** 002's summary still restates 001, so the second copy stays in force
beside ADR 019, the drift Option 1 shows.

## Decision

Option 2. 002's own reason for deferring, that a second copy of a template
decision here can only fall behind, now applies to the restatement. A
discharge fits only where the older decision survives intact, and dropping the
restatement changes what 002 decides.

Kept from 002, as no template ADR decides them for this project: the deferral
itself, the rule that diverging on purpose needs an ADR here, and two revisit
conditions, this project leaving the template and the template superseding or
renumbering an ADR named here. The links pin the 1.6.0 tag, so they still lead
to the decisions adopted.

Dropped: the plugin conditions, which ADRs 018 and 019 hold, but for one
pointer to 019's, since some, such as ADRs authored outside a session, are
seen only from inside a project, whose index never shows the template's (018's
plugin condition, dropping `phx-adr`, falls under 019's "drops its ADR
tooling", and phx's `main` taking non-release commits shows in phx-claude-
siat, not in a project); and "a template release changes AGENTS.md's ADR-
tooling instruction, the `adrs` job or its phx Renovate manager without an
ADR", which watched for the template acting on a decision no ADR recorded; ADR
019 now records it. ADR 019 weighs 001's vendored copy and pinned pre-commit
hook for every generated project. 001's other rejected option, the plugin's
hooks with no CI check, has no template ADR weighing it: ADR 019 keeps the
`adrs` job in every option, and ADR 018 decides only how its pin moves. The
job lives in the template-owned `build.yml`, so dropping it would be the
template's change.

## Consequences

- `.agents/rules/template-owned.md` decides whether a change to a
  template-owned file is made here or proposed to cookiecutter-py; that rule,
  not this ADR's `scope`, lists the files.
- A reason to revisit ADR tooling, such as a condition from cookiecutter-py
  ADR 019's `revisit-when` seen here, goes to cookiecutter-py as a
  `docs/backlog/` item (its ADR 011), unless it is specific to filters-django,
  which needs its own ADR here naming ADR 018 or 019 as the decision it
  departs from.

[001-rely-on-the-phx-plugin-for-adr-tooling.md]: 001-rely-on-the-phx-plugin-for-adr-tooling.md
[002-defer-to-cookiecutter-py-s-template-decisions.md]: 002-defer-to-cookiecutter-py-s-template-decisions.md
[cookiecutter-py ADR 015]: https://github.com/todofixthis/cookiecutter-py/blob/1.6.0/docs/adr/015-propagate-template-changes-with-copier-and-rotate-python-from-agent-sessions.md
[cookiecutter-py ADR 018]: https://github.com/todofixthis/cookiecutter-py/blob/1.6.0/docs/adr/018-require-gate-everywhere-and-the-release-check-on-main.md
[cookiecutter-py ADR 019]: https://github.com/todofixthis/cookiecutter-py/blob/1.6.0/docs/adr/019-rely-on-the-phx-plugin-for-adr-tooling.md
[cookiecutter-py's copier template]: https://github.com/todofixthis/cookiecutter-py
