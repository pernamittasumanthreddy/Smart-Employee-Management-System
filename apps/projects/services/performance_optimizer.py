"""
Smart Enterprise Management System — Project Management & Resource Allocation Query Optimizer & Memory Cache
Milestone tracking, resource utilization, and budget vs actuals.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple


class ProjectsPerformanceOptimizer:
    """
    In-memory LRU caching and query result cache for Project Management & Resource Allocation.
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
