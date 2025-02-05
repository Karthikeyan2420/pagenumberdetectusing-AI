from ultralytics import YOLO

# Load pretrained YOLOv8 model
model = YOLO("yolov8n.pt")
def main():
    # Train the model
    results = model.train(
        data="yolov8n.yaml",
        epochs=100,
        imgsz=640,
        batch=8,
        name="page_number_detector"
    )

if __name__=="__main__":
    main()