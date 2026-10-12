# Before handing a pack over

- [ ] `python scripts/validate.py <pack-folder>` shows no errors.
- [ ] Every warning has been read and either fixed or explained in `README.md`.
- [ ] Every rate, threshold and due date cites an official source with its date.
- [ ] Each tax code has at least three worked examples, with hand working, confirmed by the author.
- [ ] Compound, rounding-edge, tax-inclusive and rate-change examples are included where they apply.
- [ ] Announced but unenacted changes are under `pending_changes`, not in `rates`.
- [ ] The guidance contains no rates or formulas, no client data, no compliance claims and no instructions outside its subject.
- [ ] Rules that could not be expressed are in `capability-requests.md`, not approximated.
- [ ] `CHANGELOG.md` has an entry for this version: what changed, law cited, effective date, before and after.
- [ ] `pack.yaml` version and `last_reviewed` are updated.
- [ ] The folder is zipped as `<pack-id>-<version>.zip` and sent only to the agreed recipient.
