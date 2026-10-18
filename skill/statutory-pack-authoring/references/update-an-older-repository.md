# Updating a pack repository made from an older toolkit

Use this guide if you created your repository from the toolkit before the checker was tightened (October 2026), or if you are not sure. Your pack files stay exactly as they are. You replace three of the toolkit's own files, then fix what the new check reports. Allow about 20 minutes.

## Why this matters

The checker that runs in your repository is a copy made on the day you created it. An older copy lets a pack pass with the author's name empty, with files in the wrong folder, or with a release tag that does not match the version. A green tick from an older copy does not mean the pack is ready.

## 1. Find out whether your repository is up to date

1. Open your repository on GitHub, then the **Actions** tab, the latest run, the job **check**, and the step **Check your pack**.
2. Look at the very first line of that step.

- `Toolkit checker 1.1` (or a higher number): your checker is current. Go to section 3.
- Anything else, or no such line: your checker is old. Do section 2.

## 2. Replace three files

You replace these three files in your repository with the current ones from the toolkit. Do not touch anything inside `pack/`.

| File in your repository | Current copy (plain text) |
|---|---|
| `skill/statutory-pack-authoring/scripts/validate.py` | https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/skill/statutory-pack-authoring/scripts/validate.py |
| `checker/validate.py` | https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/checker/validate.py |
| `.github/workflows/check.yml` | https://raw.githubusercontent.com/golejjer/accountants-toolkit/main/.github/workflows/check.yml |

For each file, one at a time:

1. Open the link in the right-hand column. You see the file as plain text. Select all (Ctrl+A on Windows, Cmd+A on Mac) and copy (Ctrl+C or Cmd+C).
2. In your repository, open the file at the path in the left-hand column. If it does not exist, click **Add file**, **Create new file**, and type the full path in the name box (typing a slash makes the folder).
3. If the file exists, click the pencil icon, select all of its text and replace it by pasting. Check that the first and last lines look like the link's first and last lines.
4. Click **Commit changes**, write "Update checker", choose **Commit directly to the main branch**, and confirm.

Do not use **Upload files** for this; it can put files in the wrong place.

When the third file is saved, a new run starts. Open **Actions**, the latest run, the step **Check your pack**. The first line must now read `Toolkit checker 1.1` or higher. If it does not, one of the three files was not replaced correctly: check each path and try again.

## 3. Fix what the new check reports

The current checker is stricter, so errors you did not see before may appear. Each one is a real gap in the pack. The common ones:

| The step says | What to do |
|---|---|
| `author 1: name (...) is empty or still the template text` (also credential, member_no) | Open `pack/pack.yaml`, click the pencil, and type your own full name, your professional body and grade, and your membership number. Never let an assistant make these up. Commit. |
| `the top entry is X but pack.yaml says version Y` | The top heading in `pack/CHANGELOG.md` and `version` in `pack/pack.yaml` must be the same number. |
| `the tag vX does not match pack.yaml version Y` | The release tag must be `v` plus the version. If a published release has the wrong number, do not edit it: raise the version, add a change log entry, and publish a new release (section 4 of the GitHub guide). |
| `pack/ has not been started` or files at the top of the repository | Follow "Check where your files are" in the GitHub guide. |
| `pack.level, if present, must be ...` | The `level` line is no longer used. Delete it (and `status`, `reviewers`, `last_reviewed` if they are there). |

Change nothing else. Do not change any rate, rule or worked example to make the check pass.

## 4. Release again

If you already published a release, it keeps its old number and stays as it was. Publish the corrected pack as the next version:

1. In `pack/pack.yaml` set `version` to the next number (for example `0.1.1` becomes `0.1.2`).
2. At the top of `pack/CHANGELOG.md` add a heading with the same number and one line saying what changed (for example "Added author details; no change to the rules").
3. Wait for the check on that commit: **Check your pack** must name your pack and end with `0 error(s)`.
4. Publish a release with the tag `v` plus the version, as in section 4 of the GitHub guide (`github-for-authors.md`).
5. Send the repository link and the tag to the person who asked for the pack.

## A prompt for any AI assistant

```
You are helping me, a qualified accountant, bring my statutory pack repository up to date with the current Accountants Toolkit. I am not a software developer: explain in plain words, one step at a time, and wait for me to say "done" before the next step. My repository is <paste your repository link>. The guide you are following is skill/statutory-pack-authoring/references/update-an-older-repository.md in github.com/golejjer/accountants-toolkit; if you cannot open it, ask me to paste it.

Rules
- Do not change my rules, rates, worked examples or guidance. Change only what the guide says.
- Never invent my name, credential, membership number or any figure. I will type my own details.
- Never ask for passwords, tokens or keys.
- If you cannot see my screen, ask me to paste the words or describe what I see.

Guide me through: (1) checking the first line of the "Check your pack" step; (2) replacing the three files listed in the guide; (3) reading the new result and fixing each error with me; (4) raising the version, adding the change log entry and publishing a new release; (5) telling me what to send to the person who asked for the pack.
```
