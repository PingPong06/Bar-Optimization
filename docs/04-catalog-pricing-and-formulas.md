# Catalog, Pricing, and Formulas

## Catalog Setup Order

1. Brands
2. Colors
3. Systems
4. Profiles
5. System-profile mappings
6. Profile formulas
7. Glass types
8. Hardware items
9. System hardware rules
10. Company settings

## System Configuration

Each `System` has:

- Unique code.
- Name and category.
- Optional brand.
- Active flag.
- Sort order.
- Standard, premium, and budget markup percentages.

Commercial rule: do not quote a system until all required profiles, formulas, glass compatibility, and hardware rules are validated.

## Profile Configuration

Each `Profile` stores:

- Stock number and name.
- Category and optional brand/system.
- Weight per metre.
- Cost per metre.
- Standard bar length.
- Cutting offsets.
- Default cut angles.
- Active flag.

Commercial rule: costs and weights should be reviewed whenever supplier pricing changes.

## Formula Engine

The formula engine evaluates safe numeric expressions using:

- `W`: width in mm.
- `H`: height in mm.
- `n_panels`: number of panels/sashes.
- `qty`: unit quantity.
- `offset_l`, `offset_r`, `offset_t`, `offset_b`: profile offsets.
- Supported functions: `min`, `max`, `round`.
- Supported operators: `+`, `-`, `*`, `/`, parentheses.

Unsupported Python syntax is rejected by the AST validator.

## Formula Validation Checklist

For every system:

- Test minimum and maximum supported dimensions.
- Test common panel counts.
- Test toughened and non-toughened glass cases where applicable.
- Confirm every required profile produces expected cut lengths.
- Confirm formulas never produce zero or negative lengths for valid products.
- Confirm quantities match workshop expectations.
- Confirm angles and position codes are understandable to production.
- Confirm generated production items have no diagnostics before release.

## Pricing Inputs

Quotation item pricing uses:

- Profile material cost.
- Glass cost.
- Hardware cost.
- Fabrication cost.
- Wastage percentage.
- Profit margin percentage.
- System pricing variant markup.

Quotation header pricing adds:

- Discount.
- Installation charge.
- Freight.
- Lifting charges.
- SGST/CGST/IGST settings.

## Commercial Pricing Controls

- Only admins should change base costs, wastage, fabrication, margins, tax rates, and markups.
- Pricing changes should be recorded with date, approver, and source supplier rate sheet.
- A sample quotation should be recalculated after every price update.
- Accepted quotations should not silently change if catalog rates are edited later.

