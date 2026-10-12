# What the tax engine can compute (schema 0.1)

A pack may use only these capabilities. They are general on purpose: the same feature serves every jurisdiction.

| # | Capability | How a pack uses it |
|---|---|---|
| C1 | A tax code on each invoice or bill line, one per tax | `tax_codes` |
| C2 | Rates that change on a date | `rates` with `effective_from` / `effective_to`; a document uses the rate in force on its date |
| C3 | Amounts entered before or after tax | Example lines: `amount_type: exclusive` or `inclusive` |
| C4 | A base that is a fraction of the net amount | `base: {fraction: "2/3"}` |
| C5 | A rate defined on a tax-inclusive amount (gross-up) | `base: {gross_up: true}` |
| C6 | One tax computed on top of another | `compound_on` |
| C7 | Zero-rated, exempt and out-of-scope supplies | `treatment` |
| C8 | Withholding at settlement | `kind: withholding`, receipts and payments |
| C9 | Reverse charge on purchases | `treatment: reverse_charge` |
| C10 | Unrecoverable input tax | `input_recoverable: false` |
| C11 | Rounding per line or per document, half up | `rounding` |
| C12 | Postings to statutory control accounts | `accounts` and each tax's `accounts` |
| C13 | Filing periods and due dates | `filing` |
| C14 | Tax return boxes | `returns` |
| C15 | Registration thresholds, for information | `registration_threshold` |
| C16 | Different treatment by business type | `questions` with `applies_when` on taxes and codes, for example one levy code per sector |

## Not available in schema 0.1

Partial input-tax recovery by percentage; tax on an amount other than the line net or the settled amount; caps and minimum amounts; special schemes (flat-rate, margin, cash accounting); tax on stock movements; official e-invoicing or submission to an authority; anything that needs a calculation script.

## Asking for more: capability requests

If a rule cannot be expressed with C1 to C16, **do not approximate it**. Add an entry to `capability-requests.md`:

```markdown
## CR-1: Partial input-tax recovery
- **Rule:** A business making both taxable and exempt supplies may recover input tax only in the ratio of taxable to total supplies.
- **Legal source:** VAT Act s.22 (date)
- **Who it affects:** Mixed-supply businesses, a large share of service firms
- **Worked example:** (inputs, hand-computed result)
- **Workaround meanwhile:** None; such businesses should not use the pack for input tax until supported.
```

Each request is considered as a general feature for every jurisdiction.
