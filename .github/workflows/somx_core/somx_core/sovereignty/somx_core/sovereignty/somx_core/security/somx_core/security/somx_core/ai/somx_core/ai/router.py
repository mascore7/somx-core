"""Multi-model router: every call passes token + sovereignty checks."""
from typing import Callable

from somx_core.security import Gatekeeper
from somx_core.sovereignty import SovereigntyPolicy


class AccessDenied(Exception):
    pass


class ModelRouter:
    def __init__(self, gatekeeper: Gatekeeper, policy: SovereigntyPolicy):
        self._gk = gatekeeper
        self._policy = policy
        self._models: dict[str, Callable[[str], str]] = {}
        self.audit: list[dict] = []

    def register(self, name: str, fn: Callable[[str], str]) -> None:
        self._models[name] = fn

    def route(self, token: str, region: str, model: str, prompt: str) -> str:
        ok = (
            self._gk.verify(token)
            and self._policy.check(region, model)
            and model in self._models
        )
        self.audit.append({"region": region, "model": model, "allowed": ok})
        if not ok:
            raise AccessDenied("request denied (fail-closed)")
        return self._models[model](prompt)
