# Git Commands Reference Guide

## Commands Used to Push EBYPTABL Project to GitHub

### 1. Check Git Status
```bash
git status
```
**Purpose:** Check if the directory is a git repository and see the current state of files (tracked, untracked, modified, staged).

**Output:** Shows which files are staged, unstaged, or untracked. In our case, it showed "fatal: not a git repository" because we hadn't initialized git yet.

---

### 2. Initialize Git Repository
```bash
git init
```
**Purpose:** Creates a new Git repository in the current directory by creating a hidden `.git` folder that tracks all changes.

**Output:** "Initialized empty Git repository in C:/Users/SUSHILDAS/Desktop/Learning IBM/POC/EBYPTABL/.git/"

---

### 3. Add Files to Staging Area
```bash
git add .
```
**Purpose:** Stages all files in the current directory and subdirectories for commit. The `.` means "all files".

**Alternative commands:**
- `git add filename.txt` - Add a specific file
- `git add *.py` - Add all Python files
- `git add folder/` - Add all files in a folder

---

### 4. Create a Commit
```bash
git commit -m "Initial commit: EBYPTABL analyzer project"
```
**Purpose:** Saves the staged changes to the local repository with a descriptive message.

**Breakdown:**
- `git commit` - Creates a commit
- `-m` - Flag to add a message inline
- `"message"` - The commit message describing what changed

**Output:** Shows 7 files changed with 42,781 insertions (lines added).

---

### 5. Add Remote Repository
```bash
git remote add origin https://github.com/sushildas5581/EBYPTABL.git
```
**Purpose:** Links your local repository to a remote repository on GitHub.

**Breakdown:**
- `git remote add` - Adds a new remote repository
- `origin` - The default name for the remote (you can use any name, but "origin" is convention)
- `URL` - The GitHub repository URL

**To view remotes:**
```bash
git remote -v
```

---

### 6. Push to GitHub
```bash
git push -u origin master
```
**Purpose:** Uploads your local commits to the remote GitHub repository.

**Breakdown:**
- `git push` - Sends commits to remote repository
- `-u` - Sets upstream tracking (links local branch to remote branch)
- `origin` - The name of the remote repository
- `master` - The branch name to push to

**After first push with `-u`, you can simply use:**
```bash
git push
```

---

## Common Git Workflow for Future Updates

### Daily Workflow
```bash
# 1. Check what files changed
git status

# 2. Stage your changes
git add .
# or add specific files
git add filename.py

# 3. Commit with a message
git commit -m "Description of changes"

# 4. Push to GitHub
git push
```

---

## Additional Useful Git Commands

### View Commit History
```bash
git log
```
Shows all commits with author, date, and message.

```bash
git log --oneline
```
Shows condensed commit history (one line per commit).

---

### View Changes Before Committing
```bash
git diff
```
Shows what changed in unstaged files.

```bash
git diff --staged
```
Shows what changed in staged files.

---

### Undo Changes

**Unstage a file (keep changes):**
```bash
git reset filename.txt
```

**Discard changes in a file:**
```bash
git checkout -- filename.txt
```

**Undo last commit (keep changes):**
```bash
git reset --soft HEAD~1
```

**Undo last commit (discard changes):**
```bash
git reset --hard HEAD~1
```

---

### Branch Management

**Create a new branch:**
```bash
git branch feature-name
```

**Switch to a branch:**
```bash
git checkout feature-name
```

**Create and switch in one command:**
```bash
git checkout -b feature-name
```

**List all branches:**
```bash
git branch
```

**Merge a branch into current branch:**
```bash
git merge feature-name
```

**Delete a branch:**
```bash
git branch -d feature-name
```

---

### Pull Changes from GitHub

**Fetch and merge changes:**
```bash
git pull
```

**Fetch without merging:**
```bash
git fetch
```

---

### Clone a Repository

**Clone from GitHub:**
```bash
git clone https://github.com/username/repository.git
```

---

## .gitignore File

The `.gitignore` file tells Git which files to ignore (not track).

**Common patterns:**
```
# Python
__pycache__/
*.pyc
*.pyo
venv/
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## Git Configuration

**Set your name:**
```bash
git config --global user.name "Your Name"
```

**Set your email:**
```bash
git config --global user.email "your.email@example.com"
```

**View configuration:**
```bash
git config --list
```

---

## Troubleshooting

### Authentication Issues
If you get authentication errors when pushing:

1. **Use Personal Access Token (PAT):**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate new token with repo permissions
   - Use token as password when prompted

2. **Use SSH instead of HTTPS:**
   ```bash
   git remote set-url origin git@github.com:username/repository.git
   ```

### Merge Conflicts
If you get merge conflicts:
1. Open the conflicted files
2. Look for conflict markers: `<<<<<<<`, `=======`, `>>>>>>>`
3. Edit the file to resolve conflicts
4. Stage and commit the resolved files

---

## Best Practices

1. **Commit often** - Make small, logical commits
2. **Write clear commit messages** - Describe what and why, not how
3. **Pull before push** - Always pull latest changes before pushing
4. **Use branches** - Create feature branches for new work
5. **Review before commit** - Use `git diff` to review changes
6. **Don't commit sensitive data** - Use .gitignore for secrets, API keys, etc.

---

## Quick Reference Card

| Command | Purpose |
|---------|---------|
| `git init` | Initialize repository |
| `git status` | Check status |
| `git add .` | Stage all files |
| `git commit -m "msg"` | Commit changes |
| `git push` | Push to remote |
| `git pull` | Pull from remote |
| `git clone URL` | Clone repository |
| `git branch` | List branches |
| `git checkout -b name` | Create & switch branch |
| `git merge name` | Merge branch |
| `git log` | View history |
| `git diff` | View changes |

---

## Your Project Setup Summary

**Repository:** https://github.com/sushildas5581/EBYPTABL.git  
**Branch:** master  
**Files committed:** 7 files (42,781 lines)

**Files in repository:**
- .gitignore
- CODE_EXPLANATION.md
- EBYPSHEET.xlsx
- EBYPTABL.TXT
- README.md
- ebyptabl_analyzer.py
- requirements.txt

---

*Created: April 5, 2026*  
*For: EBYPTABL Project*