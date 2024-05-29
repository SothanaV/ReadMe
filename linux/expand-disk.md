# Expand disk
### 1. grow patiton
```
growpart <disk> <partition number>
```

eg
```
growpart /dev/sda 1
```

### 2. stop service
stop service running in disk

### 3. resize

```
resize2fs <disk point>
```

eg
```
resize2fs /dev/sda1
```