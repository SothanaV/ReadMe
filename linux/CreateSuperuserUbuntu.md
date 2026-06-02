# Create a Superuser on Ubuntu

## Table of Contents

- [Create a New User](#create-a-new-user)
- [Grant sudo Privileges](#grant-sudo-privileges)
- [Change a User Password](#change-a-user-password)

---

## Create a New User

```bash
sudo adduser <username>
```

Follow the prompts to set a password and fill in optional user information.

---

## Grant sudo Privileges

Add the user to the `sudo` group:

```bash
sudo usermod -aG sudo <username>
```

Verify the user's groups:

```bash
groups <username>
```

---

## Change a User Password

```bash
sudo passwd <username>
```

> The original file had a typo (`psswd`). The correct command is `passwd`.

To change your own password (no sudo required):

```bash
passwd
```
