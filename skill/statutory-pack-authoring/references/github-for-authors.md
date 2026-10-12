# GitHub for pack authors

You can keep your statutory pack in your own GitHub repository without using a command line. Your repository is the pack's home and its public record: every change, who made it, and every published version are visible there. Clients and other accountants can see that the pack is maintained.

Three steps, all on the GitHub website.

## 1. Create your repository from the template

1. Sign in to GitHub (a free account is enough).
2. Open the toolkit repository: `github.com/golejjer/accountants-toolkit`.
3. Click the green **Use this template** button, then **Create a new repository**.
4. Owner: your account or your firm's organisation. Name: `<country>-<scope>-pack`, for example `xx-general-pack`. Choose **Public** so clients can see it, or Private if you prefer (see the note at the end).
5. Click **Create repository**.

You now have a copy of the toolkit with an empty `pack/` folder ready to fill.

## 2. Edit your pack on the web

1. In your repository, open the `pack/` folder.
2. Click a file (for example `pack/rules.yaml`), then the pencil icon to edit it.
3. Paste or type your content. Your AI assistant, using the authoring skill in `skill/`, drafts each file with you.
4. Click **Commit changes**. Write one line saying what you changed, for example "Add VAT codes and rates". Choose **Commit directly to the main branch**.

Every save runs the checker automatically. A green tick next to the commit means the pack passes; a red cross means it does not. Click the cross to read the report, fix the file and save again.

To add a new file (for example a new worked example): open `pack/examples/`, click **Add file**, then **Create new file**.

## 3. Publish a release

A release is a frozen version with a number. The platform reads only releases, never work in progress.

1. Make sure the latest commit has a green tick.
2. Update `pack/CHANGELOG.md` and the `version` in `pack/pack.yaml` (for example `0.1.0` for the first release, `1.0.0` when you are confident, `1.1.0` for a law change, `1.1.1` for a correction).
3. On the repository page click **Releases** (right-hand side), then **Draft a new release**.
4. **Choose a tag**: type the version with a `v` in front, for example `v1.0.0`, and click **Create new tag**.
5. **Release title**: the same version. **Describe this release**: copy the change log entry.
6. Click **Publish release**.

Give the platform your repository link and the tag. It fetches that exact version, runs its own checks, and keeps its own copy. Later changes to your repository never affect a published version; a correction is a new release.

## When the law changes

1. Edit the rules: add a new rate with its `effective_from` date and close the old one with `effective_to`. Never change a value that is already released.
2. Add a change log entry citing the law.
3. Publish a new release.

## Private repositories

A private repository works the same way, but the platform cannot read it on its own. When you register the pack, the platform will ask you to install its read-only GitHub app on that one repository. The app can read the repository's contents and nothing else.

## If you get stuck

- Something in the toolkit is unclear or wrong: open an issue on `github.com/golejjer/accountants-toolkit` using the "Kit problem" template.
- A rule your jurisdiction needs cannot be expressed: open an issue there with the "Capability request" template, or add it to `pack/capability-requests.md` and mention it when you register the pack.
