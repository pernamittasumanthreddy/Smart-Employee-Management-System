import json
from typing import Dict, Any

class OpenApiSpecGenerator:
    '''
    Generates OpenAPI 3.0.3 compliant specification JSON for the Smart EMS REST API suite.
    '''

    @staticmethod
    def get_complete_spec() -> Dict[str, Any]:
        return {
            'openapi': '3.0.3',
            'info': {
                'title': 'Bharat Enterprise Solutions - Smart EMS API',
                'version': '2.0.0-enterprise',
                'description': 'Enterprise Workforce, HR, Payroll, Biometrics, and Talent Management REST API Suite',
                'contact': {
                    'name': 'EMS Enterprise API Team',
                    'email': 'api-support@smartems.enterprise.bharat',
                },
            },
            'servers': [
                {'url': 'http://127.0.0.1:8000', 'description': 'Local Development Server'},
                {'url': 'https://api.smartems.enterprise.bharat', 'description': 'Production High-Availability Cluster'},
            ],
            'paths': {
                '/api/v1/employees/': {
                    'get': {
                        'summary': 'List all active employees',
                        'tags': ['Employees'],
                        'responses': {'200': {'description': 'Successful response with employee array'}},
                    }
                },
                '/api/v1/attendance/today/': {
                    'get': {
                        'summary': 'Retrieve daily live attendance punches',
                        'tags': ['Attendance'],
                        'responses': {'200': {'description': 'Today presence data'}},
                    }
                },
                '/api/v1/biometric/sync/': {
                    'post': {
                        'summary': 'Ingest biometric access gate punches',
                        'tags': ['Biometrics'],
                        'requestBody': {'required': True, 'content': {'application/json': {}}},
                        'responses': {'200': {'description': 'Punch logged successfully'}},
                    }
                },
                '/api/v1/projects/': {
                    'get': {
                        'summary': 'List active client projects',
                        'tags': ['Projects'],
                        'responses': {'200': {'description': 'Project array'}},
                    }
                },
            },
            'components': {
                'securitySchemes': {
                    'ApiKeyAuth': {
                        'type': 'apiKey',
                        'in': 'header',
                        'name': 'X-EMS-API-KEY',
                    }
                }
            }
        }
