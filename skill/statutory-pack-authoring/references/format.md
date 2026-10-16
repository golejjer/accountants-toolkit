# Pack format (schema 0.1)

All files are YAML except the guidance and the change log, which are Markdown. **Write money amounts, rates and fractions as quoted strings** (`"15"`, `"1000.00"`, `"2/3"`) so they are never rounded by a computer. Dates are `YYYY-MM-DD`.

## 1. `pack.yaml`: the manifest

```yaml
schema_version: "0.1"
pack:
  id: examplia-general            # lowercase letters, digits and hyphens
  title: Examplia general statutory pack
  jurisdiction: XE                # ISO 3166-1 alpha-2 country code
  scope: general                  # "general", or a sector name if the pack covers one sector only
  currency: XTS                   # ISO 4217 code of the jurisdiction's currency
  version: 0.1.0                  # major.minor.patch: law change . correction . wording
  level: private                  # private | shared | verified
  status: draft                   # draft | submitted
  authors:
    - name: A. Author
      credential: Member, professional accountancy body
      member_no: "00000"
  reviewers: []                   # filled in when reviewed; a reviewer is never an author
  last_reviewed: null             # date of the last full review
```

**Authors.** Every author must have a real `name`, `credential` (professional body and grade) and `member_no` (membership number). The checker fails if any is empty or still template text (for example `<Full name>`, "to be completed", "n/a"). The pack carries these details to every client; GoLejjer does not verify them.

**Version.** `version` must equal the top `## x.y.z` heading in `CHANGELOG.md` and, for a release, the tag without its `v` (tag `v0.1.0` for version `0.1.0`).

## 2. `rules.yaml`: the rule data

Top-level sections, in this order: `questions`, `accounts`, `taxes`, `tax_codes`, `rounding`, `returns`, `pending_changes`.

### 2.1 `questions`

What the platform asks a business when it accepts the pack. Taxes, tax codes and accounts are switched on by the answers.

```yaml
questions:
  - key: registered_vat
    text: Is the business registered for VAT?
    type: yes_no
  - key: sector
    text: Which sector does most of the business's turnover come from?
    type: choice
    options: [services, retail, manufacturing]
```

### 2.2 Conditions (`applies_when`, `add_when`)

Used on taxes, tax codes and accounts. Either:
- a question key with a yes/no answer: `applies_when: registered_vat`, or
- a choice: `applies_when: {question: sector, in: [retail]}`.

Leave it out when something always applies.

### 2.3 `accounts`

The statutory control accounts the taxes post to. The platform adds them to a business's chart of accounts when the condition is met.

```yaml
accounts:
  - key: output_tax_control
    name: Output Tax Control
    subtype: current_liability
    purpose: Tax charged on sales, awaiting payment to the authority
    add_when: registered_vat
```

`subtype` must be one of these fixed subtypes: `current_asset`, `non_current_asset`, `current_liability`, `non_current_liability`, `equity`, `operating_income`, `non_operating_income`, `cost_of_sales`, `operating_expense`, `non_operating_expense`.

Examples refer to the business's own ordinary accounts with these fixed keys: `trade_receivables`, `trade_payables`, `revenue`, `expense`, `bank`.

### 2.4 `taxes`

```yaml
taxes:
  - key: VAT
    name: Value added tax
    kind: output_input            # output_input | levy | withholding
    applies_when: registered_vat
    accounts:
      output: output_tax_control  # output_input: output and input
      input: input_tax_control
    filing:
      frequency: monthly          # monthly | quarterly | half_yearly | yearly
      due: {days_after_period_end: 20}   # or {day_of_following_month: 15}
    registration_threshold:       # information only; the platform never registers anyone
      amount: "12000000.00"
      measure: rolling_12_months  # rolling_12_months | calendar_year | quarter
      effective_from: 2024-01-01
      source: "Examplia VAT Act 2020, s.10"
```

**Kinds and their accounts**

| `kind` | Meaning | `accounts` keys |
|---|---|---|
| `output_input` | Charged on sales, recoverable on purchases (VAT, GST) | `output`, `input` |
| `levy` | A turnover-based levy on sales | `payable`; plus `expense` when `charged_to_customer: false` |
| `withholding` | Deducted by the payer when an invoice is settled | `receivable` (deducted from us by customers), `payable` (we deduct from suppliers). `filing` is optional |

A `levy` also needs `charged_to_customer: true` (added to the invoice) or `false` (borne by the business as an expense).

### 2.5 `tax_codes`

The choices a business makes on an invoice or bill line. A line can carry at most one code per tax.

```yaml
tax_codes:
  - key: VAT-STD
    tax: VAT
    name: Standard-rated
    applies_to: [sales, purchases]   # sales | purchases | receipts | payments
    treatment: standard
    input_recoverable: true          # purchases only; false puts the tax into the expense
    compound_on: [LEVY]              # taxes whose amount on the same line is added to this code's base
    rates:
      - rate: "15"                   # percent
        base: {fraction: "1"}        # optional; see below
        effective_from: 2024-01-01
        effective_to: null
        source: "Examplia VAT Act 2020, s.4, as amended by Finance Act 2023"
```

**Treatments**

| `treatment` | Rates | Effect |
|---|---|---|
| `standard`, `reduced` | Required, above zero | Tax computed and posted |
| `zero_rated` | Required, exactly `"0"` | Reported as taxable at zero; no tax |
| `exempt` | None | Reported as exempt; no tax; no input recovery |
| `out_of_scope` | None | Not reported; no tax |
| `reverse_charge` | Required | Purchases only. The buyer accounts for output tax and, if recoverable, input tax; the supplier is paid the net amount |
| `withholding` | Required | Receipts or payments only. Computed on the amount settled |

**The base** (optional, per rate):
- `fraction: "2/3"`: the tax is computed on that fraction of the line's net amount. Default `"1"`.
- `gross_up: true`: the rate applies to an amount that already includes this tax, so tax = base × rate ÷ (100 − rate). Use it only where the law defines the tax that way.

**Compound taxes:** `compound_on: [LEVY]` adds the line's LEVY amount to this code's base before the rate is applied. The platform computes taxes in dependency order; a loop is an error. With line rounding, the compound tax uses the *rounded* amount of the tax it builds on; with document rounding, the unrounded amount.

### 2.6 `rounding`

```yaml
rounding:
  level: line          # line: round each tax on each line | document: add unrounded line taxes per code, round once
  method: half_up      # half_up only in schema 0.1
  decimals: 2
```

**Tax-inclusive amounts:** the platform works out the net amount from the inclusive amount, computes and rounds the taxes, then sets the net to the inclusive amount minus the rounded taxes charged, so the total always equals what was entered. With document rounding, each line's net is rounded and the last line absorbs any remainder.

**Document rounding in examples:** give per-code totals under `expected.tax_totals` instead of per-line `taxes`.

### 2.7 `returns`

```yaml
returns:
  - key: VAT-RETURN
    tax: VAT
    name: VAT return
    boxes:
      - key: "1"
        label: Standard-rated sales
        sum:
          - {code: VAT-STD, side: sales, measure: net}
      - key: "2"
        label: Output tax
        sum:
          - {code: VAT-STD, side: sales, measure: output_tax}
          - {code: VAT-RC, side: purchases, measure: output_tax}
```

- `side`: `sales`, `purchases`, `receipts` or `payments`.
- `measure`: `net` (the line amount before tax; for withholding, the amount settled), `output_tax`, `input_tax` (recoverable input tax only), `tax` (a levy's amount), or `withheld`.
- Every tax code must feed at least one box, unless its treatment is `out_of_scope`.

### 2.8 `pending_changes`

Announced but not enacted. No effect on any figure.

```yaml
pending_changes:
  - description: Standard rate to rise to 16%
    announced: 2026-09-01
    expected_effective: 2027-01-01
    source: "Budget speech 2026, para 41"
```

## 3. `examples/*.yaml`

See `worked-examples.md`.

## 4. `guidance/GUIDANCE.md`

Markdown with the same front matter as a skill:

```markdown
---
name: examplia-general-tax-guidance
description: How to apply the Examplia general statutory pack when recording sales, purchases and settlements.
---
```

See `writing-guidance.md`.

## 5. Postings the platform makes

Worked examples state the expected postings. The platform posts as follows (amounts in the document currency):

| Document | Debit | Credit |
|---|---|---|
| Sale invoice | `trade_receivables`: net + taxes charged to the customer | `revenue`: net; `output` account: output tax; levy `payable`: levy charged to customer |
| Sale invoice, levy not charged to customer | levy `expense`: levy | levy `payable`: levy |
| Purchase bill | `expense`: net + any unrecoverable tax; `input` account: recoverable tax | `trade_payables`: net + taxes charged by the supplier |
| Purchase bill, reverse charge | `expense`: net (+ the tax if not recoverable); `input` account: tax if recoverable | `trade_payables`: net; `output` account: tax |
| Receipt with withholding | `bank`: amount settled − withheld; withholding `receivable`: withheld | `trade_receivables`: amount settled |
| Payment with withholding | `trade_payables`: amount settled | `bank`: amount settled − withheld; withholding `payable`: withheld |

Debits equal credits on every document.
