# Move Docker Data Directory to Another Path

Reference: [How to move Docker data directory to another location on Ubuntu](https://www.guguweb.com/2019/02/07/how-to-move-docker-data-directory-to-another-location-on-ubuntu/)

## Table of Contents

- [Stop the Docker Daemon](#stop-the-docker-daemon)
- [Configure the New Data Directory](#configure-the-new-data-directory)
- [Copy Existing Data](#copy-existing-data)
- [Rename the Old Directory](#rename-the-old-directory)
- [Start Docker and Verify](#start-docker-and-verify)
- [Remove the Old Directory](#remove-the-old-directory)

---

## Stop the Docker Daemon

```bash
sudo service docker stop
```

---

## Configure the New Data Directory

Create or edit `/etc/docker/daemon.json` and set the `data-root` path:

```bash
sudo nano /etc/docker/daemon.json
```

Add the following content (replace the path with your target location):

```json
{
  "data-root": "/path/to/your/docker"
}
```

---

## Copy Existing Data

Use `rsync` to copy the current Docker data directory to the new location, preserving all permissions and attributes:

```bash
sudo rsync -aP /var/lib/docker/ /path/to/your/docker
```

---

## Rename the Old Directory

Rename the original directory as a backup before starting Docker with the new path:

```bash
sudo mv /var/lib/docker /var/lib/docker.old
```

---

## Start Docker and Verify

Start the Docker daemon and confirm that your containers and images are intact:

```bash
sudo service docker start
```

Run a quick sanity check:

```bash
docker ps
docker images
```

---

## Remove the Old Directory

Once you have confirmed everything works correctly, delete the old data directory:

```bash
sudo rm -rf /var/lib/docker.old
```
