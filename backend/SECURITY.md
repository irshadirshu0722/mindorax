# Security Policy

## Supported Scope

Security reports are welcome for the active codebase on the default branch.

## How To Report A Vulnerability

Please report vulnerabilities privately. Do not create a public issue for:

- authentication bypass
- token leakage
- account takeover
- exposed secrets
- remote code execution
- database or infrastructure misconfiguration

When reporting, include:

- a clear description of the issue
- impact assessment
- reproduction steps
- affected file paths or endpoints
- proof of concept if safe to share

## What Happens Next

Maintainers should:

1. acknowledge receipt
2. validate the issue
3. assess severity and impact
4. prepare a fix
5. coordinate disclosure when appropriate

## Current Security Notes

The current codebase contains hard-coded settings and secrets in Django settings. Those values should be rotated and moved to environment-based configuration before any real production deployment.
