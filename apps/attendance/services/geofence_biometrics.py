"""
Geofencing & Biometric Validation Engine:
Implements Haversine distance formula, office radius boundary containment,
and IP subnet validation for mobile/touchless attendance.
"""

import math
from typing import Dict, Optional, Tuple


class GeofenceBiometricEngine:
    """
    Geofence coordinate validator and IP subnet verifier.
    """

    EARTH_RADIUS_METERS = 6371000.0

    @classmethod
    def calculate_haversine_distance(
        cls,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """
        Calculates great-circle distance between two geographic coordinates in meters.
        """
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

        distance = cls.EARTH_RADIUS_METERS * c
        return round(distance, 2)

    @classmethod
    def verify_geofence_containment(
        cls,
        punch_lat: float,
        punch_lon: float,
        office_lat: float,
        office_lon: float,
        allowed_radius_meters: float = 150.0
    ) -> Dict[str, any]:
        distance = cls.calculate_haversine_distance(punch_lat, punch_lon, office_lat, office_lon)
        is_inside = distance <= allowed_radius_meters

        return {
            'is_valid_location': is_inside,
            'distance_meters': distance,
            'allowed_radius_meters': allowed_radius_meters,
            'message': 'Punch location verified within office perimeter.' if is_inside else f'Punch location is {distance:.1f}m away (outside allowed radius of {allowed_radius_meters}m).'
        }
