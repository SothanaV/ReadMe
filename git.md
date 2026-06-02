# Git Usage Guide

## Table of Contents

- [Clone](#clone)
- [Push](#push)
- [Pull](#pull)
- [Checkout](#checkout)
- [Branch](#branch)
- [Merge](#merge)
- [Log and Diff](#log-and-diff)
- [Reset and Revert](#reset-and-revert)
- [Stash](#stash)
- [Tag](#tag)
- [Remote](#remote)
- [Configure](#configure)
- [Useful Commands](#useful-commands)
- [Git Flow](#git-flow)
- [References](#references)

---

## Clone

Clone a repository from GitHub or GitLab:

```bash
git clone <git-url>
```

---

## Push

Stage, commit, and push changes to a remote repository:

```bash
# Check working tree status
git status

# Stage files
git add <file1> <file2>   # Add specific files
git add -A                # Add all changes
git add *.py              # Add files matching a pattern

# Commit staged changes
git commit -m "<message>"

# Push to remote
git push
git push origin <branch-name>   # Push to a specific branch
```

---

## Pull

Fetch and merge changes from a remote repository:

```bash
git pull
git pull origin <branch-name>   # Pull from a specific branch
```

---

## Checkout

Switch to an existing branch or create a new one:

```bash
git checkout <branch-name>

# Create and switch to a new branch
git checkout -b <branch-name>
```

---

## Branch

Manage local and remote branches:

```bash
# List branches
git branch            # Local branches
git branch -a         # All branches (local + remote)
git branch -r         # Remote branches only

# Create a branch without switching to it
git branch <branch-name>

# Delete a branch
git branch -d <branch-name>   # Delete only if already merged
git branch -D <branch-name>   # Force delete

# Rename a branch
git branch -m <new-name>                  # Rename current branch
git branch -m <old-name> <new-name>       # Rename a specific branch
```

---

## Merge

Merge one branch into another:

```bash
git checkout <target-branch>
git merge <source-branch>

# Merge with an explicit merge commit (no fast-forward)
git merge --no-ff <source-branch>

# Abort an in-progress merge
git merge --abort
```

---

## Log and Diff

Inspect commit history and changes:

```bash
# View commit history
git log
git log --oneline             # Condensed one-line format
git log --oneline --graph     # With branch graph
git log --all --graph         # All branches with graph

# View uncommitted changes
git diff                      # Unstaged changes
git diff --staged             # Staged changes not yet committed
git diff <commit1> <commit2>  # Compare two commits

# Inspect a specific commit
git show <commit-hash>

# View history for a specific file
git log -- <file-path>
```

---

## Reset and Revert

Undo changes at different levels:

```bash
# Soft reset — moves HEAD, keeps changes staged
git reset --soft <commit-hash>

# Mixed reset — moves HEAD, keeps changes in working directory (default)
git reset --mixed <commit-hash>

# Hard reset — moves HEAD and discards all changes
git reset --hard <commit-hash>

# Revert — creates a new commit that undoes the specified commit
git revert <commit-hash>
```

---

## Stash

Temporarily shelve changes without committing:

```bash
# Save current changes to the stash
git stash
git stash save "description"   # Stash with a label

# List all stash entries
git stash list

# Restore stashed changes
git stash pop           # Apply most recent stash and remove it
git stash apply         # Apply most recent stash but keep it

# Apply a specific stash entry
git stash apply stash@{0}

# Delete stash entries
git stash drop stash@{0}   # Remove a specific entry
git stash clear            # Remove all entries
```

---

## Tag

Mark specific commits with version labels:

```bash
# List all tags
git tag

# Create a lightweight tag
git tag <tag-name>

# Create an annotated tag with a message
git tag -a v1.0 -m "Version 1.0"

# Push a tag to remote
git push origin <tag-name>
git push origin --tags        # Push all tags

# Check out a tag (detached HEAD state)
git checkout <tag-name>
```

---

## Remote

Manage remote repository connections:

```bash
# List remotes with URLs
git remote -v

# Add a new remote
git remote add origin <git-url>

# Change the URL of an existing remote
git remote set-url origin <new-git-url>

# Remove a remote
git remote remove origin

# Inspect a remote
git remote show origin
```

---

## Configure

Set up global and local Git configuration:

```bash
# Set user identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# View all global configuration
git config --global --list

# Cache credentials on disk
git config credential.helper store

# Set default editor for commit messages
git config --global core.editor "nano"
git config --global core.editor "code --wait"   # VS Code

# Disable SSL verification (not recommended for production)
git config --global http.sslVerify false

# Handle line endings on Windows
git config --global core.autocrlf true
```

---

## Useful Commands

```bash
# Short status output
git status -s

# Show the most recent commit
git log -1

# Show the last 5 commits (condensed)
git log -5 --oneline

# Count and display repository object sizes
git count-objects -vH

# Preview what would be removed by clean
git clean -n

# Remove untracked files
git clean -f

# Remove untracked files and directories
git clean -fd
```

---

## Git Flow

A basic feature branch workflow:

```bash
# 1. Sync with the latest main branch
git pull origin main

# 2. Create a feature branch
git checkout -b feature/my-feature

# 3. Make changes and commit
git add .
git commit -m "feat: add new feature"

# 4. Push the feature branch to remote
git push origin feature/my-feature

# 5. Merge back into main (typically via a Pull Request)
git checkout main
git pull origin main
git merge feature/my-feature
git push origin main
```

---

## References

- [Git Official Documentation](https://git-scm.com/doc)
- [StackOverflow — Caching Git Credentials](https://stackoverflow.com/questions/5343068/is-there-a-way-to-cache-https-credentials-for-pushing-commits)
