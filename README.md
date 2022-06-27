# pre-commit-hooks
![example workflow][gh_badge]

Heavily opinionated [pre-commit][precommit] hooks I deem useful.

**Hooks**
| Hook ID | Description |
| ---- | ---- |
|`markdown-detect-nonref-links`|Detects non-ref [links][mdlinks] in Markdown|
|`rego-unsafe-boolean-comparison`|Detects unsafe boolean [comparison][regobool] in Rego. For fix, see [harness/][safebool]|

## Using pre-commit-hooks
Add this to your `.pre-commit-config.yaml`:
```yaml
- repo: https://github.com/p15r/pre-commit-hooks.git
  rev: v0.2.0
  hooks:
  - id: markdown-detect-nonref-links
  - id: rego-unsafe-boolean-comparison
```

[gh_badge]: https://github.com/p15r/pre-commit-hooks/actions/workflows/check.yml/badge.svg
[precommit]: https://pre-commit.com/
[mdlinks]: https://daringfireball.net/projects/markdown/syntax#link
[regobool]: https://play.openpolicyagent.org/p/usNlKtMVlo
[safebool]: tests/harness/unsafe_boolean_comparison.rego
