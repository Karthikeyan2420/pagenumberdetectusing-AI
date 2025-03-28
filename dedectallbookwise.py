import cv2
from ultralytics import YOLO
import easyocr
import re
import os

class PageNumberDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.ocr = easyocr.Reader(['en'])
        self.page_number_pattern = r'\b\d+\b'

    def preprocess_image(self, image_path):
        img = cv2.imread(image_path)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def detect_page_number(self, image_path, cropped_folder):
        try:
            img = self.preprocess_image(image_path)
            results = self.model.predict(img, conf=0.5)

            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()

                if len(boxes) == 0:
                    return "No page number detected"

                largest_box = max(boxes, key=lambda box: (box[2]-box[0]) * (box[3]-box[1]))
                x1, y1, x2, y2 = map(int, largest_box)

                cropped = img[y1:y2, x1:x2]
                cropped_image_name = os.path.basename(image_path)
                cropped_image_path = os.path.join(cropped_folder, cropped_image_name)
                cv2.imwrite(cropped_image_path, cropped)

                ocr_result = self.ocr.readtext(cropped)

                for text_entry in ocr_result:
                    text = text_entry[1]
                    if re.search(self.page_number_pattern, text):
                        return text

            return "Page number found but not recognized"

        except Exception as e:
            return f"Error: {str(e)}"

    def process_folder(self, folder_path, cropped_folder):
        os.makedirs(cropped_folder, exist_ok=True)
        results = {}
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                image_path = os.path.join(folder_path, filename)
                page_number = self.detect_page_number(image_path, cropped_folder)
                results[filename] = page_number
        return results

# Main execution
bookwise_folder = "bookwise"
model_path = "best.pt"
result_file = "accuracy_results01.txt"

detector = PageNumberDetector(model_path)

# To store overall stats
total_all_books = 0
successful_all_books = 0

with open(result_file, "w") as file:
    file.write("Book-wise Detection Accuracy:\n")
    file.write("="*40 + "\n")

    # Iterate over book subfolders
    for book_folder in os.listdir(bookwise_folder):
        book_path = os.path.join(bookwise_folder, book_folder)

        if os.path.isdir(book_path):  # Ensure it's a folder
            cropped_folder = os.path.join("cropped", book_folder)  # Fix missing closing quotation mark
            result = detector.process_folder(book_path, cropped_folder)  # Fix indentation and missing part

            # Count total images and successful detections
            total_images = len(result)
            successful_detections = sum(1 for page_number in result.values() if page_number.isdigit())  # Fix incomplete variable name

            # Calculate percentage
            detection_percentage = (successful_detections / total_images) * 100 if total_images > 0 else 0

            # Update overall stats
            total_all_books += total_images
            successful_all_books += successful_detections

            # Write book-wise accuracy to file
            file.write(f"\nBook: {book_folder}\n")
            file.write(f"Total Images: {total_images}\n")
            file.write(f"Successfully Detected Page Numbers: {successful_detections}\n")
            file.write(f"Detection Accuracy: {detection_percentage:.2f}%\n")
            file.write("-" * 40 + "\n")

            # Print book-wise accuracy
            print(f"\nBook: {book_folder}")
            print(f"Total Images: {total_images}")
            print(f"Successfully Detected Page Numbers: {successful_detections}")
            print(f"Detection Accuracy: {detection_percentage:.2f}%")

    # Calculate overall detection accuracy
    overall_accuracy = (successful_all_books / total_all_books) * 100 if total_all_books > 0 else 0

    # Write overall accuracy to file
    file.write("\nOverall Detection Accuracy:\n")
    file.write("=" * 40 + "\n")
    file.write(f"Total Images Across All Books: {total_all_books}\n")
    file.write(f"Total Successfully Detected Page Numbers: {successful_all_books}\n")
    file.write(f"Overall Detection Accuracy: {overall_accuracy:.2f}%\n")

# Print overall accuracy
print("\nOverall Detection Accuracy:")
print("=" * 40)
print(f"Total Images Across All Books: {total_all_books}")
print(f"Total Successfully Detected Page Numbers: {successful_all_books}")
print(f"Overall Detection Accuracy: {overall_accuracy:.2f}%")

