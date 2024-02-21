# HotFolder2PhotoPrinter
Simple script that monitors a directory. If photos are added they are prepard to be printed on a DNP DS-RX1HS Photoprinter.

Make sure to adjust the path to the directory `(directory)` and the name of your CUPS printer `(printer_name)` according to your environment. 
This script uses the Python library Pillow (PIL) for image manipulation, pycups for printing, and tempfile for the temporary directory.
Install Pillow with `pip install pillow`, pycups with `pip install pycups`, and tempfile is included in the standard library.
