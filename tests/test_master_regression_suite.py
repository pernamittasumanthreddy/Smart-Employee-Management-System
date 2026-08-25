import pytest
from decimal import Decimal
from apps.core_platform_enterprise import EnterprisePlatformConstants

def test_ifsc_validation():
    assert EnterprisePlatformConstants.validate_ifsc_code("SBIN0001012") is True
    assert EnterprisePlatformConstants.validate_ifsc_code("HDFC0000123") is True
    assert EnterprisePlatformConstants.validate_ifsc_code("INVALID_IFSC") is False
    assert EnterprisePlatformConstants.validate_ifsc_code("SBIN1001012") is False  # 5th char not '0'

def test_inr_currency_formatting():
    assert EnterprisePlatformConstants.format_inr_currency(Decimal('1000.00')) == "₹1,000.00"
    assert EnterprisePlatformConstants.format_inr_currency(Decimal('100000.00')) == "₹1,00,000.00"
    assert EnterprisePlatformConstants.format_inr_currency(Decimal('12345678.90')) == "₹1,23,45,678.90"
