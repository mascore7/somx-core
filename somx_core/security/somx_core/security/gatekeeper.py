"""
SOMX-CORE Security Gatekeeper
Enforces Zero-Trust mTLS token validation, payload integrity, and time-bound requests.
"""

import hashlib
import hmac
import time
from typing import Dict, Optional, Tuple

class Gatekeeper:
    def __init__(self, secret_key: bytes):
        if not secret_key or len(secret_key) < 32:
            raise ValueError("Secret key must be at least 32 bytes for robust HMAC security.")
        self.secret_key = secret_key

    def verify_token(self, token: str, payload: str, timestamp: int) -> bool:
        """Xaqiijinta Token-ka iyadoo la adeegsanayo HMAC-SHA256 iyo waqti xaddidan (Time-bound)."""
        current_time = int(time.time())
        
        # Hubi in codsigu uusan dhicin (tusaale: 300 ilbiriqsi / 5 daqiiqo gudahood)
        if abs(current_time - timestamp) > 300:
            return False

        # Abuur saxiixa la filayo (Expected Signature)
        message = f"{payload}.{timestamp}".encode('utf-8')
        expected_signature = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()

        # Isticmaal hmac.compare_digest si looga hortago timing attacks
        return hmac.compare_digest(expected_signature, token)

    def authorize_request(self, headers: Dict[str, str], payload: str) -> Tuple[bool, Optional[str]]:
        """Mucaaradka Zero-Trust: Hubinta Gatekeeper-ka ka hor inta aan la sii deyn taraafikada."""
        token = headers.get("X-SOMX-Token")
        timestamp_str = headers.get("X-SOMX-Timestamp")

        if not token or not timestamp_str:
            return False, "Missing required security headers (X-SOMX-Token or X-SOMX-Timestamp)"

        try:
            timestamp = int(timestamp_str)
        except ValueError:
            return False, "Invalid timestamp format"

        if not self.verify_token(token, payload, timestamp):
            return False, "Token verification failed or request expired"

        return True, None
