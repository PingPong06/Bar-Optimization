# Production and Optimization

## Production Job Flow

1. Select a project ready for production.
2. Create a production job.
3. Generate production items from project measurements.
4. The service computes profile cuts using active formulas.
5. The service computes hardware requirements using hardware rules.
6. Production reviews diagnostics.
7. Optimization runs by profile group.
8. The system stores optimization runs, segments, optimized cuts, and reusable offcuts.
9. Production uses cutting list, hardware summary, and glass schedule in the workshop.

## Cut Generation

Cut generation is handled by `production.services.generate_production_items`.

The process:

- Copies measurement data into production items.
- Evaluates active `ProfileFormula` records for the measurement system.
- Applies formula conditions and width/height bounds.
- Stores cut length, quantity, angles, and position code.
- Evaluates active hardware rules.
- Stores diagnostics if formulas or rules are missing or invalid.

## Optimization Method

The optimizer groups cuts by profile and uses a best-fit/depth-limited search approach to reduce standard bar usage and scrap. It accounts for:

- Standard bar length.
- Kerf.
- End waste.
- Minimum reusable offcut length.
- Available reusable offcuts by profile.

## Workshop Acceptance Criteria

A production job is workshop-ready only when:

- All dimensions are confirmed.
- The project is accepted or approved for production.
- All production items are complete.
- Diagnostics are empty or reviewed.
- Optimization completed successfully.
- Cutting list is reviewed by a production supervisor.
- Glass and hardware summaries are reviewed against the project.

## Offcut Policy

Reusable offcuts should be physically labelled with:

- Profile stock number.
- Length in mm.
- Source job number.
- Date created.
- Rack or storage location.

The `ReusableOffcut.location_notes` field should be used to keep the system aligned with the workshop.

## Commercial Controls to Add or Enforce

- Require project lock before final optimization.
- Prevent optimization when any production item has unresolved diagnostics.
- Add supervisor approval for final cutting list release.
- Add status transitions for cutting, assembly, quality check, and complete.
- Add inventory reconciliation if stock levels are commercially required.

