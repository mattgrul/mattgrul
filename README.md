# repo-template

The starting point for a new repository of this account. A new
repository starts as a copy of it, so it has the Gitleaks scan, the
release workflow, Dependabot and the agent instructions from its first
commit.

| File | What it does |
|---|---|
| `.github/workflows/gitleaks-scan.yml` | Runs the required check `gitleaks-scan`. |
| `.github/workflows/release.yml` | Drafts a release when you run it. |
| `.github/dependabot.yml` | Keeps the dependencies current. It starts with one entry, for the pinned actions. |
| `AGENTS.md` | Says how to change the repository: pull requests, the scan, pinned actions, Dependabot and releases. |
| `docs/agents/` | Tells the engineering skills where the issues, the triage labels and the domain docs are, and holds the Dependabot entry to add. |

The account's settings repository starts each new repository from
this one, then replaces this README with one that holds the
repository's name alone. Every other file stays as it is, so write
each one to hold true in any repository.

GitHub copies every file here into the first commit of each new
repository, this README too, and a public repository shows that commit
to anyone. So name no private repository here, and link to none: a
later commit cannot take the name out of that history.

## Shared Text

`AGENTS.md` and each file in `docs/agents/` hold text that every
repository shares, between two marker lines:

```markdown
<!-- BEGIN shared from mattgrul/repo-template. Change it there. Write this repository's own text outside these lines. -->
...
<!-- END shared from mattgrul/repo-template -->
```

A repository writes its own text outside the markers: in `AGENTS.md`
above them, in `docs/agents/` below them. Change the shared text here
only. Then run the shared text sync in the settings repository.
It opens a pull request in each repository you choose, and changes
only the text between the markers.

## Workflows

### Gitleaks Scan

`gitleaks-scan.yml` runs the [shared scan](https://github.com/mattgrul/.github/tree/main/gitleaks-scan) from
`mattgrul/.github` on every pull request and on every push to `main` or
an `N.x` branch. The scan looks for keys, tokens, email addresses and
home folder paths. It reads the files, and on a pull request also the
commits the pull request adds, because a secret removed in a later
commit is still in the history.

The job is named `gitleaks-scan`, and GitHub
[names the check after the job](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idname). The ruleset that
the settings repository sets requires a check of that name by default. Only the
owner can merge a pull request before the check passes.

### Release

`release.yml` calls the [shared release workflow](https://github.com/mattgrul/.github/blob/main/.github/workflows/release.yml) in
`mattgrul/.github`.

1. Open the Actions tab, choose **Release**, and choose the part of the
   version to raise: `patch`, `minor` or `major`.
2. The workflow reads the highest `vX.Y.Z` tag, raises that part, and
   drafts a release. GitHub [writes the notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes) from the
   pull requests merged since the last release.
3. Review the draft on the Releases page and publish it. Publishing
   creates the tag.

It runs from `main` or an `N.x` branch only. It commits nothing. The
shared workflow gets [no more permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#access-and-permissions-for-nested-workflows) than
the calling job grants.

## Dependabot

### The Three Parts

| Part | What it does | Turned on by |
|---|---|---|
| [Alerts](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts) | Warns of a known vulnerability in a dependency. | A repository setting. It never reads `dependabot.yml`. |
| [Security updates](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-security-updates) | Opens a pull request that fixes an alert. | A repository setting. It reads some settings in `dependabot.yml`. |
| [Version updates](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates) | Opens pull requests that keep dependencies current. | `dependabot.yml` only. |

The settings repository turns alerts and security updates on for every repository
it manages.

### Settings

Each setting in `dependabot.yml`, the parts of Dependabot that use it,
and its entry in the [options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference):

| Setting | What it does here | Used by |
|---|---|---|
| [`package-ecosystem`](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#package-ecosystem-) | `github-actions`: updates the actions that the workflows use. | Version updates |
| [`directory`](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#directories-or-directory--) | `/`: for actions, Dependabot reads `.github/workflows`. | Version updates, security updates |
| [`schedule`](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#schedule-) | Checks every day at 06:00 UTC. | Version updates |
| [`cooldown`](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#cooldown-) | Waits seven days for a new release, except from `mattgrul`. | Version updates |
| [`groups`](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#groups--) | Puts minor and patch updates in one pull request. | Version updates, because the group sets no `applies-to` |
| [`labels`](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#labels--) | Gives each pull request only the label `dependencies`. | Version updates, security updates |

### Pinned Actions

Each workflow pins an action to a commit SHA, with the version in a
comment on the same line:

```yaml
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
```

A tag such as `v7` can be moved to other code, by the owner or by an
attacker, and the next run then runs that code with no pull request. A
SHA names one commit, and nobody can change it, so GitHub
[advises SHA pins](https://docs.github.com/en/actions/reference/security/secure-use#using-third-party-actions). The settings repository sets
[`sha_pinning_required`](https://docs.github.com/en/rest/actions/permissions#set-github-actions-permissions-for-a-repository), so GitHub refuses a
workflow that names an action by tag.

| | Tag pin `@v7` | SHA pin `@3d3c42e…` |
|---|---|---|
| Nobody can change what runs | no | yes |
| Alerts | yes | no |
| Security updates | yes | no, because no alert starts one |
| Version updates | yes | yes |

GitHub [raises alerts](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts#limitations) only for actions that name
a version, not a SHA. The docs tie alerts to the reference after the
`@`, not to the comment, so the comment does not bring them back.
[Version updates](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions) still work. Dependabot finds a new
version through the tags of the action's repository, changes the SHA,
and updates the comment.

### Cooldown

With no alerts, the [cooldown](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#cooldown-) is the protection.
Dependabot offers a new release only when it is seven days old, so a
bad release has time to be found and pulled first. A fix for a
vulnerable action waits as long. Releases from `mattgrul`'s own
repositories skip the cooldown, so a change to the shared scan or
release workflow arrives on the next run.

### Pull Requests

- Minor and patch updates [share one pull request](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#groups--).
- A major update gets its own, because it can need a change here.
- Every pull request has the one label `dependencies`. The settings repository
  deletes any label it does not name, and Dependabot would otherwise
  [add an ecosystem label](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#labels--) too.
- The actions entry checks every day at 06:00 UTC, weekends too. It
  uses a `cron` schedule, because [`daily` runs on weekdays
  only](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#schedule-).

### Adding a Package Type

Dependabot does not find package types by itself, and the docs [require a manifest](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#directories-or-directory--) in the
repository for each entry. So the template holds only the actions
entry. `docs/agents/dependabot.md` holds the entry to add when the
repository adds a package type.

Unlike actions, most package types record a version number, often in
a lock file, so they get alerts and
[security updates](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-security-updates) with or without an entry. The
entry turns on version updates. It also gives a security update the
label `dependencies`. Without it, a security update gets the default
ecosystem label, which the settings repository deletes.

That entry makes choices for this account, not Dependabot rules:

- **Every package entry gets version updates, even before CI tests
  the project.** Small, regular updates are easy to review. If version
  updates stay off for a long time, the next update is a large jump,
  and a security fix that needs a newer major version cannot be made
  automatically. Until a test job exists, nothing proves that an
  update works.
- **Package entries check `weekly`.** The actions entry checks every
  day so that a release from `mattgrul`'s own repositories arrives
  quickly. Packages have no such reason, and weekly gives fewer pull
  requests. Security updates ignore the schedule.

### `N.x` Branches

Each part of Dependabot uses the default branch:

| Part | Branch |
|---|---|
| Alerts | Default branch only |
| Security updates | Default branch only |
| Version updates | Default branch, or one other branch per entry |

Alerts [scan the default branch](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts), and security updates start
from alerts. Version updates keep a branch such as `1.x` current only
through a second entry with
[`target-branch`](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#target-branch-). `docs/agents/dependabot.md` says how to add it.

Nothing warns of a vulnerability on `1.x`. When an alert fires on the
default branch, check `1.x` by hand. If the default branch already has
the fixed version, no alert fires, even when `1.x` still has the
vulnerable one.
