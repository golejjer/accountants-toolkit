# Before handing a pack over

- [ ] `python scripts/validate.py <pack-folder>` shows no errors (in a repository, `python checker/validate.py --repo .`).
- [ ] The author's name, professional body and grade, and membership number are filled in `pack.yaml` (the checker fails without them).
- [ ] `pack.yaml` version, the top `CHANGELOG.md` entry and the release tag (`v` plus the version) are the same.
- [ ] Every warning has been read and either fixed or explained in `README.md`.
- [ ] Every rate, threshold and due date cites an official source with its date.
- [ ] Each tax code has at least three worked examples, with hand working, confirmed by the author.
- [ ] Compound, rounding-edge, tax-inclusive and rate-change examples are included where they apply.
- [ ] Announced but unenacted changes are under `pending_changes`, not in `rates`.
- [ ] The guidance contains no rates or formulas, no client data, no compliance claims and no instructions outside its subject.
- [ ] Rules that could not be expressed are in `capability-requests.md`, not approximated.
- [ ] `CHANGELOG.md` has an entry for this version: what changed, law cited, effective date, before and after.
- [ ] The latest commit's **Check your pack** step names your pack and ends with `0 error(s)`.
- [ ] The release is published on GitHub with the tag `v` plus the version, and you have the repository link and the tag to give to the person who asked for the pack.
