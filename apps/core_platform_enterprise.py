from decimal import Decimal
from typing import Dict, List, Any

class EnterprisePlatformConstants:
    '''
    Enterprise Platform Constants, IFSC Bank Routing Dictionary, Indian State Codes,
    and Currency Localization Formatters.
    '''

    INDIAN_STATES_AND_UT = [
        ('AN', 'Andaman and Nicobar Islands'),
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CH', 'Chandigarh'),
        ('CT', 'Chhattisgarh'),
        ('DH', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('DL', 'Delhi (National Capital Territory)'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JK', 'Jammu and Kashmir'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('LA', 'Ladakh'),
        ('LD', 'Lakshadweep'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PY', 'Puducherry'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TG', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UT', 'Uttarakhand'),
        ('WB', 'West Bengal'),
    ]

    MAJOR_INDIAN_BANKS = {
        'SBI': {'name': 'State Bank of India', 'ifsc_prefix': 'SBIN', 'rtgs_supported': True},
        'HDFC': {'name': 'HDFC Bank Ltd', 'ifsc_prefix': 'HDFC', 'rtgs_supported': True},
        'ICICI': {'name': 'ICICI Bank Ltd', 'ifsc_prefix': 'ICIC', 'rtgs_supported': True},
        'AXIS': {'name': 'Axis Bank Ltd', 'ifsc_prefix': 'UTIB', 'rtgs_supported': True},
        'KOTAK': {'name': 'Kotak Mahindra Bank', 'ifsc_prefix': 'KKBK', 'rtgs_supported': True},
        'PNB': {'name': 'Punjab National Bank', 'ifsc_prefix': 'PUNB', 'rtgs_supported': True},
        'BOB': {'name': 'Bank of Baroda', 'ifsc_prefix': 'BARB', 'rtgs_supported': True},
        'CANARA': {'name': 'Canara Bank', 'ifsc_prefix': 'CNRB', 'rtgs_supported': True},
    }

    @classmethod
    def validate_ifsc_code(cls, ifsc: str) -> bool:
        if not ifsc or len(ifsc) != 11:
            return False
        # Character 5 is always '0'
        return ifsc[4] == '0' and ifsc[:4].isalpha() and ifsc[5:].isalnum()

    @staticmethod
    def format_inr_currency(amount: Decimal) -> str:
        # Formats number according to Indian Numbering System (Lakhs and Crores)
        s = f"{amount:.2f}"
        parts = s.split('.')
        integer_part = parts[0]
        decimal_part = parts[1]

        if len(integer_part) <= 3:
            formatted_int = integer_part
        else:
            last_three = integer_part[-3:]
            remaining = integer_part[:-3]
            # Group in 2s
            groups = []
            while len(remaining) > 2:
                groups.insert(0, remaining[-2:])
                remaining = remaining[:-2]
            if remaining:
                groups.insert(0, remaining)
            formatted_int = ",".join(groups) + "," + last_three

        return f"₹{formatted_int}.{decimal_part}"
