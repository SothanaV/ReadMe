# Generating Python Documentation with Sphinx

Reference: <https://towardsdatascience.com/documenting-python-code-with-sphinx-554e1d6c4f6d>

## Table of Contents

- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Initialize Sphinx](#initialize-sphinx)
- [Configure conf.py](#configure-confpy)
- [Generate RST Files](#generate-rst-files)
- [Build HTML Docs](#build-html-docs)
- [Rebuild HTML Docs](#rebuild-html-docs)
- [Build Script](#build-script)

---

## Installation

```bash
pip install sphinx sphinx_rtd_theme
```

---

## Directory Structure

Your project should look like this before starting:

```text
mylib/
 ├── docs/
 └── mylib/
     ├── xxx.py
     └── yyy.py
```

Create the `docs` directory if it does not exist:

```bash
mkdir docs
```

---

## Initialize Sphinx

```bash
sphinx-quickstart
```

Answer the prompts as follows:

```text
> Separate source and build directories (y/n) [n]: n
> Project name: mylib
> Author name(s): sothanav
> Project release []: 0.0.1
> Project language [en]: en
```

---

## Configure conf.py

Edit `docs/conf.py`:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# ...

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

# ...

html_theme = 'sphinx_rtd_theme'
```

---

## Generate RST Files

Run from the project root (one level above `docs/`):

```bash
sphinx-apidoc -o docs mylib/
```

---

## Build HTML Docs

```bash
cd docs
make html
```

---

## Rebuild HTML Docs

Clean the previous build before regenerating:

```bash
cd docs
make clean html
make html
```

---

## Build Script

Save as a shell script to automate the full rebuild:

```bash
#!/bin/bash
echo "Generating docs ..."
sphinx-apidoc -o docs dsmlibrary/
cd docs
make clean html
make html
cd ..
echo "Docs generated!"
```
