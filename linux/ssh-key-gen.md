# SSH Key Generation and Passwordless Login

Generate an SSH key pair and configure passwordless login to a remote server.

## Table of Contents

- [Generate an SSH Key Pair](#generate-an-ssh-key-pair)
- [Copy the Public Key to the Server](#copy-the-public-key-to-the-server)
- [Connect to the Server](#connect-to-the-server)
- [Grant Passwordless sudo (Optional)](#grant-passwordless-sudo-optional)

---

## Generate an SSH Key Pair

```bash
ssh-keygen -t rsa -b 4096 -N "" -f "<PATH/KEYNAME>"
```

**Flags:**

| Flag    | Description                                         |
|---------|-----------------------------------------------------|
| `-t`    | Key type (`rsa`, `ed25519`, etc.)                   |
| `-b`    | Key size in bits (4096 recommended for RSA)         |
| `-N ""` | Empty passphrase (no passphrase protection)         |
| `-f`    | Output file path and key name                       |

> For better security, `ed25519` is the preferred modern key type:
> `ssh-keygen -t ed25519 -f "<PATH/KEYNAME>"`

---

## Copy the Public Key to the Server

```bash
ssh-copy-id -i <KEY>.pub <USERNAME>@<HOST>
```

This appends the public key to `~/.ssh/authorized_keys` on the remote server.

---

## Connect to the Server

```bash
ssh -i <KEY> <USERNAME>@<HOST>
```

To simplify repeated connections, add an entry to `~/.ssh/config`:

```text
Host myserver
    HostName <HOST>
    User <USERNAME>
    IdentityFile <PATH/TO/KEY>
```

Then connect with just:

```bash
ssh myserver
```

---

## Grant Passwordless sudo (Optional)

Allow the current user to run `sudo` without a password prompt:

```bash
echo "$USER    ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers
```

> Use this carefully. Passwordless sudo removes an important security barrier. Prefer limiting it to specific commands where possible.
