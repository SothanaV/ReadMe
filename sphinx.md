# Sphinx
- ref https://towardsdatascience.com/documenting-python-code-with-sphinx-554e1d6c4f6d

1. Install packages
```sh
pip install sphinx sphinx_rtd_theme
```

2. directory structure

```
mylib
 ┣ docs
 ┗ mylib
   ┣ xxx.py
   ┣ yyy.py
```

```
mkdir docs
```

3. setup sphinx
```
sphinx-quickstart
```

- steps
```
> Separate source and build directories (y/n) [n]: n
> Project name: mylib
> Author name(s): sothanav
> Project release []: 0.0.1
> Project language [en]: en
```

4. editing ```conf.py``` file

```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

. . .

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]
. . .
html_theme = 'sphinx_rtd_theme'
. . .
```

5. Generating .rst files
```bash
cd ..
sphinx-apidoc -o docs mylib/
```

6. generating html
```bash
cd docs
make html
```

7. regenerate html
```bash
cd docs
make clean html
make html
```

## script
```bash
echo "Generating docs ..."
sphinx-apidoc -o docs dsmlibrary/
cd docs
make clean html
make html
cd ..
echo "Docs generated !!! "
```