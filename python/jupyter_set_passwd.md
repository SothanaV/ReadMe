# Set a Jupyter Notebook Password

## Table of Contents

- [Step 1: Create the Config File](#step-1-create-the-config-file)
- [Step 2: Generate a Hashed Password](#step-2-generate-a-hashed-password)
- [Step 3: Copy the Hash into the Config File](#step-3-copy-the-hash-into-the-config-file)
- [Step 4: Mount the Config in Docker Compose](#step-4-mount-the-config-in-docker-compose)
- [Launch Command](#launch-command)

---

## Step 1: Create the Config File

Create a file named `jupyter_notebook_config.json`:

```json
{
    "NotebookApp": {
        "password": "<HASHED_PASSWORD>"
    }
}
```

---

## Step 2: Generate a Hashed Password

Run the following in a Python shell:

```python
from notebook.auth import passwd

passwd()
# Enter password:
# Verify password:
# Returns: 'argon2:...' or 'sha1:...'
```

Copy the returned hash string.

---

## Step 3: Copy the Hash into the Config File

Replace `<HASHED_PASSWORD>` in `jupyter_notebook_config.json` with the hash generated in Step 2.

---

## Step 4: Mount the Config in Docker Compose

```yaml
services:
  notebook:
    # ...
    volumes:
      # ...
      - ./jupyter_notebook_config.json:/config/jupyter_notebook_config.json
```

---

## Launch Command

Start Jupyter Notebook with the password config applied:

```bash
jupyter notebook \
  --allow-root \
  --no-browser \
  --ip=* \
  --config=/config/jupyter_notebook_config.json
```
