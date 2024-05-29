# How to upload package to Pypi
required
- twine 
```
pip install twine
```

## build package
```
python setup.py sdist
```

## upload to Pypi
```
twine upload dist/<target file> --verbose
```