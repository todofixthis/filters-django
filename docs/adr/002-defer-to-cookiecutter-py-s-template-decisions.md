---
status: Accepted
date: 2026-11-20
scope: [.agents/rules/template-owned.md, .claude/settings.json, .copier-answers.yml, .github/workflows/build.yml, AGENTS.md, docs/adr/, pyproject.toml, renovate.json]
summary: This project follows the copier template todofixthis/cookiecutter-py, which writes and owns the files that .agents/rules/template-owned.md lists, and defers to its decisions in them; restating ADR 001, ADR tooling relies on the phx plugin (its hooks in sessions, phx-adr in CI), not a repo-local generator, pre-commit hook or vendored copy, with CI and AGENTS.md each pinning a phx-claude-siat release's commit SHA with a trailing `# X.Y.Z`, bumped together by Renovate as cookiecutter-py ADR 018 decides, not AGENTS.md reading the pin from the adrs job; diverging from a template decision on purpose needs an ADR here naming the cookiecutter-py ADR it departs from.
revisit-when: This project stops taking template updates; a cookiecutter-py ADR decides reliance on the phx plugin; a template release changes AGENTS.md's ADR-tooling instruction, the adrs job or its phx Renovate manager without an ADR; the template supersedes or renumbers one of the ADRs named here; a phx plugin release imposes an ADR convention the maintainer rejects; ADRs here are regularly authored outside a Claude Code session with the plugin; plugin releases routinely outrun the pin and leave CI red; the phx plugin drops its ADR tooling or its `phx-adr` entry point; phx's `main` stops carrying only releases.
---

# 002: Defer to cookiecutter-py's Template Decisions

## Context

This project now takes its tooling from [cookiecutter-py's copier template][],
recorded in `.copier-answers.yml`; each template release arrives as a Renovate
PR running `copier update` ([cookiecutter-py ADR 015][]). The files copier
writes are template-owned: `.agents/rules/template-owned.md` lists them and
says how to change one, and is itself written by the template.

[001-rely-on-the-phx-plugin-for-adr-tooling.md][] decided to rely on the phx
plugin for ADR tooling, with CI's `phx-adr` pinned to a release's commit, and
says `AGENTS.md`'s commands read that ref from the `adrs` job rather than
repeat it, with the version in a comment above the pin for a `git-tags`
Renovate manager. The template's `adrs` job and AGENTS.md, both
template-owned, each pin the same kind of commit with a trailing `# X.Y.Z`,
and AGENTS.md links the skill at the release's tag; one `github-tags` manager
in the template's `renovate.json` bumps them together
([cookiecutter-py ADR 018][]). So 001's decision stands, but its claim about
AGENTS.md no longer holds in files the template now owns.

No template ADR decides 001's core, relying on the phx plugin rather than a
repo-local or vendored tool, though the template's AGENTS.md carries it as an
instruction. The template's `build.yml` comment says its ADR 009 forbids a
repo-local copy of the tool, but neither 009 nor 018, which superseded it,
decides that. Sessions install the plugin from phx's `main`; only CI's pin
follows release tags.

## Options

### Option 1: Do nothing

**Pros:** No change to the record.
**Cons:** ADR 001 describes a pin layout the files no longer use. A reader
restoring it (AGENTS.md reading the job's ref, the comment above the pin)
conflicts with the next template update touching those lines, where the
template-owned rule takes the template's side.

### Option 2: One ADR deferring to the template and restating 001's core (Accepted)

Supersede 001 with this ADR, which keeps its reliance on the phx plugin and
hands the pin's layout to cookiecutter-py ADR 018.

**Cons:** A reader follows a link to another repository for the pin's
reasoning. This ADR names template ADRs by number, which goes stale if the
template supersedes or renumbers one; the links pin the 1.3.1 tag, so they
still lead to the decision this project adopted. When a template ADR decides
plugin reliance, half of this ADR gives way while the deferral stands.

### Option 3: Two ADRs, as class-registry has

Supersede 001 with a narrow ADR on plugin reliance and the pin, and record the
deferral in a separate ADR, split as todofixthis/class-registry's ADRs 007 and
008 are.

**Pros:** A template ADR on plugin reliance would supersede one ADR cleanly.
**Cons:** Two ADRs for one adoption, where filters-django has no other ADRs
for a deferral to supersede.

### Option 4: Keep 001's pin layout and diverge from the template

Keep AGENTS.md reading the pin from the `adrs` job and the `git-tags` manager,
with an ADR naming cookiecutter-py ADR 018 as the decision it departs from.

**Pros:** One copy of the pin, where the template keeps several.
**Cons:** Every template change to AGENTS.md's commands, the `adrs` job or the
Renovate manager conflicts here, to keep a layout the template chose against
for every library and nothing about filters-django needs.

## Decision

Option 2. The template owns these files, so it owns the decisions about them;
a second copy here can only fall behind. The template repeats the pin in
AGENTS.md; keeping 001's single copy would cost a conflict on every template
update touching those lines, for no gain specific to filters-django. A
single ADR suits a project whose only overlap with the template is 001.

Unlike class-registry's ADR 007, which stayed in force beside its deferral,
001 says something about AGENTS.md that the template's files contradict, so
it is restated and superseded rather than kept.

001's core stands, in this ADR's summary: ADR tooling is the phx plugin's,
never a repo-local generator, pre-commit hook or vendored copy. 001's Options
still give the reasons against each of those, and stand: this ADR changes
only the pin's layout. The template
implements that core in AGENTS.md without an ADR recording it, so this ADR
holds the record until a template ADR does.

## Consequences

- `.agents/rules/template-owned.md` decides whether a change to a
  template-owned file is made here or proposed to cookiecutter-py; that rule,
  not this ADR's `scope`, lists the files.
- Diverging from a template decision on purpose needs its own ADR here,
  naming the template ADR it departs from.
- Between a plugin release and Renovate's bump, sessions run a newer
  `phx-adr` than CI; AGENTS.md says how to reconcile them. That gap stays
  small only while phx's `main` carries only releases.

[001-rely-on-the-phx-plugin-for-adr-tooling.md]: 001-rely-on-the-phx-plugin-for-adr-tooling.md
[cookiecutter-py ADR 018]: https://github.com/todofixthis/cookiecutter-py/blob/1.3.1/docs/adr/018-require-gate-everywhere-and-the-release-check-on-main.md
[cookiecutter-py ADR 015]: https://github.com/todofixthis/cookiecutter-py/blob/1.3.1/docs/adr/015-propagate-template-changes-with-copier-and-rotate-python-from-agent-sessions.md
[cookiecutter-py's copier template]: https://github.com/todofixthis/cookiecutter-py
