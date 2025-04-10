# pre-commit-hooks
![example workflow][gh_badge]

Heavily opinionated [pre-commit][precommit] hooks I deem useful.

**Hooks**
| Hook ID | Description |
| ---- | ---- |
|`markdown-detect-nonref-links`|Detects non-ref [links][mdlinks] in Markdown|
|`rego-unsafe-boolean-comparison`|Detects unsafe boolean [comparison][regobool] in Rego. For fix, see [harness/][safebool]|
|`dockerfile-multiline-cmds`|Detects suboptimal use of multiline commands in Dockerfiles|
|`prevent-commit-to-default-branch`|Prevent commits to the default branch.|
|`prevent-returning-fastapi-httpexceptions`|Prevent returning FastAPI HTTPExceptions|

## Using pre-commit-hooks
Add this to your `.pre-commit-config.yaml`:
```yaml
- repo: https://github.com/p15r/pre-commit-hooks.git
  rev: v0.5.1
  hooks:
  - id: markdown-detect-nonref-links
  - id: rego-unsafe-boolean-comparison
  - id: dockerfile-multiline-cmds
  - id: prevent-commit-to-default-branch
  - id: prevent-returning-fastapi-httpexceptions
```
(run `pre-commit autoupdate` for latest hooks)

## Development
* Use the `try-repo` command for fast feedback loop:
```bash
cd dummyrepo/
pre-commit try-repo ../pre-commit-hooks/ --verbose
```
Make sure that `dummyrepo` contains at least one commit.

[gh_badge]: https://github.com/p15r/pre-commit-hooks/actions/workflows/check.yml/badge.svg
[precommit]: https://pre-commit.com/
[mdlinks]: https://daringfireball.net/projects/markdown/syntax#link
[regobool]: https://play.openpolicyagent.org/p/usNlKtMVlo
[safebool]: tests/harness/unsafe_boolean_comparison.rego
