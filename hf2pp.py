import os
import time
import shutil
from PIL import Image
import cups
import tempfile

# Directory to monitor
directory = "/path/to/Folder"
temp_directory = tempfile.mkdtemp()  # Create a temporary directory

# Set your CUPS printer name here
printer_name = "Your-Printer-Name"  

def watch_directory(directory):
    conn = cups.Connection()
    
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

                    # Check if width (x) is greater than height (y)
                    x, y = image.size
                    if x < y:
                        # Rotate the image to landscape (90 degrees clockwise)
                        rotated_image = image.rotate(-90, expand=True)
                        print(f"Image rotated!")
                    else:
                        rotated_image = image  # No rotation needed
                        print(f"Image NOT rotated!")

                    # Resize while maintaining aspect ratio
                    new_width, new_height = 1844, 1240
                    rotated_image.thumbnail((new_width, new_height), Image.LANCZOS)

                    # Create a new white canvas
                    canvas = Image.new("RGB", (new_width, new_height), "white")
                    offset = ((new_width - rotated_image.width) // 2, (new_height - rotated_image.height) // 2)
                    canvas.paste(rotated_image, offset)

                    # Save the modified image
                    canvas.save(temp_file_path)

                    # Print the file
                    job_id = conn.printFile(printer_name, temp_file_path, "My Print Job", {})
                    print(f"File {filename} printed (Job ID: {job_id})")

                    # Delete the temporary file
                    os.remove(temp_file_path)
                    print(f"Temporary file {temp_file_path} deleted.")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        time.sleep(5)  # Wait for 5 seconds before checking the directory again

if __name__ == "__main__":
    watch_directory(directory)
