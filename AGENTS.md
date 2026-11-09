# Agent instructions

This repository holds the profile README of `mattgrul`. GitHub shows
`README.md` on the profile page, so keep the README to the card alone.
Put notes for people who change the repository here.

## The card

The README shows `card-dark.svg` or `card-light.svg` from the branch
`output`, chosen by the visitor's theme.

- `card/card.py` draws both cards. It needs only the standard library.
- `card/portrait.json` holds the ASCII portrait. `card/portrait.py`
  makes it from the profile picture. Its header says how to run it.
- `.github/workflows/card.yml` draws the cards each night and on each
  merge to `main`, and pushes them to `output`. Its header says why.

To change the text on the card, edit `info()` in `card/card.py` and
open a pull request. The merge draws the card again.

To change the portrait, run `card/portrait.py` on the new picture.
Render the card and check the hair and the blink before you open the
pull request, because the crop, the masks and the eye cells are tuned
to the current photo.

Run the tests from `card/`:

```bash
python3 -m unittest -v
```

<!-- BEGIN shared from mattgrul/repo-template. Change it there. Write this repository's own text outside these lines. -->

Every repository of this account has the rules below. A rule above
them is this repository's own, and it wins when the two disagree.

## Pull Requests

Open a pull request for every change. A ruleset protects `main` and
each `N.x` branch, so do not push to them. A pull request merges by
squash only, and the squash commit takes the pull request title, so
write the title as the change, in one sentence.

Merge a pull request only after its required checks pass, with
`gitleaks-scan` among them. When a required check fails, fix the cause.
Merging past it with `--admin` is the account owner's choice alone.

## Gitleaks Scan

The scan fails on keys, tokens, email addresses and home folder paths,
in the files and in each commit of a pull request. Write paths
relative to the repository, and keep personal data out of files and
commit messages.

- Keep the job name `gitleaks-scan`. The ruleset requires a check of
  that name.
- For one known finding that is not a secret, add a `gitleaks:allow`
  comment on its line, or add the finding to a `.gitleaksignore`.
- Add a `.gitleaks.toml` only when the shared scan rules cannot work.
  It replaces all of them.

## Actions

Pin each action to a full commit SHA, with its version in a comment on
the same line. GitHub refuses a workflow that names an action by tag.
Dependabot moves the SHAs.

The steps of the scan and the release workflow live in
`mattgrul/.github`. A repository that calls them changes them there.

## Dependabot

Follow `docs/agents/dependabot.md` in the same pull request when the
repository adds a package type, such as Composer, npm or Go modules,
or when an `N.x` branch starts or stops getting fixes.

Once CI tests the project, merge a dependency pull request when its
required checks pass. Until then, check it by hand before you merge it.

## Releases

Draft a release with the Release workflow:
`gh workflow run release.yml -f bump=<patch|minor|major>`. It raises
that part of the highest `vX.Y.Z` tag. The account owner publishes
the draft, and publishing creates the tag.

## Agent skills

### Issue tracker

When a skill reads or writes issues, follow
`docs/agents/issue-tracker.md`.

### Triage labels

When a skill names a triage role, take its label from
`docs/agents/triage-labels.md`.

### Domain docs

Before a skill explores the code or names a domain concept, read
`docs/agents/domain.md`.

<!-- END shared from mattgrul/repo-template -->
