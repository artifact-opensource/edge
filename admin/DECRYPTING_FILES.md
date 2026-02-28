# Decrypting Encrypted Files (Team Quick Guide)

! **Important:** Only authorized personnel should access the `SHIELD_PASSPHRASE`. Do not share passphrases in chat, email, or commit them to the repository.

## Where to get the passphrase
- Preferred: Retrieve from the authorized company secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, or GitHub Secrets).
- If necessary for emergency access: request it from the security owner (see team contact list) and rotate immediately after use.

## Quick decrypt steps (PowerShell)
1. Set the passphrase in your session (do NOT store in plain text):
   - $env:SHIELD_PASSPHRASE = Read-Host -AsSecureString | ConvertFrom-SecureString -AsPlainText
   - (Or retrieve directly from your secrets manager tooling and export to $env:SHIELD_PASSPHRASE)
2. Decrypt a file:
   - python scripts/shield/shield256.py decrypt path/to/file.md.enc
   - The tool will prompt for the passphrase if $env:SHIELD_PASSPHRASE is not set.
   - After decrypt: the file `file.md` will be restored and `file.md.enc` will be removed.

## Quick decrypt steps (bash)
1. Export passphrase (example - replace with vault retrieval):
   - export SHIELD_PASSPHRASE="$(vault read -field=value secret/artifact/shield-pass)"
2. Decrypt:
   - python3 scripts/shield/shield256.py decrypt path/to/file.md.enc

## Verifying decryption
- The `scripts/shield/verify_sample_decrypt.py` script can be used to verify a collection of .enc files decrypt correctly using the passphrase.
  - Usage: `python scripts/shield/verify_sample_decrypt.py <passphrase>` or `export SHIELD_PASSPHRASE=...` then run without args.

## Operational notes
- Rotate the passphrase after any incident or when a user with access leaves the team.
- Keep backups from `~/.artifact_shield/backups` available to security and compliance for recovery.
- If this repo was force-pushed (history rewrite), coordinate with the team before pulling: team members should run `git fetch origin` and then either `git reset --hard origin/main` (if they can discard local changes) or rebase safely if they have work to keep.

## Contacts
- Security owner: see `enterprise/divisions/departments/security/` for contacts and escalation procedures.

---
*This file is intentionally short; update it in `docs/DECRYPTING_FILES.md` if your team requires additional platform-specific steps.*