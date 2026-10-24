"""Gatekeeper: signed, expiring tokens (HMAC-SHA256)."""
import hashlib
import hmac
import time


class Gatekeeper:
    def __init__(self, secret: bytes, ttl: int = 300):
        if not secret:
            raise ValueError("secret must not be empty")
        self._secret = secret
        self._ttl = ttl

    def _sign(self, subject: str, expires: int) -> str:
        msg = f"{subject}.{expires}".encode()
        return hmac.new(self._secret, msg, hashlib.sha256).hexdigest()

    def issue(self, subject: str, now: float | None = None) -> str:
        expires = int((now if now is not None else time.time()) + self._ttl)
        return f"{subject}.{expires}.{self._sign(subject, expires)}"

    def verify(self, token: str, now: float | None = None) -> bool:
        try:
            subject, expires, sig = token.rsplit(".", 2)
            expires_i = int(expires)
        except ValueError:
            return False
        if expires_i < (now if now is not None else time.time()):
            return False
        return hmac.compare_digest(sig, self._sign(subject, expires_i))
