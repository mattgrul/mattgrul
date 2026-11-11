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

<!-- BEGIN shared text. Change it in the template repository. Write this repository's own text outside these lines. -->

Every repository of this account has the rules below. A rule above
them is this repository's own, and it wins when the two disagree.

## Pull Requests

Open a pull request for every change. A ruleset protects `main` and
each `N.x` branch, so do not push to them. A pull request merges by
squash only, and the squash commit takes the pull request title, so
write the title as the change, in one sentence.

Merge a pull request only after every check on it passes, not only
the required ones. The ruleset requires `gitleaks-scan` in every
repository. When a check fails, fix the cause.

## Shared Text

The text between the `BEGIN shared text` and `END shared text` marker
lines is the same in every repository of this account. It is in
`AGENTS.md`, in each file in `docs/agents/` and in
`.github/dependabot.yml`.

- Write text that only this repository needs outside the markers:
  above them in `AGENTS.md`, below them in the other files.
- Change the shared text only in the template repository. In any
  other repository the next sync replaces the change, so propose it
  to the account owner instead.
- In the template repository, a change to the shared text reaches
  every repository at the next sync. Make it only when it holds true
  for all of them, and say so in the pull request. After the merge,
  the account owner runs the sync.

## Public Text

Public repositories carry the shared text. Each new repository also
starts with a copy of every file in the template repository. A later
commit cannot take text out of that history. So in the shared text and
in the template, name no private repository and no person, and give no
detail of a check or a setting that shows a way past it. Name a public
repository only where a file or its reader needs the name.

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

## Checks Workflow

Run the checks of the repository's own code, such as its tests and
its linters, in `.github/workflows/checks.yml`. Name the workflow
`checks`. Keep the scan in its own workflow. A repository with no
checks of its own has no `checks` workflow.

- Name the required job `checks`. The ruleset requires a check of
  that name in each repository that has the workflow, and GitHub
  names a check after its job. Do not rename the job, because the
  ruleset then waits for a check that never reports.
- When the checks need more than one job, make `checks` the last job.
  It waits for the others and fails when one of them fails, so the
  ruleset requires one name only:

  ```yaml
  checks:
    needs: [lint, unit]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - if: contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled')
        run: exit 1
  ```

  Keep `if: always()`. Without it, a failed job does not fail
  `checks`.

## Actions

Pin each action to a full commit SHA, with its version in a comment on
the same line. GitHub refuses a workflow that names an action by tag.
Dependabot moves the SHAs.

The steps of the scan and the release workflow live in the repository
that the workflows call. Change them there.

## Dependabot

Follow `docs/agents/dependabot.md` in the same pull request when the
repository adds a package type, such as Composer, npm or Go modules,
or when an `N.x` branch starts or stops getting fixes.

Once CI tests the project, merge a dependency pull request when its
checks pass. Until then, check it by hand before you merge it.

## Releases

Draft a release with the Release workflow:
`gh workflow run release.yml -f bump=<patch|minor|major>`. It raises
that part of the highest `vX.Y.Z` tag. To release from an `N.x`
branch, add `--ref N.x`. The workflow then raises the highest
`vN.Y.Z` tag, and it refuses `major`. The account owner publishes the
draft, and publishing creates the tag.

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

<!-- END shared text -->
