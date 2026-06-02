# Upload a Package to PyPI

## Table of Contents

- [Prerequisites](#prerequisites)
- [Build the Package](#build-the-package)
- [Upload to PyPI](#upload-to-pypi)

---

## Prerequisites

Install `twine`:

```bash
pip install twine
```

---

## Build the Package

```bash
python setup.py sdist
```

This creates a source distribution under the `dist/` directory.

---

## Upload to PyPI

```bash
twine upload dist/<target_file> --verbose
```

You will be prompted for your PyPI username and password (or an API token).

> **Tip:** To avoid entering credentials each time, create a `~/.pypirc` file or set the `TWINE_USERNAME` and `TWINE_PASSWORD` environment variables.
