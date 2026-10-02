# GPRL Globe

A globe of everyone in the lab. Each person adds one folder; the presenter builds the globe from all of them.

## Adding someone
Each person owns exactly one folder: `people/<github-username>/`, containing:

- `profile.json`, in the same shape as `people/_example/profile.json`:
  - `name`: how they want to appear
  - `city`, `country`: where they're from
  - `lat`, `lon`: that city's coordinates in decimal degrees. Look them up yourself; never ask the person for them.
  - `fun_fact`: in their own words, verbatim
  - `photo`: file name of their photo in the same folder
- their photo, copied into the folder (jpg, png, webp, gif, or svg; under 2 MB)

If anything is missing (GitHub username, name, city, fun fact, photo), ask for it. Don't invent it.

If `python3` is available, run `python3 globe.py --no-open` to check that the profile builds. Its output names any broken profile.

## Rules
- Only create or edit files inside `people/<their-username>/`. Never touch anything else.
- Don't commit or push unless asked. When asked, commit on `main` and push to `origin`.
- Use the GitHub CLI (`gh`) for GitHub steps. If it's missing, install it. If `gh auth status` says they're not logged in, run `gh auth login --web --git-protocol https` in the background, read the one-time code from its output, and tell them to enter it at github.com/login/device. Once it finishes, run `gh auth setup-git` so `git push` can use it.
- `origin` must be their own fork (`github.com/<their-username>/gprl-globe`). Check `git remote get-url origin` first:
  - If it's `GlobalPovertyResearchLab/gprl-globe`, run `gh repo fork --remote` here. Their fork becomes `origin` (and upstream becomes `upstream`).
  - Only if the current folder isn't a gprl-globe clone at all, run `gh repo fork GlobalPovertyResearchLab/gprl-globe --clone`, then work inside `gprl-globe/`.
- After the push, open the pull request for them: `gh pr create --repo GlobalPovertyResearchLab/gprl-globe --head <their-username>:main --title "Add <their-username>" --body ""`, and give them the link.
- `people.js` is generated; never commit it.
