"""Sovereignty policy: fail-closed by default."""
from dataclasses import dataclass


@dataclass(frozen=True)
class SovereigntyPolicy:
    allowed_regions: frozenset = frozenset({"SO", "KE", "DJ", "EG", "NG"})
    allowed_models: frozenset = frozenset()  # empty = deny all

    def check(self, region: str, model: str) -> bool:
        """Return True only if both region and model are explicitly allowed."""
        return region in self.allowed_regions and model in self.allowed_models
