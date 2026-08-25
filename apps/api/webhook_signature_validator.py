import hmac
import hashlib

class WebhookSignatureValidator:
    '''
    HMAC-SHA256 signature verification for inbound biometric and third-party webhook payloads.
    '''

    @staticmethod
    def verify_signature(payload_bytes: bytes, secret_key: str, header_signature: str) -> bool:
        expected = hmac.new(secret_key.encode('utf-8'), payload_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, header_signature)
