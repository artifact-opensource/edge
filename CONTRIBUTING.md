# Contributing to Artifact Virtual (Enterprise)

Thank you for contributing. This repository is **private and proprietary**—contributions must follow enterprise rules and approvals.

## Getting Started
- Forking: Not required for direct collaborators; create branches off `main` or `develop` as per the Branching Strategy.
- Install dev dependencies listed in per-project `package.json`/`requirements.txt`.

## Workflow
1. Create a feature branch: `feature/<short>`
2. Make focused commits using Conventional Commits.
3. Push and open a PR against `main`/`develop`.
4. Ensure CI passes and get required approvals.

## Testing & Linting
- Run unit tests and linters locally before opening PRs.
- Update tests for any functional change.

## Adding or Updating CSV Dashboards
- Place CSVs under `enterprise/departments/<department>/` with descriptive filenames.
- Add metadata entry to `docs/csv-manifest.json` if introducing a new CSV. Example entry:

```json
{ "id": "my_dashboard", "name": "My Dashboard", "path": "enterprise/departments/ops/MY_DASHBOARD.csv", "department": "operations", "sensitive": false }
```

- After adding a CSV or updating `docs/csv-manifest.json`, run the validation script locally to check headers and potential sensitive fields:

```bash
python scripts/validate_csvs.py
```

- Ensure no PII or secret values are committed. If data is sensitive, set `"sensitive": true` in the manifest and provide a redacted or encrypted export.


## Style & Documentation
- Keep docs up-to-date when changing data schemas or dashboards.
- Update `README.md` and internal docs for larger changes.

## Contact
- For policy questions, reach out to the repository owners listed in `.github/CODEOWNERS`.