## Getting Started

Before writing code, check:

- `docs/plans/` — current implementation plan
- `docs/adr/INDEX.md` — prior decisions (don't re-litigate)
- `docs/future/` — deferred features (don't re-discuss)

## Architecture Decision Records

When making significant decisions — choosing between libraries, patterns, tools, or conventions — you **must** write an ADR before implementing the decision. Use the `phx:writing-adrs` skill (from the phx plugin, which `.claude/settings.json` enables) for the format, conventions and tooling: its `adr.py` allocates the number, generates `docs/adr/INDEX.md` and validates the corpus. Where `phx:writing-adrs` is unavailable (another harness, or the plugin not installed), follow [its SKILL.md](https://github.com/todofixthis/phx-claude-siat/blob/0725567cec6bab6a227c2a3d569e64c226c33a4e/skills/writing-adrs/SKILL.md) and run the same tool as `phx-adr` (see Commands). Don't hand-edit the index or add a repo-local ADR script (ADR 001). ADRs live in `docs/adr/`.

If you find yourself about to establish a new cross-cutting pattern (something that will affect multiple domains or files, e.g. a testing convention, a shared utility, an error-handling approach), stop and write an ADR first even if the immediate task feels local. A pattern adopted once becomes the template for everything that follows.

## Commands

```bash
uv run autohooks activate --mode=pythonpath     # install pre-commit hook (once per clone)
uv run git commit                               # always use instead of git commit (runs autohooks)
uv add --bounds major <package>                 # add a runtime dependency at latest version
uv add --bounds major --group dev <package>     # add a dev dependency at latest version
uv run pytest                                   # run tests (current virtualenv)
uv run pytest test/app/test_model.py::test_name # single test
uv run tox -p                                   # test across all supported Python versions
```

The phx plugin's ADR tool, for use where the skill is unavailable (keep these refs in step with the `adrs` CI job):

```bash
# Scaffold the next ADR
uvx --from 'git+https://github.com/todofixthis/phx-claude-siat@0725567cec6bab6a227c2a3d569e64c226c33a4e#subdirectory=skills/writing-adrs' phx-adr new "Title" --summary "…" --scope path/
# Regenerate docs/adr/INDEX.md
uvx --from 'git+https://github.com/todofixthis/phx-claude-siat@0725567cec6bab6a227c2a3d569e64c226c33a4e#subdirectory=skills/writing-adrs' phx-adr index
# Validate, as CI does
uvx --from 'git+https://github.com/todofixthis/phx-claude-siat@0725567cec6bab6a227c2a3d569e64c226c33a4e#subdirectory=skills/writing-adrs' phx-adr check
```

If the `adrs` job reports the index stale right after a session regenerated it, the installed plugin has outrun the pin: bump every pinned ref (here, in the SKILL.md link and in the `adrs` job) to the installed release's commit (`<tag>^{commit}`; the version is in the plugin's `plugin.json`). Don't regenerate the index with the old pin.

## Architecture

Single-module library (`src/filters_django/__init__.py`) that extends [`phx-filters`](https://pypi.org/project/phx-filters/) with one class: `Model`.

`Model` is a `filters.BaseFilter` subclass that validates a value against a Django ORM query. Constructor args: `model` (required), `field` (default: `pk`), plus `**predicates` for arbitrary QuerySet method calls (`filter=`, `exclude=`, `select_related=`, etc.). Returns the matched instance or raises a validation error (`CODE_NOT_FOUND` / `CODE_NOT_UNIQUE`).

Registered as a `phx-filters` extension via the `filters.extensions` entry point, making it available as `filters.ext.Model`.

`test/` is a minimal Django app for testing only — in-memory SQLite, with a `Specie` model used throughout the test suite.

## Docstrings

Google/Napoleon format (`Args:`, `Returns:`, `Note:`) — not Sphinx `:param:` style. Max 80 chars per line. Escape backslashes (e.g. `'\\n'` not `'\n'`). Blank line before lists inside `Args:` sections to avoid Sphinx indentation warnings. ReadTheDocs treats all Sphinx warnings as errors — resolve them before pushing.

## Code Comments

Place comments on the line preceding the code they document, not as trailing comments.

## Language and Style

- Alphabetise `pyproject.toml` sections and keys within sections
- NZ English; incorporate Te Reo Māori where natural (e.g. "mahi", "kaupapa")
- Use "Initialises" not "Initializes"

### Writing for coding agents

- Do not document information that already exists in the coding agent's training data or could be easily discovered by reading the code.
- Do not list individual files; list high-level directories so the agent knows where to look.
- Aim for concise style that optimises token count without sacrificing clarity.

## Branches

- `main` — releases only; merge from `develop` via PR
- `develop` — main development branch
- Feature branches off `develop` for all new work

## Git Worktrees

Use `.claude/worktrees/` for isolated workspaces (project-local, gitignored).

After switching to a worktree, run the autohooks activate command (see Commands) to install the pre-commit hook for that worktree.

Keep `.claude/` a real directory — only `.claude/skills` is a symlink into `.agents/skills`. If `.claude` itself becomes a symlink, the native worktree tooling refuses to run.