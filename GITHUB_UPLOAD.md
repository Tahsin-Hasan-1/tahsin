# GitHub Upload Commands

All commands used to stage, commit, and push this project to GitHub.

---

## 1. Check Repository Status

```bash
git status
```
> Shows which files are modified, staged, or untracked.

---

## 2. Check Remote & Commit History

```bash
git remote -v
git log --oneline -5
```
> Verifies the GitHub remote URL and reviews recent commits.

---

## 3. Stage Changed Files

```bash
git add assets/js/main.js contact.html README.md
```
> Stages specific modified files for the commit.

---

## 4. Commit the Changes

```bash
git commit -m "fix: remove exit cmd, hide project page, rename index to home in terminal"
```
> Creates a commit with a descriptive message following conventional commits format.

---

## 5. Push to GitHub

```bash
git push origin main
```
> Pushes the committed changes to the `main` branch on the `origin` remote (GitHub).

---

## ⚠️ Auth Note

If you get a `403 Permission denied` error, your `gh` CLI may be logged into a different account.
Re-authenticate with the correct account:

```bash
gh auth login
```

Select: **GitHub.com → HTTPS → Login with a web browser**  
Go to https://github.com/login/device and enter the one-time code shown.

Then retry:

```bash
git push origin main
```

---

## Full Sequence (copy-paste ready)

```bash
git status
git remote -v
git log --oneline -5
git add assets/js/main.js contact.html README.md
git commit -m "fix: remove exit cmd, hide project page, rename index to home in terminal"
git push origin main
```

---

**Remote:** `https://github.com/Tahsin-Hasan-1/tahsin.git`  
**Branch:** `main`
