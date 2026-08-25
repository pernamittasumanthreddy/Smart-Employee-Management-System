import math
from decimal import Decimal
from typing import Tuple, Dict, Any

class GeoFencingVerificationService:
    '''
    Validates GPS latitude and longitude coordinates against authorized corporate office boundaries
    using the Haversine Great-Circle distance formula on the WGS 84 ellipsoid.
    '''

    # Corporate Office Geofence Targets (Bengaluru HQ, Mumbai, Hyderabad, Pune, Delhi NCR)
    OFFICE_LOCATIONS = {
        'HQ_BENGALURU': {'name': 'Bengaluru HQ Campus', 'lat': 12.9716, 'lon': 77.5946, 'radius_meters': 250},
        'MUMBAI_FIN': {'name': 'Mumbai Financial Center BKC', 'lat': 19.0688, 'lon': 72.8687, 'radius_meters': 200},
        'HYDERABAD_TECH': {'name': 'Hyderabad HITEC City', 'lat': 17.4435, 'lon': 78.3772, 'radius_meters': 250},
        'PUNE_DEV': {'name': 'Pune Magarpatta Cybercity', 'lat': 18.5158, 'lon': 73.9272, 'radius_meters': 200},
        'DELHI_GURUGRAM': {'name': 'Gurugram Cyber Hub', 'lat': 28.4950, 'lon': 77.0895, 'radius_meters': 250},
    }

    EARTH_RADIUS_METERS = 6371000.0

    @classmethod
    def calculate_distance_meters(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi / 2.0) ** 2) + (math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return cls.EARTH_RADIUS_METERS * c

    @classmethod
    def verify_location_within_geofence(cls, user_lat: float, user_lon: float) -> Dict[str, Any]:
        closest_office = None
        min_distance = float('inf')
        is_valid = False

        for code, office in cls.OFFICE_LOCATIONS.items():
            dist = cls.calculate_distance_meters(user_lat, user_lon, office['lat'], office['lon'])
            if dist < min_distance:
                min_distance = dist
                closest_office = office
                if dist <= office['radius_meters']:
                    is_valid = True

        return {
            'is_within_geofence': is_valid,
            'distance_to_office_meters': round(min_distance, 2),
            'matched_office': closest_office['name'] if closest_office else 'None',
            'allowed_radius_meters': closest_office['radius_meters'] if closest_office else 250,
        }
