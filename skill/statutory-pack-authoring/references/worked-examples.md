# Worked examples

Worked examples are the proof that the rules are right. The checker recomputes each one from `rules.yaml` and compares it with the author's hand-computed answer. Both must agree exactly.

## How many

- At least **three per tax code**.
- At least one **compound** case (a tax on top of another) where the pack has one.
- At least one **rounding edge** case: an amount whose tax ends in exactly half a cent, or several lines whose rounded taxes differ from the rounded total.
- At least one **tax-inclusive** line where the pack expects businesses to enter inclusive amounts.
- One example dated **just before and one just after** each rate change.

## File format

One example per file, named `examples/NN-short-name.yaml`.

```yaml
id: "03"
title: "Retail sale with levy and VAT, line rounding"
date: 2026-03-15
document: sale_invoice          # sale_invoice | purchase_bill | receipt | payment
answers:                        # the business's answers to the pack's questions
  registered_vat: yes
  levy_liable: yes
  sector: retail
lines:                          # invoices and bills
  - description: Goods
    amount: "1000.00"
    amount_type: exclusive      # exclusive | inclusive
    codes: [LEVY-RET, VAT-STD]
settlement:                     # receipts and payments instead of lines
  amount: "1000.00"
  codes: [WHT-SVC]
working: |
  Levy base = 1000.00 x 3/5 = 600.00; levy (gross-up 3%) = 600.00 x 3 / 97 = 18.5567..., rounded half up = 18.56
  VAT base = 1000.00 + 18.56 = 1018.56; VAT = 1018.56 x 15% = 152.784, rounded = 152.78
  Total = 1000.00 + 18.56 + 152.78 = 1171.34
expected:
  lines:
    - net: "1000.00"
      taxes: {LEVY-RET: "18.56", VAT-STD: "152.78"}
  total: "1171.34"              # invoices and bills: amount owed by or to the other party
  postings:
    - {account: trade_receivables, debit: "1171.34"}
    - {account: revenue, credit: "1000.00"}
    - {account: levy_payable, credit: "18.56"}
    - {account: output_tax_control, credit: "152.78"}
  boxes:
    VAT-RETURN: {"1": "1000.00", "4": "152.78"}
    LEVY-RETURN: {"1": "1000.00", "2": "18.56"}
```

- `settlement` is used instead of `lines` for receipts and payments. Its `total` is the cash that moved.
- `taxes` lists every code on the line, with its tax amount.
- `postings`: one entry per account. Use `debit` or `credit`, never both. Combine amounts to the same account into one entry.
- `boxes`: list only the boxes this document changes.

## The working

- Show every step as plain arithmetic, in the order the rules apply.
- State the rate, the fraction and the rounding used at each step.
- When a total is computed before the per-line split (inclusive amounts), show how any remainder from rounding is allocated: the net amount absorbs it.
- The author confirms every example before the pack is submitted.

## When the checker disagrees

1. Recompute by hand, slowly.
2. If the hand answer is right, the rules are wrong: fix `rules.yaml`.
3. If the rules are right, the hand answer is wrong: fix the example, and note why in the working.
4. If the law needs something the engine cannot do, raise a capability request (`capabilities.md`) and remove the example from this pack until it is supported.

Never change an expected value only to make the checker pass.
