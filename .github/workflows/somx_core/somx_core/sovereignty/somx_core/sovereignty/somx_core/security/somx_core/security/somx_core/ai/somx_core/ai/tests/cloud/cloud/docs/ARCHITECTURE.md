# SOMX-CORE Architecture

Request -> Gatekeeper (token) -> Sovereignty Policy -> Model Router -> Audit

- **security/**: signed expiring tokens (HMAC-SHA256)
- **sovereignty/**: allowed regions and models, deny by default
- **ai/**: model registry and routing, logs every decision
- **cloud/**: Cloudflare Worker gateway
