# transstellar

A pytest framework

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
