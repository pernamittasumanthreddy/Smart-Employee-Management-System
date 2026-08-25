"""
Smart Enterprise Management System — Employee Recognition & Peer Kudos Query Optimizer & Memory Cache
Kudos points wallet, peer badges, leaderboard, and gift vouchers.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple


class RecognitionPerformanceOptimizer:
    """
    In-memory LRU caching and query result cache for Employee Recognition & Peer Kudos.
    """

    _CACHE_STORE: Dict[str, Tuple[Any, datetime]] = {}
    CACHE_TTL_SECONDS = 300 # 5 minutes

    @classmethod
    def get_cached_result(cls, cache_key: str) -> Optional[Any]:
        if cache_key in cls._CACHE_STORE:
            val, expiry = cls._CACHE_STORE[cache_key]
            if datetime.now() < expiry:
                return val
            else:
                del cls._CACHE_STORE[cache_key]
        return None

    @classmethod
    def set_cached_result(
        cls,
        cache_key: str,
        value: Any,
        ttl_seconds: Optional[int] = None
    ) -> None:
        ttl = ttl_seconds or cls.CACHE_TTL_SECONDS
        expiry = datetime.now() + timedelta(seconds=ttl)
        cls._CACHE_STORE[cache_key] = (value, expiry)

    @classmethod
    def invalidate_cache(cls, key_prefix: Optional[str] = None) -> int:
        if not key_prefix:
            cleared = len(cls._CACHE_STORE)
            cls._CACHE_STORE.clear()
            return cleared

        keys_to_del = [k for k in cls._CACHE_STORE if k.startswith(key_prefix)]
        for k in keys_to_del:
            del cls._CACHE_STORE[k]
        return len(keys_to_del)
