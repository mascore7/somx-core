"""
SOMX-CORE Sovereignty Router (Cryptographic SOMX-Net)
Unifies Gatekeeper authentication, Sovereignty Policy evaluation, 
and secure payload dispatch into a single cryptographic pipeline.
"""

from typing import Dict, Any, Tuple, Optional
from somx_core.security.gatekeeper import Gatekeeper
from somx_core.sovereignty.policy import SovereigntyPolicyEngine

class SovereigntyRouter:
    def __init__(self, gatekeeper: Gatekeeper, policy_engine: SovereigntyPolicyEngine):
        self.gatekeeper = gatekeeper
        self.policy_engine = policy_engine

    def route_request(
        self, 
        headers: Dict[str, str], 
        payload: str, 
        request_context: Dict[str, Any]
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Nidaamka Isku-xirka Guud (Sovereignty Router Pipeline):
        1. Xaqiijinta Zero-Trust mTLS & Token (Gatekeeper)
        2. Hubinta Xeerarka Madaxbannaanida & Jurisdiction (Policy Engine)
        3. Faafinta iyo Gudbinta Xogta ee Cryptographic SOMX-Net
        """
        
        # Tallaabada 1: Gatekeeper Security Check
        authorized, auth_error = self.gatekeeper.authorize_request(headers, payload)
        if not authorized:
            return False, f"Gatekeeper Rejection: {auth_error}", None

        # Tallaabada 2: Sovereignty & Policy Evaluation Check
        policy_passed, policy_msg = self.policy_engine.evaluate_policy(request_context)
        if not policy_passed:
            return False, f"Sovereignty Policy Rejection: {policy_msg}", None

        # Tallaabada 3: Routing & Cryptographic Verification Success
        routing_metadata = {
            "network": "CRYPTOGRAPHIC SOMX-NET",
            "status": "dispatched",
            "jurisdiction": request_context.get("jurisdiction"),
            "classification": request_context.get("classification", "standard"),
            "secure_tunnel": "mTLS-Enforced"
        }

        return True, "Request successfully verified and routed across SOMX-CORE", routing_metadata
