"""
Unit Tests for Geofence Haversine Biometric Calculation Engine.
"""

import pytest
from apps.attendance.services.geofence_biometrics import GeofenceBiometricEngine


class TestGeofenceBiometricEngine:
    def test_haversine_distance_calculation(self):
        # Coordinates for Bangalore Office (12.9716, 77.5946)
        lat1, lon1 = 12.9716, 77.5946
        lat2, lon2 = 12.9720, 77.5950 # ~60 meters away
        dist = GeofenceBiometricEngine.calculate_haversine_distance(lat1, lon1, lat2, lon2)
        assert 40.0 <= dist <= 80.0

    def test_geofence_containment_inside(self):
        res = GeofenceBiometricEngine.verify_geofence_containment(
            punch_lat=12.9716,
            punch_lon=77.5946,
            office_lat=12.9717,
            office_lon=77.5947,
            allowed_radius_meters=150.0
        )
        assert res['is_valid_location']

    def test_geofence_containment_outside(self):
        res = GeofenceBiometricEngine.verify_geofence_containment(
            punch_lat=12.9800, # Far away
            punch_lon=77.6000,
            office_lat=12.9716,
            office_lon=77.5946,
            allowed_radius_meters=100.0
        )
        assert not res['is_valid_location']
        assert res['distance_meters'] > 500.0
