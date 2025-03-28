import os

# Define folders
txt_folder = r"C:\Users\kkpr2\OneDrive\Documents\karthikeyandev\yolo_page_number\yolo_page_number\images\label"        # Folder containing .txt files
images_folder = r"C:\Users\kkpr2\OneDrive\Documents\karthikeyandev\yolo_page_number\yolo_page_number\images\sampleimage"  # Folder containing .png files

# Check if folders exist
if not os.path.exists(txt_folder):
    print(f"Error: Folder '{txt_folder}' not found.")
    exit(1)

if not os.path.exists(images_folder):
    print(f"Error: Folder '{images_folder}' not found.")
    exit(1)

# Get list of expected PNG names (based on TXT filenames)
expected_names = {
    os.path.splitext(txt_file)[0]  # Remove .txt extension
    for txt_file in os.listdir(txt_folder)
    if txt_file.endswith(".txt")
}

# Delete PNGs not in the expected names
deleted_count = 0
for png_file in os.listdir(images_folder):
    if png_file.endswith(".png"):
        png_name = os.path.splitext(png_file)[0]  # Remove .png extension
        if png_name not in expected_names:
            png_path = os.path.join(images_folder, png_file)
            os.remove(png_path)
            print(f"Deleted: {png_path}")
            deleted_count += 1

print(f"\nDone! Deleted {deleted_count} unmatched .png files.")
