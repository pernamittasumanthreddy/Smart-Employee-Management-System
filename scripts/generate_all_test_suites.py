import os

def write_test(rel_path, content):
    os.makedirs(os.path.dirname(rel_path), exist_ok=True)
    with open(rel_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    lines = len(content.strip().splitlines())
    print(f"Generated Test: {rel_path} ({lines} LOC)")

print("Generating 30 Comprehensive Test Suites in tests/...")

test_tax_code = '''"""
Unit Tests for Indian Income Tax Calculation Engine (Section 115BAC & Old Regime).
"""

from decimal import Decimal
import pytest
from apps.payroll.services.tax_calculator import (
    IncomeTaxCalculationEngine,
    TaxExemptionDeclaration,
    TaxComputationResult
)


class TestIncomeTaxCalculationEngine:
    def test_new_regime_zero_tax_under_7_lakhs(self):
        """Income up to 7,00,000 should have zero tax after standard deduction and 87A rebate."""
        res = IncomeTaxCalculationEngine.calculate_new_regime_tax(Decimal('750000.00'))
        # 7.5L - 75K Std Ded = 6.75L Taxable Income <= 7.0L -> Tax should be 0
        assert res.taxable_income == Decimal('675000.00')
        assert res.total_tax_liability == Decimal('0.00')
        assert res.rebate_87a > Decimal('0.00')

    def test_new_regime_tax_15_lakhs(self):
        """Income of 15,00,000 in New Regime."""
        res = IncomeTaxCalculationEngine.calculate_new_regime_tax(Decimal('1575000.00'))
        # 15.75L - 75K Std Ded = 15.0L Taxable Income
        assert res.taxable_income == Decimal('1500000.00')
        # Slabs: 0-3L (0), 3-7L (20k), 7-10L (30k), 10-12L (30k), 12-15L (60k) = 140,000 + 4% cess = 145,600
        assert res.slab_tax == Decimal('140000.00')
        assert res.total_tax_liability == Decimal('145600.00')

    def test_old_regime_hra_exemption_metro(self):
        """HRA exemption for metro city."""
        basic = Decimal('600000.00')
        hra = Decimal('300000.00')
        rent = Decimal('240000.00')
        exempt = IncomeTaxCalculationEngine.calculate_hra_exemption(basic, hra, rent, is_metro=True)
        # Condition 1: 300,000
        # Condition 2: 50% of 600,000 = 300,000
        # Condition 3: 240,000 - 10% of 600,000 (60,000) = 180,000
        assert exempt == Decimal('180000.00')

    def test_old_regime_chapter_via_capping(self):
        """80C capped at 1.5 Lakhs, 80CCD at 50k, 24b at 2 Lakhs."""
        dec = TaxExemptionDeclaration(
            section_80c=Decimal('250000.00'), # Should cap at 1.5L
            section_80d_self=Decimal('35000.00'), # Cap at 25k
            section_80ccd_1b=Decimal('80000.00'), # Cap at 50k
            section_24b=Decimal('300000.00') # Cap at 2L
        )
        total_ded = IncomeTaxCalculationEngine.calculate_chapter_via_deductions(dec)
        assert total_ded == Decimal('425000.00') # 150k + 25k + 50k + 200k

    def test_regime_comparison(self):
        dec = TaxExemptionDeclaration(section_80c=Decimal('150000.00'), section_80d_self=Decimal('25000.00'))
        comp = IncomeTaxCalculationEngine.compare_regimes(
            gross_income=Decimal('1200000.00'),
            basic_salary=Decimal('500000.00'),
            hra_received=Decimal('250000.00'),
            declaration=dec
        )
        assert comp['recommended_regime'] in ['NEW', 'OLD']
        assert comp['tax_savings'] >= Decimal('0.00')
'''
write_test('tests/test_tax_calculator_service.py', test_tax_code)

test_salary_code = '''"""
Unit Tests for Salary Slip Formula Generation Engine.
"""

from decimal import Decimal
import pytest
from apps.payroll.services.salary_slip_generator import SalaryCalculationEngine


class TestSalaryCalculationEngine:
    def test_epf_contributions_with_ceiling(self):
        """EPF calculations capped at statutory Rs. 15,000 ceiling."""
        res = SalaryCalculationEngine.calculate_epf_contributions(Decimal('45000.00'), cap_at_statutory_ceiling=True)
        assert res['epf_employee'] == Decimal('1800.00') # 12% of 15,000
        assert res['eps_employer'] == Decimal('1250.00') # 8.33% capped at 1250
        assert res['epf_employer'] == Decimal('550.00')  # 1800 - 1250

    def test_epf_contributions_without_ceiling(self):
        """EPF calculations on actual basic salary without ceiling."""
        res = SalaryCalculationEngine.calculate_epf_contributions(Decimal('50000.00'), cap_at_statutory_ceiling=False)
        assert res['epf_employee'] == Decimal('6000.00') # 12% of 50,000

    def test_esi_applicable_under_21k(self):
        emp_esi, empr_esi = SalaryCalculationEngine.calculate_esi_contributions(Decimal('18000.00'))
        assert emp_esi == Decimal('135.00') # 0.75% of 18,000
        assert empr_esi == Decimal('585.00') # 3.25% of 18,000

    def test_esi_exempt_above_21k(self):
        emp_esi, empr_esi = SalaryCalculationEngine.calculate_esi_contributions(Decimal('45000.00'))
        assert emp_esi == Decimal('0.00')
        assert empr_esi == Decimal('0.00')

    def test_gratuity_provision(self):
        basic = Decimal('52000.00')
        prov = SalaryCalculationEngine.calculate_gratuity_provision(basic)
        # (52,000 * 15 / 26) / 12 = 30,000 / 12 = 2500.00
        assert prov == Decimal('2500.00')

    def test_full_pay_breakdown_matches_ctc(self):
        monthly_ctc = Decimal('100000.00')
        breakdown = SalaryCalculationEngine.generate_full_pay_breakdown(monthly_ctc=monthly_ctc)
        assert breakdown.total_cost_to_company == monthly_ctc
        assert breakdown.gross_earnings > breakdown.net_take_home_pay
        assert breakdown.net_take_home_pay > Decimal('0.00')
'''
write_test('tests/test_salary_computation_service.py', test_salary_code)

test_ptax_code = '''"""
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
'''
write_test('tests/test_state_ptax_service.py', test_ptax_code)

test_compliance_code = '''"""
Unit Tests for Statutory Compliance Validator and Legal Rule Checker.
"""

from decimal import Decimal
import pytest
from apps.compliance.services.statutory_validator import StatutoryComplianceValidator


class TestStatutoryComplianceValidator:
    def test_minimum_wages_compliance_pass(self):
        violations = StatutoryComplianceValidator.validate_minimum_wages(
            state='KARNATAKA',
            skill_category='SKILLED',
            monthly_basic_plus_da=Decimal('25000.00')
        )
        assert len(violations) == 0

    def test_minimum_wages_violation_detect(self):
        violations = StatutoryComplianceValidator.validate_minimum_wages(
            state='KARNATAKA',
            skill_category='SKILLED',
            monthly_basic_plus_da=Decimal('12000.00')
        )
        assert len(violations) == 1
        assert violations[0].statute_code == 'MWA_1948_SEC12'
        assert violations[0].severity == 'CRITICAL'

    def test_work_hours_ceiling_violation(self):
        violations = StatutoryComplianceValidator.validate_work_hours_and_overtime(
            daily_hours=Decimal('10.5'),
            weekly_hours=Decimal('54.0'),
            consecutive_days=7,
            interval_rest_minutes=15
        )
        assert len(violations) >= 3 # Daily ceiling, weekly ceiling, consecutive days, rest interval

    def test_maternity_benefit_sanction_check(self):
        violations = StatutoryComplianceValidator.validate_maternity_benefit_compliance(
            employee_gender='FEMALE',
            days_worked_past_12_months=120,
            is_maternity_requested=True,
            approved_leave_weeks=18
        )
        assert len(violations) == 1
        assert violations[0].statute_code == 'MBA_2017_AMENDMENT'
'''
write_test('tests/test_compliance_statutory.py', test_compliance_code)

test_posh_code = '''"""
Unit Tests for POSH Governance and Statutory 90-Day Timeline Monitor.
"""

from datetime import date, timedelta
import pytest
from apps.compliance.services.posh_governance_engine import POSHGovernanceEngine


class TestPOSHGovernanceEngine:
    def test_statutory_timeline_within_deadline(self):
        complaint_dt = date.today() - timedelta(days=30)
        res = POSHGovernanceEngine.track_case_statutory_timeline(
            complaint_id='POSH-2026-001',
            complainant='Employee A',
            respondent='Employee B',
            incident_dt=complaint_dt - timedelta(days=5),
            complaint_dt=complaint_dt,
            stage='FORMAL_INQUIRY'
        )
        assert not res.is_overdue
        assert res.days_elapsed == 30
        assert res.days_remaining == 60

    def test_statutory_timeline_overdue(self):
        complaint_dt = date.today() - timedelta(days=95)
        res = POSHGovernanceEngine.track_case_statutory_timeline(
            complaint_id='POSH-2026-002',
            complainant='Employee X',
            respondent='Employee Y',
            incident_dt=complaint_dt - timedelta(days=10),
            complaint_dt=complaint_dt,
            stage='FORMAL_INQUIRY'
        )
        assert res.is_overdue
        assert res.days_remaining == 0

    def test_ic_constitution_compliance_pass(self):
        res = POSHGovernanceEngine.validate_ic_constitution(
            total_members=5,
            presiding_officer_is_senior_woman=True,
            female_member_count=3,
            has_external_ngo_member=True
        )
        assert res['is_compliant']
        assert len(res['violations']) == 0

    def test_ic_constitution_invalid_presiding_officer(self):
        res = POSHGovernanceEngine.validate_ic_constitution(
            total_members=4,
            presiding_officer_is_senior_woman=False,
            female_member_count=1,
            has_external_ngo_member=False
        )
        assert not res['is_compliant']
        assert len(res['violations']) >= 3
'''
write_test('tests/test_posh_governance.py', test_posh_code)

test_attrition_code = '''"""
Unit Tests for ML Attrition Predictor and Retention Risk Scorer.
"""

from decimal import Decimal
import pytest
from apps.insights.services.ml_attrition_predictor import EmployeeAttritionPredictor


class TestEmployeeAttritionPredictor:
    def test_high_risk_employee_detection(self):
        res = EmployeeAttritionPredictor.calculate_flight_risk(
            emp_id='EMP-1001',
            name='Rohit V',
            dept='Engineering',
            current_salary=Decimal('50000.00'),
            benchmark_market_salary=Decimal('90000.00'), # 45% below market
            tenure_months=38,
            months_since_last_promotion=38,
            monthly_avg_overtime_hours=42.0,
            manager_changed_past_6_months=True,
            unplanned_leave_spike_percent=60.0,
            recent_sentiment_score=-0.7
        )
        assert res.flight_risk_score >= 70.0
        assert res.risk_level in ['CRITICAL', 'HIGH']
        assert len(res.key_risk_drivers) >= 3
        assert len(res.retention_recommendations) >= 2

    def test_low_risk_satisfied_employee(self):
        res = EmployeeAttritionPredictor.calculate_flight_risk(
            emp_id='EMP-1002',
            name='Priya S',
            dept='Design',
            current_salary=Decimal('95000.00'),
            benchmark_market_salary=Decimal('90000.00'),
            tenure_months=14,
            months_since_last_promotion=6,
            monthly_avg_overtime_hours=5.0,
            manager_changed_past_6_months=False,
            unplanned_leave_spike_percent=0.0,
            recent_sentiment_score=0.8
        )
        assert res.flight_risk_score <= 30.0
        assert res.risk_level == 'LOW'
'''
write_test('tests/test_attrition_prediction.py', test_attrition_code)

test_workload_code = '''"""
Unit Tests for Team Workload and Sprint Capacity Forecaster.
"""

import pytest
from apps.insights.services.workload_forecasting_engine import WorkloadForecastingEngine


class TestWorkloadForecastingEngine:
    def test_optimal_capacity_sprint(self):
        members = [
            {'name': 'Dev 1', 'leave_days': 0, 'assigned_hours': 65.0},
            {'name': 'Dev 2', 'leave_days': 1, 'assigned_hours': 60.0},
            {'name': 'Dev 3', 'leave_days': 0, 'assigned_hours': 68.0},
        ]
        res = WorkloadForecastingEngine.forecast_sprint_capacity('Backend Core', members)
        assert res.total_engineers == 3
        assert res.workload_status in ['OPTIMAL', 'UNDERUTILIZED']
        assert res.estimated_sprint_story_points > 0

    def test_overloaded_sprint_alert(self):
        members = [
            {'name': 'Lead Dev', 'leave_days': 0, 'assigned_hours': 105.0}, # Overloaded
            {'name': 'Senior Dev', 'leave_days': 2, 'assigned_hours': 90.0},
        ]
        res = WorkloadForecastingEngine.forecast_sprint_capacity('Mobile Team', members)
        assert res.workload_status == 'OVERLOADED'
        assert len(res.overload_risk_members) > 0
'''
write_test('tests/test_workload_capacity.py', test_workload_code)

test_sentiment_code = '''"""
Unit Tests for Workplace Feedback Sentiment Analyzer.
"""

import pytest
from apps.insights.services.sentiment_analyzer import WorkplaceSentimentAnalyzer


class TestWorkplaceSentimentAnalyzer:
    def test_positive_feedback_analysis(self):
        text = "The leadership team is very supportive and collaborative. Great growth environment!"
        res = WorkplaceSentimentAnalyzer.analyze_feedback_text(text)
        assert res['sentiment'] == 'POSITIVE'
        assert res['score'] > 0.3
        assert 'supportive' in res['positive_hits']

    def test_negative_burnout_feedback(self):
        text = "Severe micromanagement and toxic deadlines. Everyone is exhausted and overworked."
        res = WorkplaceSentimentAnalyzer.analyze_feedback_text(text)
        assert res['sentiment'] == 'NEGATIVE'
        assert res['score'] < -0.3
        assert 'toxic' in res['negative_hits']

    def test_negated_sentiment(self):
        text = "The working culture is not supportive and there is no transparent leadership."
        res = WorkplaceSentimentAnalyzer.analyze_feedback_text(text)
        assert res['sentiment'] == 'NEGATIVE'
'''
write_test('tests/test_sentiment_analyzer.py', test_sentiment_code)

test_gratuity_code = '''"""
Unit Tests for Gratuity Actuarial Calculation Engine.
"""

from decimal import Decimal
import pytest
from apps.compliance.services.gratuity_actuarial_engine import GratuityActuarialEngine


class TestGratuityActuarialEngine:
    def test_gratuity_tenure_rounding(self):
        """Tenure of 5 years 8 months rounds to 6 years."""
        res = GratuityActuarialEngine.calculate_statutory_gratuity(
            last_drawn_basic_plus_da=Decimal('52000.00'),
            completed_years_of_service=5,
            fractional_months=8
        )
        assert res['is_eligible_for_gratuity']
        assert res['effective_service_years'] == 6
        # Daily wage = 52,000 / 26 = 2000
        # Gratuity = 2000 * 15 * 6 = 1,80,000
        assert res['calculated_gratuity_amount'] == Decimal('180000.00')

    def test_gratuity_ineligible_under_5_years(self):
        res = GratuityActuarialEngine.calculate_statutory_gratuity(
            last_drawn_basic_plus_da=Decimal('50000.00'),
            completed_years_of_service=3,
            fractional_months=2
        )
        assert not res['is_eligible_for_gratuity']

    def test_gratuity_capped_at_20_lakhs(self):
        res = GratuityActuarialEngine.calculate_statutory_gratuity(
            last_drawn_basic_plus_da=Decimal('260000.00'), # 10k/day
            completed_years_of_service=25
        )
        # 10,000 * 15 * 25 = 37,50,000 -> Should cap at 20,00,000
        assert res['statutory_payable_amount'] == Decimal('2000000.00')
        assert res['taxable_portion'] == Decimal('1750000.00')
'''
write_test('tests/test_gratuity_actuarial_service.py', test_gratuity_code)

test_insurance_code = '''"""
Unit Tests for Group Health Insurance Claims Adjudicator.
"""

from decimal import Decimal
import pytest
from apps.benefits.services.insurance_claim_engine import InsuranceClaimEngine


class TestInsuranceClaimEngine:
    def test_standard_claim_adjudication(self):
        res = InsuranceClaimEngine.adjudicate_claim(
            claim_id='CLM-2026-881',
            emp_id=101,
            patient_name='Rahul K',
            is_parent=False,
            sum_insured=Decimal('500000.00'),
            hospital_bill=Decimal('120000.00'),
            room_rent_per_day=Decimal('4000.00'), # Below 1% of 5L (5000/day)
            hospitalization_days=4,
            non_medical_charges=Decimal('5000.00')
        )
        assert res.claim_status == 'APPROVED'
        assert res.room_rent_deduction == Decimal('0.00')
        assert res.final_settled_amount == Decimal('115000.00') # 120k - 5k

    def test_parental_copay_deduction(self):
        res = InsuranceClaimEngine.adjudicate_claim(
            claim_id='CLM-2026-882',
            emp_id=102,
            patient_name='Father of Emp',
            is_parent=True, # 10% co-pay
            sum_insured=Decimal('500000.00'),
            hospital_bill=Decimal('100000.00'),
            room_rent_per_day=Decimal('3000.00'),
            hospitalization_days=3,
            non_medical_charges=Decimal('0.00')
        )
        assert res.co_pay_deduction == Decimal('10000.00') # 10% of 100k
        assert res.final_settled_amount == Decimal('90000.00')
'''
write_test('tests/test_insurance_claims_service.py', test_insurance_code)

test_asset_dep_code = '''"""
Unit Tests for Asset Depreciation Schedule Calculator (SLM Method).
"""

from decimal import Decimal
import pytest
from apps.assets.services.asset_depreciation_engine import AssetDepreciationEngine


class TestAssetDepreciationEngine:
    def test_laptop_depreciation_3_years(self):
        res = AssetDepreciationEngine.calculate_slm_depreciation_schedule(
            asset_id='AST-LAP-001',
            name='MacBook Pro 16',
            category='LAPTOP',
            purchase_cost=Decimal('200000.00'),
            salvage_rate_pct=Decimal('5.0') # Salvage = 10,000, Depreciable = 190,000
        )
        assert res.useful_life_years == 3
        assert res.salvage_value == Decimal('10000.00')
        assert res.depreciable_base == Decimal('190000.00')
        assert len(res.depreciation_schedule_years) == 3
        assert res.depreciation_schedule_years[-1]['closing_book_value'] == Decimal('10000.00')
'''
write_test('tests/test_asset_depreciation_service.py', test_asset_dep_code)

test_geofence_code = '''"""
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
'''
write_test('tests/test_geofence_biometrics_service.py', test_geofence_code)

test_resume_parser_code = '''"""
Unit Tests for Resume Keyword Extractor and Match Scorer.
"""

import pytest
from apps.recruitment.services.resume_parser import ResumeParsingEngine


class TestResumeParsingEngine:
    def test_resume_skill_and_exp_extraction(self):
        text = """
        Rohit Verma - Lead Software Engineer
        Email: rohit.verma@example.com | Phone: (987) 654-3210
        Summary: 6+ years of experience developing web applications using Python, Django,
        PostgreSQL, Docker, React, and AWS cloud infrastructure. Holds a B.Tech in Computer Science.
        """
        required = ['Python', 'Django', 'PostgreSQL', 'AWS']
        profile = ResumeParsingEngine.parse_resume_text(text, required)
        assert profile.email == 'rohit.verma@example.com'
        assert profile.total_experience_years == 6.0
        assert profile.skill_match_percentage == 100.0
        assert profile.is_shortlisted
'''
write_test('tests/test_resume_parser_service.py', test_resume_parser_code)

test_okr_code = '''"""
Unit Tests for OKR Cascading Progress Engine.
"""

import pytest
from apps.goals.services.okr_cascading_engine import OKRCascadingEngine


class TestOKRCascadingEngine:
    def test_okr_weighted_progress(self):
        krs = [
            {'title': 'Deliver Microservices', 'current_value': 80, 'target_value': 100, 'weight': 2.0}, # 80% * 2 = 160
            {'title': 'Achieve 99.9% Uptime', 'current_value': 100, 'target_value': 100, 'weight': 1.0}, # 100% * 1 = 100
        ]
        res = OKRCascadingEngine.calculate_objective_progress(1, 'Cloud Modernization', 'DevOps', krs)
        # Total weight = 3.0, weighted sum = 260 -> 260 / 3 = 86.7%
        assert res.overall_progress_percent == 86.7
        assert res.health_status == 'ON_TRACK'
'''
write_test('tests/test_okr_cascading_service.py', test_okr_code)

test_enps_code = '''"""
Unit Tests for eNPS Statistical Engine.
"""

import pytest
from apps.surveys.services.enps_statistical_engine import ENPSSurveyEngine


class TestENPSSurveyEngine:
    def test_enps_calculation(self):
        # 10 respondents: 6 Promoters (9-10), 2 Passives (7-8), 2 Detractors (0-6)
        ratings = [10, 10, 9, 9, 9, 10, 8, 7, 5, 4]
        res = ENPSSurveyEngine.calculate_enps(ratings)
        assert res.promoters_count == 6
        assert res.passives_count == 2
        assert res.detractors_count == 2
        assert res.promoter_percentage == 60.0
        assert res.detractor_percentage == 20.0
        assert res.enps_score == 40.0 # 60 - 20
        assert res.satisfaction_benchmark == 'GOOD'
'''
write_test('tests/test_enps_survey_service.py', test_enps_code)

print("Batch of Test Suites Generated Successfully!")
