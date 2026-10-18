# GitHub for pack authors

You can keep your statutory pack in your own GitHub repository without installing anything and without a command line. Your repository is the pack's home and its public record: every change, who made it, and every published version are visible there. Clients and other accountants can see that the pack is maintained.

You do not need to know GitHub. If your AI assistant can operate a browser it can do the clicks for you; if it cannot, it walks you through them one at a time. There is a ready-made prompt for this at the end of this guide.

GitHub renames buttons and moves menus from time to time. If something is not where this guide says, tell your assistant what you see on the screen (paste the words, or a screenshot) and ask it to find the equivalent.

## What you will end up with

Everything you write lives inside one folder called `pack/`. Files outside it are not read.

```
your-repository/
  pack/
    pack.yaml                 who you are, and the pack's name and version
    rules.yaml                the rule data
    CHANGELOG.md              what changed in each version
    README.md                 a short description of the pack
    capability-requests.md    only if some rule could not be expressed
    examples/
      01-services-sale.yaml   one file per worked example
      02-....yaml
    guidance/
      GUIDANCE.md             how an assistant should use the pack
```

The repository also contains the toolkit's own folders (`.github`, `checker`, `examples`, `skill`). Leave those alone.

## 1. Create your repository from the template

1. Sign in to GitHub (a free account is enough).
2. Open the toolkit repository: `github.com/golejjer/accountants-toolkit`.
3. Click the green **Use this template** button, then **Create a new repository**.
4. Owner: your account or your firm's organisation. Name: `<country>-<scope>-pack`, for example `xx-general-pack`. Choose **Public** so clients can see it, or Private if you prefer (see the note at the end).
5. Click **Create repository**.

You now have your own copy of the toolkit with a `pack/` folder holding empty templates for you to fill.

## 2. Put your files in the right place

Your assistant drafts each file with you. Getting the file into the repository in the right folder is the step where things most often go wrong, so read this section once.

**The reliable way: create each file in GitHub.**

1. On the repository's main page click **Add file**, then **Create new file**.
2. In the name box at the top, type the **full path including the folder**. For example `pack/rules.yaml` or `pack/examples/01-services-sale.yaml`. Typing a slash (`/`) creates the folder for you.
3. Paste the file's content into the large box.
4. Click **Commit changes**, write one line saying what you added (for example "Add VAT codes and rates"), choose **Commit directly to the main branch**, and confirm.

**Files that already exist in `pack/`** (`pack.yaml`, `rules.yaml`, `CHANGELOG.md`, `README.md`, `guidance/GUIDANCE.md`): open the file, click the pencil icon, replace the contents, and commit as above.

**Be careful with "Upload files".** GitHub's **Add file**, **Upload files** puts files where you currently are, and folder structure can be lost on the way: files that belong in `pack/` can end up at the top of the repository, and a zip file is stored as a zip, not unpacked. This has happened to a pilot author. If you upload, check afterwards (next step).

### Check where your files are

Open the repository's main page. You should see the folders `.github`, `checker`, `examples`, `pack` and `skill`, and none of your own files at the top level. If you see `pack.yaml`, `rules.yaml`, `GUIDANCE.md` or numbered example files (such as `01-services-sale.yaml`) at the top:

1. Click the file, then the pencil icon.
2. In the name box at the top, put the folder in front of the name: change `rules.yaml` to `pack/rules.yaml`, `GUIDANCE.md` to `pack/guidance/GUIDANCE.md`, `01-services-sale.yaml` to `pack/examples/01-services-sale.yaml`.
3. Click **Commit changes**. The file moves; its content does not change.

### Delete the blank sample

Once you have your own worked examples, delete the blank sample `pack/examples/00-template.yaml`: open it, click the three dots (**...**) at the top right of the file, choose **Delete file**, and commit.

### Fill in the author details

Open `pack/pack.yaml` and replace the three placeholder lines under `authors` with your own details: your full name, your professional body and membership grade, and your membership number. The pack carries these details, and every client's assistant tells the business owner who wrote the pack. Do this before you publish a release.

## 3. Read the check result

Every save runs the checker automatically.

1. Click the **Actions** tab at the top of your repository.
2. Click the latest run, then the job called **check**.
3. Open the step called **Check your pack**.

A green tick means the checks finished without an error. A red cross means there is a problem. In both cases open **Check your pack** and read it:

- It should report your pack and end with `0 error(s)`.
- If it says that `pack/` has not been started, **your pack was not checked at all**, even if the run shows a green tick. Right after you create the repository this is normal, because `pack/` still holds the empty templates.
- The step called **Check the fictional example pack** checks the toolkit's own sample (Examplia). It does not tell you anything about your pack.

If there are errors, copy the text of the step and paste it into your assistant. It explains each message and suggests a fix; you decide whether the rule or your hand calculation is wrong. Never change an expected answer only to make the check pass.

To add a new worked example later, use **Add file**, **Create new file**, and type the full path, for example `pack/examples/22-new-example.yaml`.

## 4. Publish a release

A release is a frozen version with a number. The platform reads only releases, never work in progress.

Before you start, make sure the version appears in three places and is the same everywhere:

| Where | What it should say (first release) |
|---|---|
| `version` in `pack/pack.yaml` | `0.1.0` |
| The first entry heading in `pack/CHANGELOG.md` | `## 0.1.0` |
| The release tag you create below | `v0.1.0` |

Use `0.1.0` for a first draft, `1.0.0` when you are confident, `1.1.0` for a law change and `1.1.1` for a correction.

Then:

1. Make sure the latest commit's **Check your pack** step reports your pack with `0 error(s)` (section 3).
2. On the repository's main page click **Releases** (on the right-hand side), then **Draft a new release**.
3. Click **Choose a tag**, type the version with a `v` in front (for example `v0.1.0`), and click **Create new tag** on publish.
4. **Release title**: the same version. **Describe this release**: copy the change log entry.
5. Click **Publish release**.

Give the platform your repository link and the tag. It fetches that exact version, runs its own checks, and keeps its own copy. Later changes to your repository never affect a published version; a correction is a new release with the next number.

## When the law changes

1. Edit the rules: add a new rate with its `effective_from` date and close the old one with `effective_to`. Never change a value that is already released.
2. Add a change log entry citing the law, and raise the version in `pack/pack.yaml` to match.
3. Publish a new release (section 4).

## Private repositories

A private repository works the same way, but the platform cannot read it on its own. When you register the pack, the platform will ask you to install its read-only GitHub app on that one repository. The app can read the repository's contents and nothing else.

## When something goes wrong

| What you see | What to do |
|---|---|
| The first line of **Check your pack** is not `Toolkit checker 1.1` (or higher), or your repository was created before October 2026 | Your checker is old. Follow `update-an-older-repository.md` before anything else. |
| Your files are at the top of the repository, not in `pack/` | Move each one as described under "Check where your files are". |
| The step **Check your pack** says `pack/` has not been started | Your pack was not checked. Make sure your files are inside `pack/` and that `pack/pack.yaml` no longer holds the template text (angle brackets such as `<jurisdiction>`). |
| A red cross and errors in **Check your pack** | Copy the text into your assistant and work through each message. |
| You cannot find **Releases** or **Add file** | GitHub may have moved it. Tell your assistant what you see on the screen and ask where the equivalent is. |
| Your assistant says it cannot open a toolkit link | Ask it to read the page you paste, or copy the file's text into the chat yourself. The links in the toolkit's README point to the plain text of each file. |
| You published a release with a mistake | Do not edit it. Fix the pack, raise the version, and publish a new release. |

## A prompt for any AI assistant

Paste this into your assistant (any assistant works, whether or not it can browse) to be guided through the GitHub steps. Replace the repository link with yours.

```
You are helping me, a qualified accountant, finish my statutory pack on GitHub. I am not a software developer, so explain everything in plain words, one step at a time, and wait for me to say "done" before the next step. My repository is <paste your repository link>. The guide you are following is skill/statutory-pack-authoring/references/github-for-authors.md in github.com/golejjer/accountants-toolkit; if you cannot open it, ask me to paste it.

Rules for this session
- Do not change, move, rename or delete any of my files unless I ask you to.
- Never invent my name, credential, membership number, rates, dates or sources. I will type my own details.
- Never ask me for passwords, tokens or keys.
- If you cannot open a page yourself, ask me to paste the words or describe what I see. You cannot see my screen unless you can operate a browser.

Please guide me through these, in order:
1. WHERE MY FILES ARE. Show me how to open the repository's main page and check that my pack files are inside the pack/ folder, with none at the top level. If some are at the top level, show me how to move each one.
2. THE CHECK. Show me how to open the Actions tab, the latest run, and the step called "Check your pack". Tell me in plain words whether my pack was really checked, and explain each error message if there are any.
3. MY DETAILS. Show me where the author details are in pack/pack.yaml. I will type my own name, professional body and grade, and membership number.
4. THE VERSION. Check that the version in pack/pack.yaml, the first heading in pack/CHANGELOG.md and the release tag I intend to use are the same.
5. THE RELEASE. Walk me through Releases, "Draft a new release", the tag, the title, and Publish release.

At the end, summarise what we did and what I should send to the person who asked for the pack: the repository link and the release tag.
```

## If you get stuck

- Something in the toolkit is unclear or wrong: open an issue on `github.com/golejjer/accountants-toolkit` using the "Kit problem" template.
- A rule your jurisdiction needs cannot be expressed: open an issue there with the "Capability request" template, or add it to `pack/capability-requests.md` and mention it when you register the pack.
