# SSH Tools
- tools for help easy ssh

0. config `$HOME/.ssh/config"`
example 
```
...
Host home-proxy
    HostName 192.168.68.117
    IdentityFile ~/Desktop/ssh/home/home
    User serveradmin
...
```

1. create shell script eg `/Users/sothanav/Desktop/ssh/bin`
```bash
#!/usr/bin/env bash

CONFIG="$HOME/.ssh/config"

# Extract hosts (ignores wildcards, Match blocks, includes only Host entries)
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

read -p "Select host number to SSH: " choice

if [ -z "${MAP[$choice]}" ]; then
    echo "Invalid choice"
    exit 1
fi

ssh "${MAP[$choice]}"
```

2. change to executeable
```bash
chmod 700 /Users/sothanav/Desktop/ssh/bin
```

3. use it's

./shell

## Optional
add to path
```
echo 'export PATH="/Users/sothanav/Desktop/ssh/bin:$PATH"' >> $HOME/.zshrc
```

can use every where
```
shell
```