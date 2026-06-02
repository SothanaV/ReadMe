# Tesseract OCR

> **Archived** — Instructions for installing and using Tesseract OCR with Python.

## Installation

### Install Tesseract Engine

```bash
sudo apt-get install tesseract-ocr -y
```

### Install Python Bindings

```bash
pip install pillow pytesseract
```

### Verify Installation

```bash
tesseract -v
```

## Command-Line Usage

### Extract Text from an Image

```bash
tesseract tesseract_inputs/example_01.png stdout
```

### Extract Digits Only

```bash
tesseract tesseract_inputs/example_03.png stdout digits
```

### Save Output to a File

```bash
tesseract input.png output
# Output is saved as output.txt
```

## Python Usage

```python
from PIL import Image
import pytesseract

# Extract text from an image file
image = Image.open("example_01.png")
text = pytesseract.image_to_string(image)
print(text)

# Extract digits only
digits = pytesseract.image_to_string(image, config="--psm 6 digits")
print(digits)
```

## Language Data Files

Tesseract supports multiple languages. Download additional language packs as needed:

```bash
sudo apt-get install tesseract-ocr-tha   # Thai
sudo apt-get install tesseract-ocr-eng   # English (usually installed by default)
```

List all installed languages:

```bash
tesseract --list-langs
```

## References

- [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)
- [Tesseract Data Files](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files)
- [pytesseract PyPI](https://pypi.org/project/pytesseract/)
