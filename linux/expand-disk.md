# Expand disk
### 1. grow patiton
```
growpart <disk> <partition number>

# eg
## growpart /dev/sda 1
```

### 2. stop service
stop service running in disk

### 3. resize

```
resize2fs <disk point>

# eg
## resize2fs /dev/sda1
```

## If logical volume

Resize the Physical Volume (PV)
```
sudo pvresize <disk point>

# eg
## sudo pvresize /dev/sda3
```

Extend the Logical Volume (LV)

```
sudo lvextend -l +100%FREE <mount point>

# eg
## sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
```

Resize Filesystem
```
sudo resize2fs <mount point>

# eg
## sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
```