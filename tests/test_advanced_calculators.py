import pytest
from decimal import Decimal
from apps.payroll.salary_components import SalaryComponentCalculator
from apps.recruitment.scorecard_compiler import InterviewScorecardCompiler
from apps.benefits.flexi_benefit_allocator import FlexibleBenefitPlanAllocator
from apps.timesheets.client_invoice_compiler import ClientInvoiceCompiler
from apps.surveys.sentiment_analyzer import WorkforceSentimentAnalyzer

def test_salary_component_gratuity_and_nps():
    # Tenure < 5 years
    assert SalaryComponentCalculator.calculate_gratuity_provision(Decimal('80000.00'), Decimal('4.0')) == Decimal('0.00')
    # Tenure >= 5 years: (15 * 80000 * 6) / 26 = 276923.08
    grat = SalaryComponentCalculator.calculate_gratuity_provision(Decimal('80000.00'), Decimal('6.0'))
    assert grat > Decimal('270000.00')

    nps = SalaryComponentCalculator.calculate_nps_corporate_contribution(Decimal('80000.00'))
    assert nps['monthly_nps_employer'] == Decimal('8000.00')
    assert nps['eligible_under_section'] == '80CCD(2)'

def test_scorecard_compiler():
    verdict = InterviewScorecardCompiler.compute_composite_rating(5, 5, 4, 5)
    assert verdict['hiring_verdict'] == 'STRONG_HIRE'
    assert verdict['is_above_bar'] is True

def test_flexi_benefit_allocator():
    fbp = FlexibleBenefitPlanAllocator.calculate_optimal_fbp_distribution(Decimal('200000.00'))
    assert fbp['total_fbp_allocated'] > Decimal('50000.00')
    assert fbp['estimated_annual_tax_saved_inr'] > Decimal('15000.00')

def test_client_invoice_compiler():
    items = [
        {'role': 'Lead Cloud Architect', 'hours': 40, 'hourly_rate': 150},
        {'role': 'Senior Full-Stack Engineer', 'hours': 80, 'hourly_rate': 100},
    ]
    inv = ClientInvoiceCompiler.generate_invoice_summary("Tata Consultancy Services", "INV-2026-001", items)
    assert inv['subtotal'] == Decimal('14000.00')
    assert inv['gst_amount'] == Decimal('2520.00')
    assert inv['grand_total'] == Decimal('16520.00')

def test_sentiment_analyzer():
    res_pos = WorkforceSentimentAnalyzer.analyze_feedback_text("Great innovative culture, highly supportive leadership and proud to be here!")
    assert res_pos['sentiment'] == 'POSITIVE'
    assert res_pos['positive_word_count'] >= 3

    res_neg = WorkforceSentimentAnalyzer.analyze_feedback_text("Overworked and high stress with delayed approvals.")
    assert res_neg['sentiment'] == 'NEGATIVE'
