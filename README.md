# pre-commit-hooks
![example workflow][gh_badge]

Heavily opinionated [pre-commit][precommit] hooks I deem useful.

**Hooks**
- `markdown-detect-nonref-links`: Detects non-ref [links][mdlinks] in Markdown

## Using pre-commit-hooks
Add this to your `.pre-commit-config.yaml`:
```yaml
- repo: https://github.com/p15r/pre-commit-hooks.git
  rev: v0.1.0
  hooks:
  - id: markdown-detect-nonref-links
```

[gh_badge]: https://github.com/p15r/pre-commit-hooks/actions/workflows/check.yml/badge.svg
[precommit]: https://pre-commit.com/
[mdlinks]: https://daringfireball.net/projects/markdown/syntax#link
