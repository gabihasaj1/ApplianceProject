# Open, run, commit, and share

## On Ashley's Mac: use the prepared folder
Open VS Code > File > Open Folder and choose this ApplianceProject folder.
Install the Microsoft Python extension. Open Terminal > New Terminal.
Follow the five commands in README.md, then choose the .venv Python interpreter
(Command-Shift-P > Python: Select Interpreter).

## Understand Git
A commit records a snapshot on your computer. A push uploads committed work to GitHub.
The configured group remote should be:
https://github.com/gabihasaj1/ApplianceProject.git

Check existing setup before initializing anything:
```sh
git status
git remote -v
git log -1 --oneline
```
If this folder already has an initial commit and origin, do not reinitialize it.
To upload an existing local main commit:
```sh
git push -u origin main
```
Sign in to the GitHub account with collaborator access when VS Code prompts.
If access is denied, Gabi (repository owner) must invite your account and you must
accept. Never paste a token into source files or a remote URL.

## If using the ZIP (which has no .git directory)
Safest approach: in VS Code run “Git: Clone” from the command palette, paste the
repository URL, choose a folder, and open the clone. Copy the ZIP's project CONTENTS
into the clone, including .gitignore and .vscode. Do not overwrite teammates' changed
files if the repository already contains work; compare those changes first.
For an empty clone:
```sh
git add .
git commit -m "Add data preparation pipeline and team setup"
git branch -M main
git push -u origin main
```
If Git asks for identity, configure your real name and your verified GitHub email
(or GitHub-provided no-reply email) with `git config user.name` and `git config user.email`.
Do not use example identities. No force push is needed.

## Future changes (after initial main is published)
```sh
git switch main
git pull --ff-only
git switch -c ashley/data-preparation-updates
# Edit files and run preparation/tests.
git add src docs tests README.md requirements.txt reports data/raw/source_metadata.json data/processed/feature_config.json
git commit -m "Describe the preparation changes"
git push -u origin ashley/data-preparation-updates
```
Open the group repository on GitHub and create a pull request for review.
If a push is rejected because someone else updated main, do not force push: fetch
and inspect the remote changes before integrating them.

## Teammates
Clone the group repository, open its folder in VS Code, run README.md setup, then
read docs/HANDOFF.md. Each person should use a separate branch for their work.

Official setup references:
- https://code.visualstudio.com/docs/python/python-tutorial
- https://docs.github.com/en/get-started/git-basics/set-up-git
