# Repository Policy (Enterprise)

This document contains operational policies for managing the repository.

## Access & Permissions
- Least privilege principle. Approvals required for admin-level changes.
- Use single sign-on and MFA.

## Secrets & Sensitive Data
- Secrets must never be committed. Use approved secret stores (1Password, AWS Secrets Manager, etc.).
- Use pre-commit hooks and secret scanning tools.

## Data Handling
- CSVs and data files must be accompanied by metadata in `docs/csv-manifest.json`.
- For sensitive/PII datasets, provide a redaction or encrypted alternative and document retention schedule.

## Incident Handling
- Report incidents following the `SECURITY.md` process.

## Enforcement
- Policy violations may lead to access revocation and HR/legal action."