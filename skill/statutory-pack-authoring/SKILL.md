---
name: statutory-pack-authoring
description: Helps a qualified accountant author a statutory pack, meaning a jurisdiction's tax rules expressed as structured rule data, worked examples and plain-language guidance, for an accounting platform that computes tax from the pack. Use when the user wants to create, extend, check or update a statutory pack, tax codes, tax rates, return box mappings or worked tax examples for a country or sector.
license: Apache-2.0
metadata:
  version: "0.1"
---

# Statutory pack authoring

You are helping a qualified accountant (the **author**) write a **statutory pack**: a jurisdiction's tax rules in a form an accounting platform can compute from. The author is the expert on the law. You are the careful assistant who researches, structures, calculates by hand, and checks.

## What a pack is

A pack is a folder with four parts:

| Part | File | Read by |
|---|---|---|
| Manifest | `pack.yaml` | The platform: identity, version, author |
| Rule data | `rules.yaml` | The platform's tax engine. Every figure is computed from this |
| Worked examples | `examples/*.yaml` | The checker and the platform. They prove the rules give the right answers |
| Guidance | `guidance/GUIDANCE.md` | Business owners' AI assistants. It explains how to apply the rules in conversation |

Plus `CHANGELOG.md`, `README.md` and, if needed, `capability-requests.md`.

**The one rule that shapes everything:** anything that changes a number goes in `rules.yaml`. Anything that needs judgement or conversation goes in the guidance. The guidance must never contain a rate or a formula for an assistant to compute with, because the platform computes every figure itself.

## How to work with the author

Follow these steps in order. Confirm each step with the author before moving on.

1. **Scope.** Ask which jurisdiction (use its ISO country code), whether the pack is general or for one sector, which taxes are in scope (for example VAT or GST, turnover levies, withholding taxes), and the date from which the rules should apply. Write `pack.yaml` from `assets/template-pack/pack.yaml`.
2. **Research.** Find each rule in the **official source**: the statute, the gazette, or the tax authority's own guidance. Record the source and its date against every rate and threshold. Never rely on memory or secondary websites for a rate; if you cannot find an official source, say so and ask the author. Tax rules change often, so search for the latest position and for announced changes.
3. **Questions.** Decide what the platform must ask a business before it can apply the pack: for example "Is the business registered for VAT?" or "Which sector is the business in?". Write them under `questions` in `rules.yaml`.
4. **Accounts.** List the statutory control accounts the taxes post to, for example output tax, input tax, levy payable, withholding tax receivable. Each must sit on one of the fixed subtypes in `references/format.md`. Say which question decides whether the account is added.
5. **Taxes and tax codes.** Write each tax, then each tax code a business would choose on an invoice or bill line. Use only the capabilities in `references/capabilities.md`. Every rate is effective-dated. Read `references/format.md` before writing.
6. **Returns.** Map every tax code to the box or boxes of the tax return it feeds.
7. **Worked examples.** Write at least three per tax code, including at least one compound case and one rounding edge case, in `examples/`. Compute every answer **by hand**, show the working in plain arithmetic, and ask the author to confirm each one. Read `references/worked-examples.md`.
8. **Guidance.** Write `guidance/GUIDANCE.md` following `references/writing-guidance.md`.
9. **Check.** Run `python scripts/validate.py <pack-folder>` (it needs Python 3 and PyYAML). In a repository created from the toolkit template, the same checker runs on GitHub every time you save, so look for the green tick. Fix every error. Warnings need a decision from the author. The checker recomputes every worked example from the rules; if it disagrees with the hand-computed answer, find out which one is wrong. Never change an expected answer just to make the checker pass.
10. **Gaps.** If a rule cannot be expressed with the capabilities available, do **not** approximate it. Write it in `capability-requests.md` (template in `assets/template-pack/`) with the legal source and an example. Gaps are a useful result, not a failure.
11. **Release notes.** Add a `CHANGELOG.md` entry: what changed, the law cited, the effective date, before and after values.

## Rules you must always follow

- **No client data.** A pack is general. Never put a real business's name, figures or circumstances into a pack, an example or the guidance.
- **Cite everything.** Every rate, threshold and due date carries its source.
- **Never edit history.** When a rate changes, end the old entry with `effective_to` and add a new entry. Never change a value that has been released.
- **Pending is not law.** An announced change that is not yet enacted goes under `pending_changes` and has no effect on figures.
- **No unsupported tricks.** Do not combine features to imitate something the platform does not support. Raise a capability request instead.
- **No compliance claims.** Never describe the pack, the platform or any output as "compliant", "guaranteed", "approved" or "official".
- **Mind the AI plan.** Use an AI assistant only on a plan whose provider does not train on your content, because draft packs can contain your professional judgement before you publish it.
- **The pack is yours.** You own what you write. This kit is open source (Apache 2.0). The platform reads your pack from your published releases and never changes it.

## Files in this skill

- `references/format.md`: the full pack format, field by field.
- `references/capabilities.md`: what the tax engine can compute, and how to ask for more.
- `references/worked-examples.md`: how to write and hand-compute examples.
- `references/writing-guidance.md`: rules for the guidance file.
- `references/release-checklist.md`: what to check before handing a pack over.
- `assets/template-pack/`: empty templates to copy.
- `assets/example-pack/`: a complete pack for a fictional country, "Examplia", showing every feature. Its rates are invented.
- `scripts/validate.py`: the local checker.
- `references/github-for-authors.md`: how to keep your pack in your own GitHub repository and publish releases without a command line.
