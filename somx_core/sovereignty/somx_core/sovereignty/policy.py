"""
SOMX-CORE Sovereignty Policy Engine
Manages data residency, jurisdiction compliance, and access rules.
"""

from typing import Dict, Any, List, Tuple

class SovereigntyPolicyEngine:
    def __init__(self, allowed_jurisdictions: List[str]):
        if not allowed_jurisdictions:
            raise ValueError("At least one allowed jurisdiction must be specified.")
        self.allowed_jurisdictions = set(allowed_jurisdictions)

    def evaluate_policy(self, request_context: Dict[str, Any]) -> Tuple[bool, str]:
        """Qiimeynta xeerarka madaxbannaanida xogta iyo caddaynta goobta (Jurisdiction)."""
        jurisdiction = request_context.get("jurisdiction")
        data_classification = request_context.get("classification", "standard")
        mfa_verified = request_context.get("mfa_verified", False)

        if not jurisdiction:
            return False, "Missing jurisdiction in request context"

        # Hubi in waddanka ama goobtu ay ku jirto liiska la oggol yahay (Data Residency)
        if jurisdiction not in self.allowed_jurisdictions:
            return False, f"Jurisdiction '{jurisdiction}' is not allowed under current sovereignty policy"

        # Xogta xasaasiga ah (restricted) waxay u baahan tahay MFA sugan
        if data_classification == "restricted" and not mfa_verified:
            return False, "Restricted data classification requires verified Multi-Factor Authentication (MFA)"

        return True, "Policy evaluation passed successfully"
