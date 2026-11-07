# Security

Two-factor authentication is required for the owner and admins of Business and Enterprise accounts, and recommended for everyone else. Larkspur supports authenticator apps and hardware security keys.

All data is encrypted at rest with AES-256 and in transit with TLS 1.2 or later. Backups and export archives are encrypted the same way.

API keys belong to a project, not to a person. A key can be limited to read-only access, and keys can be rotated from Settings, then API keys, without downtime: the old key keeps working for 24 hours after a new one is created.

Larkspur staff can open a customer server only when the customer grants access in a support ticket, and every such access is logged in the account audit log.

Report a suspected vulnerability to security@larkspur.example. Reports are acknowledged within one business day.
