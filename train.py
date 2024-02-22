from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch


# Use the model
model.train(data="custom_data.yaml", epochs=150, imgsz=640, batch_size=16, workers=8)  