# Enterprise Payroll & Indian Statutory Compliance Handbook

## 1. Statutory Deduction Framework
The Smart EMS payroll engine enforces exact calculation models under Indian labor and tax jurisprudence:
- **Employees' Provident Fund (EPF)**: 12% employee deduction and 12% employer contribution (3.67% to EPF, 8.33% to EPS capped at statutory wage ceiling).
- **Employees' State Insurance (ESI)**: 0.75% employee contribution and 3.25% employer contribution for employees earning gross wages up to ₹21,000 per month.
- **Professional Tax (PT)**: State-specific slabs (standard ₹200/month in Karnataka / Maharashtra).
- **Tax Deducted at Source (TDS)**: Computed under Section 192 of Income Tax Act 1961 comparing Old vs New Tax Regimes (Section 115BAC).

## 2. Salary Components Architecture
| Component | Classification | Taxability | Standard Formula |
| :--- | :--- | :--- | :--- |
| **Basic Pay** | Core Earning | 100% Taxable | 40% - 50% of Annual CTC |
| **House Rent Allowance (HRA)** | Earning | Partially Exempt (Sec 10(13A)) | 20% - 25% of Basic Pay |
| **Dearness Allowance (DA)** | Earning | 100% Taxable | 10% of Basic Pay |
| **Special Allowance** | Flexible Earning | 100% Taxable | CTC balancing component |
| **Provident Fund (PF)** | Statutory Deduction | Exempt up to statutory caps | 12% of (Basic + DA) |
| **Professional Tax** | State Statutory | Deductible under Sec 16(iii) | ₹200.00 / month |
