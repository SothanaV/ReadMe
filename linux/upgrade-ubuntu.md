# Upgrade Ubuntu to a New Version

Upgrade Ubuntu to the next major release (e.g., 22.04 → 24.04).

## Table of Contents

- [Step 1: Update Current Packages](#step-1-update-current-packages)
- [Step 2: Install the Upgrade Manager](#step-2-install-the-upgrade-manager)
- [Step 3: Run the Release Upgrade](#step-3-run-the-release-upgrade)

---

## Step 1: Update Current Packages

Ensure all installed packages are up to date and clean up obsolete ones before upgrading:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove --purge
```

---

## Step 2: Install the Upgrade Manager

The `update-manager-core` package provides the `do-release-upgrade` tool:

```bash
sudo apt install update-manager-core
```

---

## Step 3: Run the Release Upgrade

Start the interactive upgrade process:

```bash
sudo do-release-upgrade
```

> **Tips:** Run this in a `screen` or `tmux` session so the upgrade continues if your SSH connection drops.
> To upgrade to a development (non-LTS) release, use `sudo do-release-upgrade -d`.
> The process will prompt you to confirm changes and may ask whether to keep or replace configuration files.
