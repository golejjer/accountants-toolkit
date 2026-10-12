# Accountants Toolkit

Author and check **statutory packs** for GoLejjer.

A statutory pack is a jurisdiction's tax rules (VAT or GST, turnover levies, withholding taxes) written as structured data, worked examples and plain-language guidance. GoLejjer computes every tax figure from the pack's rule data; the client's AI assistant reads the pack's guidance to know what to ask and which code to choose.

Packs are written and owned by accountants, not by GoLejjer. GoLejjer checks that a pack is well-formed and that its worked examples reproduce exactly; it never reviews or endorses the tax content. Every pack a client uses is labelled with its author and the date it was last updated.

## What is here

| Folder | What it is |
|---|---|
| `skill/statutory-pack-authoring/` | An [Agent Skill](https://agentskills.io) your AI assistant follows to write a pack with you: the format, the engine's capabilities, how to write worked examples and guidance, and the checker |
| `checker/validate.py` | Runs the checker on a pack folder: `python checker/validate.py pack` (Python 3 and PyYAML) |
| `pack/` | The empty pack you fill in when you create a repository from this template |
| `examples/examplia/` | A complete pack for a fictional country. Every rate in it is invented |
| `.github/workflows/check.yml` | Runs the checker on every save and shows a tick or a cross on your repository |

## How to use it

**1. Give your AI assistant the skill.**
- Claude: download the latest `statutory-pack-authoring.zip` from this repository's Releases page, then in Claude go to Customize, Skills, "+", Create skill, Upload a skill. (Settings, Capabilities must have code execution and file creation on.)
- Other assistants: give them `skill/statutory-pack-authoring/SKILL.md` and its `references/` folder, and ask them to follow it.

**2. Create your own pack repository.** Click **Use this template** at the top of this page. Your new repository holds your pack in `pack/`, with the checker already running on every save. See `skill/statutory-pack-authoring/references/github-for-authors.md` for the web-only steps: no command line needed.

**3. Write the pack with your assistant.** Research each rule in its official source, fill in `pack/`, compute the worked examples by hand, and get a green tick.

**4. Publish a release** (for example `v1.0.0`) and register the repository link and tag in GoLejjer. GoLejjer fetches that exact version, runs its own checks, and keeps its own copy. If a rule cannot be expressed, the report says so and records it as a capability request; it also lands in `pack/capability-requests.md`.

**5. Attach the pack to your clients.** A pack reaches a client's books only through the Accountant role: the client invites you as their Accountant, and you attach your pack. When the law changes, publish a new release and every attached client moves to it from its effective date.

## Rules of the road

- Every rate, threshold and due date cites an official source with its date.
- Worked examples are computed by hand; the checker is a second opinion, never the authority.
- Rules the format cannot express are raised as capability requests, never approximated.
- No client data in a pack. No compliance claims ("compliant", "guaranteed", "approved", "official").
- Use an AI assistant only on a plan whose provider does not train on your content.

## Feedback

Open an issue: **Capability request** for a rule the format cannot express; **Kit problem** for anything unclear or wrong here.

## Licence

Apache 2.0 (see `LICENSE`). You own the packs you write. The example pack is fictional and carries no real jurisdiction's rules.
