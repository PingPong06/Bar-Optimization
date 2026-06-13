# Product Scope and Workflows

## Product Positioning

CutFlow is a commercial ERP for fenestration companies that fabricate aluminium or uPVC windows and doors. The system is designed to reduce manual quoting errors, convert measured openings into structured production data, generate customer-facing quotations, and optimize raw bar usage during fabrication.

## Primary Users

- Admin: owns setup, access, company settings, catalog integrity, and project locking.
- Salesman: creates customers, projects, measurements, and quotations.
- Production: creates jobs, generates cut items, runs optimization, and tracks hardware/glass/offcuts.
- Viewer: reviews dashboards and records without operational write access.

## End-to-End Workflow

1. A sales user creates a customer record.
2. A project is created for that customer with site and delivery details.
3. Site measurement items are entered for every opening.
4. A quotation is generated from the measurements.
5. Pricing is reviewed using profile, glass, hardware, fabrication, wastage, margin, and markup settings.
6. The quotation PDF is downloaded and sent to the customer.
7. When accepted, the project is moved toward order/production.
8. A production job is created from the accepted project.
9. Production items are generated from confirmed measurements.
10. Profile cut items and hardware requirements are calculated from formulas and rules.
11. Bar optimization is run for each profile group.
12. Cutting list, glass schedule, hardware summary, and offcut records support workshop execution.
13. Project status progresses through production, delivery, installation, and completion.

## In-Scope Commercial Capabilities

- Customer and project management.
- Site measurement capture.
- Configurable systems, profiles, colors, glass, and hardware.
- Formula-based profile cut calculation.
- Quotation pricing with taxes, discounts, freight, lifting, and installation charges.
- Quotation PDF generation.
- Production job generation from project measurements.
- Hardware BOQ generation.
- Bar optimization with kerf, end waste, and reusable offcuts.
- Basic role-aware navigation and access protection.

## Out-of-Scope Unless Added

- Online payment collection.
- Inventory purchasing and supplier management.
- Advanced CRM campaigns.
- Accounting system integration.
- E-signatures for quotation acceptance.
- Mobile offline survey capture.
- Multi-branch warehouse control.
- Automated email delivery tracking.
- Customer portal.

## Commercial Assumptions

- Dimensions are stored in millimetres.
- Area calculations use both square feet and square metres where relevant.
- Tax defaults are oriented around GST-style SGST/CGST/IGST fields.
- Production relies on accurate catalog formulas. Incorrect formulas directly affect quotation and cutting outputs.
- SQLite is acceptable for local development only. Production should use MySQL or a managed relational database.

