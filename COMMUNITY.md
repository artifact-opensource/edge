# Git Community & Repository Governance (Enterprise)

This document codifies repository governance, branching strategy, commit and PR process, and security expectations for this private, proprietary repository.

## Purpose
- Provide a single source of truth for how to collaborate on source and data in this enterprise repo.
- Ensure code quality, compliance, and operational continuity.

## Repository Status
- Visibility: Private
- License: Proprietary (see `LICENSE.PROPRIETARY.md`)
- Branches: `main` is protected and always deployable. Feature branches follow `feature/<short-description>`.

## Branching Strategy
- Main: protected, CI passing, reviewed PRs only.
- Development/Integration branches: `develop` or `release/*` where appropriate.
- Feature branches: `feature/<issue>-<short>`
- Hotfix branches: `hotfix/<short>`

## Commits & Messages
- Use Conventional Commits (e.g., `feat:`, `fix:`, `chore:`, `docs:`, `perf:`).
- Include issue/PR reference when applicable: `fix: correct CSV parser (#123)`.
- No secrets or credentials in commits. Use secret store and rotate if leaked.

## Pull Requests & Reviews
- All PRs must have at least 1 approver and pass CI and static checks.
- Size limits: keep PRs small; >500 LOC require extra reviewer.
- Use descriptive titles and link related issues.

## CI/CD & Checks
- PRs must pass build, lint, unit tests, and security scans (SAST/secret scanning).
- Releases are tagged and signed by maintainers.

## Data Governance & CSVs
- Treat CSVs as first-class artifacts. Metadata must be documented (see `csv-manifest.json`).
- PII or regulated data must be redacted or access restricted; follow `SECURITY.md`.

## Security & Compliance
- Report vulnerabilities to `SECURITY.md` process.
- Secret scanning and policy enforcement are mandatory.

## Onboarding & Roles
- Define repository owners in `.github/CODEOWNERS`.
- Use `CONTRIBUTING.md` to onboard new contributors and set expectations.

---

For full contributor workflow and templates, see `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `REPO_POLICY.md`, and `.github/` templates.