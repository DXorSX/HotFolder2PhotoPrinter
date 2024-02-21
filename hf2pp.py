import os
import time
import shutil
from PIL import Image
import cups
import tempfile

# Directory to monitor
directory = "/path/to/directory"
temp_directory = tempfile.mkdtemp()  # Create a temporary directory

def watch_directory(directory):
    conn = cups.Connection()
    printer_name = "your_printer_name"  # Set your CUPS printer name here

    while True:
        for filename in os.listdir(directory):
            if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
                file_path = os.path.join(directory, filename)
                try:
                    # Move the file to the temporary directory
                    shutil.move(file_path, temp_directory)
                    temp_file_path = os.path.join(temp_directory, filename)

                    # Open the file using Pillow (PIL)
                    image = Image.open(temp_file_path)
                    # Change the format to 4:6
                    new_format = (4, 6)
                    image.thumbnail(new_format, Image.ANTIALIAS)
                    # Save the modified image
                    image.save(temp_file_path)

                    # Print the file
                    job_id = conn.printFile(printer_name, temp_file_path, "My Print Job", {})
                    print(f"File {filename} printed (Job ID: {job_id})")

                    # Delete the temporary file
                    os.remove(temp_file_path)
                    print(f"Temporary file {filename} deleted.")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        time.sleep(5)  # Wait for 5 seconds before checking the directory again

if __name__ == "__main__":
    watch_directory(directory)
