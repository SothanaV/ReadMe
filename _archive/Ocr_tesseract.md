# Tesseract
## Install
    $ pip install pillow
    $ pip install pytesseract
    $ sudo apt-get install tesseract-ocr

## Check install tesseract
    $ tesseract -v

# Use
## Testing
    ###Text
    $ tesseract tesseract_inputs/example_01.png stdout 

    ###Digit
    $ tesseract tesseract_inputs/example_03.png stdout digits

https://github.com/tesseract-ocr/tesseract/wiki/Data-Files