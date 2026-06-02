# Linux Command Reference

## Table of Contents

- [File and Directory Listing](#file-and-directory-listing)
- [Networking](#networking)
- [Manual Pages](#manual-pages)
- [File Timestamps](#file-timestamps)
- [Text Editors](#text-editors)
- [File Management](#file-management)
- [Disk Operations](#disk-operations)
- [Permissions and Ownership](#permissions-and-ownership)

---

## File and Directory Listing

```bash
ls          # List files and directories
ls -l       # List with detailed (long) format
ls -a       # List all files including hidden files
ls -h       # List with human-readable file sizes (combine with -l: ls -lh)
```

---

## Networking

```bash
ip addr     # Show IP addresses and network interface names
ifconfig    # Legacy tool equivalent to ipconfig on Windows (may need net-tools installed)
```

---

## Manual Pages

```bash
man <command>   # Display the manual page for a command
# Example:
man ls          # Show the manual page for the ls command
```

---

## File Timestamps

```bash
touch <file>    # Create an empty file or update the timestamp of an existing file
```

---

## Text Editors

### Vim

```bash
vim <file>      # Open a file in Vim
```

Common Vim key bindings:

| Key      | Action                        |
|----------|-------------------------------|
| `i`      | Enter insert mode             |
| `Esc`    | Return to normal mode         |
| `dw`     | Delete a word                 |
| `dd`     | Delete a line                 |
| `:w`     | Write (save) the file         |
| `:q`     | Quit                          |
| `:wq`    | Save and quit                 |
| `:q!`    | Quit without saving           |

### Nano

```bash
nano <file>     # Open a file in Nano
```

Common Nano shortcuts: `Ctrl+O` to save, `Ctrl+X` to exit.

---

## File Management

```bash
cp <src> <dst>          # Copy a file
cp -r <src> <dst>       # Copy a directory recursively
mv <src> <dst>          # Move or rename a file or directory

scp <src> <user>@<host>:<dst>   # Securely copy a file to a remote server
scp <user>@<host>:<src> <dst>   # Securely copy a file from a remote server

pwd                     # Print the current working directory
tree                    # Show the directory tree structure

cd <directory>          # Change to the specified directory
cd -                    # Switch back to the previous directory

echo <text>             # Print text to standard output
less <file>             # View file contents interactively (press G to go to end, g to go to top)
```

---

## Disk Operations

### Write a disk image with `dd`

```bash
dd if=<input> of=<output>
# Example: copy an ISO to a USB drive
dd if=ubuntu.iso of=/dev/sdb bs=4M status=progress
```

### Mount a block device

```bash
udisksctl mount -b /dev/<partition>
# Example:
udisksctl mount -b /dev/sdb1
```

---

## Permissions and Ownership

### Change ownership recursively

```bash
sudo chown -R <user>:<group> <directory>
# Example:
sudo chown -R naii:naii /home/naii/data
```

### Change file permissions

```bash
chmod <mode> <file>
# Example: give owner read/write/execute, group and others read/execute
chmod 755 script.sh
```
