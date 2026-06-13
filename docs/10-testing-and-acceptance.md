# Testing and Acceptance

## Test Layers

Commercial readiness requires:

- Unit tests for formula evaluation and optimizer behavior.
- Model tests for pricing calculations.
- View tests for login and role permissions.
- PDF generation smoke tests.
- End-to-end workflow tests.
- Manual acceptance tests with real catalog data.

## Required Automated Test Areas

### Formula Engine

- Valid arithmetic formulas.
- `min`, `max`, and `round`.
- Unknown variables rejected.
- Unsafe syntax rejected.
- Division by zero handled as failure.

### Pricing

- Profile material cost.
- Glass cost.
- Hardware cost.
- Fabrication cost.
- Wastage and profit.
- Budget, standard, premium markups.
- Discount and tax calculations.

### Production

- Production items generated from measurements.
- Invalid measurements rejected.
- Missing formulas produce diagnostics.
- Hardware rules produce expected quantities.
- Optimization rejects cuts longer than available bar capacity.

### Access Control

- Anonymous users redirected to login.
- Sales users cannot access admin-only catalog settings.
- Production users cannot edit commercial quotation settings.
- Viewer users cannot perform write actions.

## Manual Acceptance Scenario

Use one sample customer and project:

1. Create customer.
2. Create project.
3. Add three measurement items:
   - One simple casement window.
   - One larger multi-panel window.
   - One door or fixed/sliding unit if catalog supports it.
4. Generate quotation.
5. Verify recommended rates.
6. Download quotation PDF.
7. Mark quotation accepted.
8. Create production job.
9. Generate production items.
10. Resolve diagnostics.
11. Run optimization.
12. Download or review cutting list, hardware summary, and glass schedule.
13. Confirm offcut records.

## Launch Acceptance Criteria

The product can launch commercially when:

- All critical and high issues in `12-commercial-gap-report.md` are resolved.
- Production settings pass `python manage.py check --deploy`.
- Smoke tests pass in staging.
- A real pilot project completes from customer to optimized cutting list.
- Business owner approves quotation PDF and terms.
- Production supervisor approves cutting list output.
- Backup and restore are tested.
- Admin and role training are complete.

