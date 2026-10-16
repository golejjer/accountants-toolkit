# Accountants Toolkit

Author and check **statutory packs** for GoLejjer.

A statutory pack is a jurisdiction's tax rules (VAT or GST, turnover levies, withholding taxes) written as structured data, worked examples and plain-language guidance. GoLejjer computes every tax figure from the pack's rule data; the client's AI assistant reads the pack's guidance to know what to ask and which code to choose.

Packs are written and owned by accountants, not by GoLejjer. GoLejjer checks that a pack is well-formed and that its worked examples reproduce exactly; it never reviews or endorses the tax content. Every pack a client uses is labelled with its author and the date it was last updated.

## If you are an accountant

Paste this page's link into your AI assistant and say:

> Help me author a statutory pack for my country using this toolkit.

Your assistant does the rest: it reads the instructions below, asks you what the pack should cover, helps you create your own copy of this repository, drafts every file with you, and tells you when the pack passes. You need a free GitHub account and your professional knowledge. No software to install, no command line.

## If you are an AI assistant

You are helping a qualified accountant (the **author**) write a statutory pack. The author is the expert on the law; you research, structure, calculate by hand and check. Follow these steps in order, confirming each with the author.

### 1. Read the skill first

Read these files, in this order, before asking the author anything:

1. `skill/statutory-pack-authoring/SKILL.md` ([raw](https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/skill/statutory-pack-authoring/SKILL.md)): the authoring procedure and the rules you must always follow.
2. `skill/statutory-pack-authoring/references/format.md` ([raw](https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/skill/statutory-pack-authoring/references/format.md)): the pack format, field by field.
3. `skill/statutory-pack-authoring/references/capabilities.md` ([raw](https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/skill/statutory-pack-authoring/references/capabilities.md)): what the tax engine can compute, and how to raise a capability request for anything it cannot.
4. `skill/statutory-pack-authoring/references/worked-examples.md` ([raw](https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/skill/statutory-pack-authoring/references/worked-examples.md)) and `writing-guidance.md` ([raw](https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/skill/statutory-pack-authoring/references/writing-guidance.md)): how to write the examples and the guidance.
5. `examples/examplia/` ([rules](https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/examples/examplia/rules.yaml), [one example](https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/examples/examplia/examples/01-service-sale.yaml), [guidance](https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/examples/examplia/guidance/GUIDANCE.md)): a complete pack for a fictional country. Every figure in it is invented; use it only to see the shape.

If you can install skills (for example Claude with code execution on), you may instead upload `statutory-pack-authoring.zip` from this repository's Releases page and activate it. Reading the files directly works just as well.

### 2. Agree the scope with the author

Ask, and write the answers down:

- **Jurisdiction** (ISO country code) and **currency**.
- **Which taxes.** A first pack should cover the jurisdiction's main **indirect tax** (VAT or GST), any **turnover-based levy**, and **withholding tax** on payments for services. Leave income tax, payroll taxes, customs and e-invoicing for a later release.
- **Scope:** general (all sectors, with a sector question where rules differ) is the default; a single-sector pack is fine if that is the author's practice.
- **From when:** rules in force from the start of the current tax year, plus any change already enacted. Announced but unenacted changes go under `pending_changes`.

### 3. Create the author's own repository

The pack lives in the author's repository, created from this template. All of this is on the GitHub website; the author needs a free account.

1. Open this repository and click the green **Use this template**, then **Create a new repository**.
2. Owner: the author's account. Name: `<country code>-general-pack` (for example `xx-general-pack`). **Public** is recommended, so clients can see the pack is maintained. Create it.
3. The new repository contains an empty `pack/` folder, the checker, and a workflow that runs the checker on every save.

If you can operate a browser, do these clicks for the author and show them the result. If you cannot, read `skill/statutory-pack-authoring/references/github-for-authors.md` ([raw](https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/skill/statutory-pack-authoring/references/github-for-authors.md)) and walk the author through it one click at a time.

### 4. Write the pack, one file at a time

Work through `SKILL.md` steps 2 to 8: research each rule in its official source, then draft `pack/pack.yaml`, `pack/rules.yaml`, the worked examples in `pack/examples/`, `pack/guidance/GUIDANCE.md`, `pack/CHANGELOG.md` and `pack/README.md`.

For each file: show the author the complete content and get their confirmation. Files that already exist in `pack/` are changed by opening them (pencil icon), replacing the contents and choosing **Commit changes** directly to main. New files are made with **Add file**, **Create new file**, typing the full path in the name box (for example `pack/examples/01-services-sale.yaml`; a slash makes the folder). Do not use **Upload files** unless you have checked afterwards that every file sits inside `pack/`: uploads can drop the folder and leave files at the top level, where they are not read. Delete the blank `pack/examples/00-template.yaml` once the author has their own examples. Do these steps for the author if you can operate a browser.

After every save, GitHub runs the checker. A green tick alone is not enough: open the **Actions** tab, the latest run, and the step **Check your pack**, and confirm that it names the author's pack and ends with `0 error(s)`. If it says `pack/` has not been started, the pack was not checked. A **red cross** means a problem: ask the author to paste you the output, fix the file, and save again. The checker recomputes every worked example from the rules, so a mismatch means either the rules or the hand calculation is wrong: work out which, and never change an expected answer only to make the check pass.

Rules that cannot be expressed with the capabilities in `capabilities.md` go in `pack/capability-requests.md`, with the legal source and a worked example. Do not approximate them.

### 5. Publish a release

When the step **Check your pack** on the latest commit reports the author's pack with `0 error(s)`, the author's own name, credential and membership number are filled in `pack/pack.yaml`, and the author has confirmed every worked example:

1. Set `version` in `pack/pack.yaml` (first release `0.1.0`), add the `pack/CHANGELOG.md` entry with the same number, and use the tag `v0.1.0`. The three must match.
2. On the repository page: **Releases**, **Draft a new release**, tag `v0.1.0`, title `v0.1.0`, description copied from the change log, **Publish release**.

### 6. Finish

Give the author this to send to whoever asked for the pack:

- the repository link and the release tag;
- `pack/capability-requests.md`, if any;
- a short note: time spent, what was unclear in this toolkit, where you (the assistant) helped and where you got things wrong, and any rule the author is unsure about.

GoLejjer registers the pack by its repository link and tag, runs its own checks, and keeps its own copy of that version. The author attaches the pack to a client's books only after the client invites them as Accountant. When the law changes, the author publishes a new release and every attached client moves to it from its effective date.

## What is here

| Folder | What it is |
|---|---|
| `skill/statutory-pack-authoring/` | The [Agent Skill](https://agentskills.io): procedure, format, capabilities, example rules, guidance rules, GitHub guide, and the checker |
| `checker/validate.py` | Runs the checker: `python checker/validate.py --repo .` checks your whole repository (files in `pack/`, author details filled in, version matches) (Python 3 and PyYAML) |
| `tests/` | The checker's own tests (toolkit maintainers only) |
| `pack/` | The empty pack the author fills in after "Use this template" |
| `examples/examplia/` | A complete pack for a fictional country; every rate is invented |
| `.github/workflows/check.yml` | Runs the checker on every save and shows a tick or a cross |

## Rules of the road

- Every rate, threshold and due date cites an official source with its date.
- Worked examples are computed by hand; the checker is a second opinion, never the authority.
- Rules the format cannot express are raised as capability requests, never approximated.
- No client data in a pack. No compliance claims ("compliant", "guaranteed", "approved", "official").
- Use an AI assistant only on a plan whose provider does not train on your content.

## Feedback

Open an issue here: **Capability request** for a rule the format cannot express; **Kit problem** for anything unclear or wrong.

## Licence

Apache 2.0 (see `LICENSE`). Authors own the packs they write. The example pack is fictional and carries no real jurisdiction's rules.
