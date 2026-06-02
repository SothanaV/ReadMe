# SSH Tools

A helper script that reads `~/.ssh/config` and presents a numbered menu to quickly SSH into a configured host.

## Table of Contents

- [Configure SSH Hosts](#configure-ssh-hosts)
- [Create the Shell Script](#create-the-shell-script)
- [Make the Script Executable](#make-the-script-executable)
- [Run the Script](#run-the-script)
- [Optional: Add to PATH](#optional-add-to-path)

---

## Configure SSH Hosts

Add your hosts to `~/.ssh/config`:

```text
Host home-proxy
    HostName 192.168.68.117
    IdentityFile ~/Desktop/ssh/home/home
    User serveradmin

Host work-server
    HostName 10.0.1.50
    IdentityFile ~/.ssh/id_ed25519
    User deploy
```

---

## Create the Shell Script

Create the script at a convenient location, for example `~/Desktop/ssh/bin/sshpick`:

```bash
#!/usr/bin/env bash

CONFIG="$HOME/.ssh/config"

# Extract hosts (ignores wildcards, Match blocks; includes only Host entries)
HOSTS=$(grep -E '^Host ' "$CONFIG" | grep -v '[*?]' | awk '{for(i=2;i<=NF;i++) print $i}')

if [ -z "$HOSTS" ]; then
    echo "No hosts found in $CONFIG"
    exit 1
fi

echo "Available hosts:"
i=1
declare -A MAP
for host in $HOSTS; do
    echo "  [$i] $host"
    MAP[$i]=$host
    ((i++))
done

read -rp "Select host number to SSH into: " choice

if [ -z "${MAP[$choice]}" ]; then
    echo "Invalid choice"
    exit 1
fi

ssh "${MAP[$choice]}"
```

---

## Make the Script Executable

```bash
chmod 700 ~/Desktop/ssh/bin/sshpick
```

---

## Run the Script

```bash
~/Desktop/ssh/bin/sshpick
```

---

## Optional: Add to PATH

Add the script directory to your shell PATH so you can run `sshpick` from anywhere:

```bash
echo 'export PATH="$HOME/Desktop/ssh/bin:$PATH"' >> "$HOME/.zshrc"
source "$HOME/.zshrc"
```

Then simply run:

```bash
sshpick
```
