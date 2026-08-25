"""
Unit Tests for State Professional Tax Statutory Calculator.
"""

from decimal import Decimal
import pytest
from apps.payroll.services.state_ptax_calculator import StateProfessionalTaxCalculator


class TestStateProfessionalTaxCalculator:
    def test_karnataka_ptax_under_25k(self):
        tax = StateProfessionalTaxCalculator.calculate_ptax('KARNATAKA', Decimal('22000.00'))
        assert tax == Decimal('0.00')

    def test_karnataka_ptax_above_25k(self):
        tax = StateProfessionalTaxCalculator.calculate_ptax('KARNATAKA', Decimal('45000.00'))
        assert tax == Decimal('200.00')

    def test_maharashtra_february_surcharge(self):
        """In Maharashtra, Feb PT is Rs. 300 instead of Rs. 200."""
        jan_tax = StateProfessionalTaxCalculator.calculate_ptax('MAHARASHTRA', Decimal('35000.00'), month=1)
        feb_tax = StateProfessionalTaxCalculator.calculate_ptax('MAHARASHTRA', Decimal('35000.00'), month=2)
        assert jan_tax == Decimal('200.00')
        assert feb_tax == Decimal('300.00')

    def test_maharashtra_female_exemption(self):
        """Women in Maharashtra earning <= 25,000 are exempt."""
        tax = StateProfessionalTaxCalculator.calculate_ptax('MAHARASHTRA', Decimal('22000.00'), month=1, gender='FEMALE')
        assert tax == Decimal('0.00')

    def test_telangana_slabs(self):
        assert StateProfessionalTaxCalculator.calculate_ptax('TELANGANA', Decimal('12000.00')) == Decimal('0.00')
        assert StateProfessionalTaxCalculator.calculate_ptax('TELANGANA', Decimal('18000.00')) == Decimal('150.00')
        assert StateProfessionalTaxCalculator.calculate_ptax('TELANGANA', Decimal('35000.00')) == Decimal('200.00')
