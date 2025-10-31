# pre-commit-hooks
![example workflow][gh_badge]

Heavily opinionated [pre-commit][precommit] hooks I deem useful.

**Hooks**
| Hook ID | Description |
| ---- | ---- |
|`markdown-detect-nonref-links`|Detects non-ref [links][mdlinks] in Markdown|
|`rego-unsafe-boolean-comparison`|Detects unsafe boolean [comparison][regobool] in Rego. For fix, see [harness/][safebool]|
|`dockerfile-multiline-cmds`|Detects suboptimal use of multiline commands in Dockerfiles|
|`prevent-push-to-default-branch`|Prevent pushing to the default branch. Requires `pre-commit install -t pre-push` to install.|
|`prevent-returning-fastapi-httpexceptions`|Prevent returning FastAPI HTTPExceptions|

## Using pre-commit-hooks
Add this to your `.pre-commit-config.yaml`:
```yaml
repos:
- repo: https://github.com/p15r/pre-commit-hooks.git
  rev: v0.5.7
  hooks:
  - id: markdown-detect-nonref-links
  - id: rego-unsafe-boolean-comparison
  - id: dockerfile-multiline-cmds
    # Note: requires `pre-commit install -t pre-push` to install hook.
  - id: prevent-push-to-default-branch
  - id: prevent-returning-fastapi-httpexceptions
```
(run `pre-commit autoupdate` for latest hooks)

## Development
* Use the `try-repo` command for fast feedback loop:
```bash
cd dummyrepo/
# add `--hook-stage pre-push` to test `prevent-push-to-default-branch`
pre-commit try-repo ../pre-commit-hooks/ --verbose
```
Make sure that `dummyrepo` contains at least one commit.

### Create Release
* Bump package version in `pyproject.toml`
* Bump `rev` in readme
* Update lock file using `uv lock`
* Create new release on Github

[gh_badge]: https://github.com/p15r/pre-commit-hooks/actions/workflows/check.yml/badge.svg
[precommit]: https://pre-commit.com/
[mdlinks]: https://daringfireball.net/projects/markdown/syntax#link
[regobool]: https://play.openpolicyagent.org/p/usNlKtMVlo
[safebool]: tests/harness/unsafe_boolean_comparison.rego
