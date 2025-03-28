import os
import shutil

# Define source and destination directories
source_folder = "sampleimage"
destination_folder = "bookwise"

# Ensure destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Iterate through all files in the source folder
for filename in os.listdir(source_folder):
    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
        book_name = filename.split("_")[0]  # Extract book name
        book_folder = os.path.join(destination_folder, book_name)  # Create bookwise folder path
        
        # Ensure the book-specific folder exists
        os.makedirs(book_folder, exist_ok=True)
        
        # Move the file to the correct folder
        shutil.move(os.path.join(source_folder, filename), os.path.join(book_folder, filename))

print("Images have been organized successfully!")
