# transstellar

A pytest framework

## Prepare testing environment

1. Docker

2. Create a GitHub personal access token with permission to access transstellar and permission to read and write issue.

Update .env `GITHUB_PERSONAL_ACCESS_TOKEN` variable.


## How to publish to PyPI

1. Update PyPI Token. Open .env to update `POETRY_PYPI_TOKEN_PYPI` variable.

2. Create a new version and tag

  ```
  poetry version [major|minor|patch]
  git add -u; git commit -m 'chore: bump version to 1.2.3'
  git tag -a v1.2.3
  ```

3. Build & Publish

  ```
  poetry build
  poetry publish
  ```
