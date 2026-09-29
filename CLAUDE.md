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
- `origin` must be their own fork (`github.com/<their-username>/gprl-globe`). If it points at `GlobalPovertyResearchLab/gprl-globe`, the push will fail: tell them to fork the repo on GitHub and clone their fork.
- After the push, they open a pull request from their fork to `GlobalPovertyResearchLab/gprl-globe` (on the fork's GitHub page: Contribute → Open pull request).
- `people.js` is generated; never commit it.
