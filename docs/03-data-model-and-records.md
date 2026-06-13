# Data Model and Records

## Core Record Groups

### Accounts

- `UserProfile`: role, phone, avatar, active flag.
- `ActivityLog`: intended audit trail for user actions, model names, object ids, details, IP address, and timestamp.

### Catalog

- `Brand`: supplier or product brand.
- `Color`: finish/color data, including RAL or code.
- `System`: window/door system type with category and markup values.
- `Profile`: physical profile stock data, cost, bar length, offsets, and angles.
- `SystemProfile`: maps profiles to systems and roles.
- `ProfileFormula`: calculates cut length and quantity.
- `Glass`: glass type, specification, cost, and weight.
- `Hardware`: hardware stock data and unit costs.
- `SystemHardwareRule`: calculates hardware quantities for a system.
- `CompanySettings`: singleton for business identity, tax, terms, bar settings, wastage, fabrication, and margin.

### Projects

- `Customer`: customer identity, company, contact, billing/site details.
- `Project`: commercial project record, status, owner, dates, lock state, and notes.
- `ProjectStatusHistory`: status transition audit.
- `MeasurementItem`: site opening record with system, dimensions, glass, color, panels, flags, and final confirmed dimensions.

### Quotations

- `Quotation`: commercial quote header with status, revision, pricing variant, tax flags, discounts, delivery costs, payment terms, and totals.
- `QuotationItem`: line item copied from measurement data with calculated cost and recommended pricing support.

### Production

- `ProductionJob`: workshop job header linked to a project.
- `ProductionItem`: production copy of a measurement item.
- `ProductionCutItem`: generated profile cuts per production item.
- `HardwareRequirement`: generated hardware BOQ.
- `OptimizationRun`: optimization header and totals.
- `OptimizationSegment`: per-profile optimization summary.
- `OptimizedCut`: exact bar/cut assignment.
- `ReusableOffcut`: remaining stock large enough for future use.

## Data Ownership

- Customer and project records are business records and should be retained according to company policy.
- Quotation PDFs and production PDFs are commercial documents and should be reproducible from database state.
- Catalog changes affect future quotations and production output; they should be made only by trained admins.
- Formula changes should be versioned operationally because they can alter pricing and cut lists.

## Data Retention Recommendation

| Data | Suggested Retention |
| --- | --- |
| Customers and projects | 7 years or according to local business rules. |
| Quotations and PDFs | 7 years, especially for tax/commercial audit. |
| Production jobs and cut lists | 5-7 years or warranty period plus audit buffer. |
| Activity logs | Minimum 1 year; longer for regulated operations. |
| Backups | Daily for 30 days, monthly for 12 months, yearly archive if required. |

## Commercial Data Risks

- Deleting protected catalog records can break historical interpretation; prefer inactive flags over deletion.
- Catalog costs and margins are commercially sensitive.
- Customer names, addresses, phones, and emails are personal/business contact data.
- Formula changes need approval and test records before use in live quotes.

