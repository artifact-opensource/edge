# Visualizer Server (example)

Lightweight Node.js static server to host `csv-visualizer.html` with optional Basic Auth.

Usage:
- set VIS_USER and VIS_PASS env vars for basic auth (recommended behind a reverse proxy with TLS)
- install: `npm ci`
- run: `npm start`

For production, deploy behind an SSO/OCID-enabled gateway (Auth0, Azure AD, Keycloak) or use an internal ingress that enforces authentication.
