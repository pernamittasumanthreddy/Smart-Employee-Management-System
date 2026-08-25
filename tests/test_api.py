import pytest
import json
from django.test import Client
from apps.api.openapi import OpenApiSpecGenerator

@pytest.mark.django_db
def test_api_endpoints_and_openapi(client):
    spec = OpenApiSpecGenerator.get_complete_spec()
    assert spec['openapi'] == '3.0.3'
    assert '/api/v1/employees/' in spec['paths']

    resp = client.get('/api/v1/employees/')
    assert resp.status_code == 200
    assert 'results' in resp.json()

    resp_attn = client.get('/api/v1/attendance/today/')
    assert resp_attn.status_code == 200

    resp_sync = client.post(
        '/api/v1/biometric/sync/',
        data=json.dumps({'device_id': 'GATE-01', 'user_id': 'EMP-1001', 'punch_type': 'IN'}),
        content_type='application/json'
    )
    assert resp_sync.status_code == 200
