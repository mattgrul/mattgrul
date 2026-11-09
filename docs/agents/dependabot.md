<!-- BEGIN shared text. Change it in the template repository. Write this repository's own text outside these lines. -->
# Dependabot Entries

## Adding a Package Type

Add an entry to `.github/dependabot.yml`. Put it after the
`# END shared text` marker line, with one blank line before it.

```yaml
  - package-ecosystem: composer
    directory: /
    schedule:
      interval: weekly
    cooldown:
      default-days: 7
    groups:
      composer:
        patterns:
          - "*"
        update-types:
          - minor
          - patch
    labels:
      - dependencies
```

Replace `composer` with the ecosystem name, in both places.

## `N.x` Branches

To keep an `N.x` branch such as `1.x` current, add a copy of each
entry with `target-branch: 1.x`, after the END line. Delete those
copies when the branch gets no more fixes.
<!-- END shared text -->
