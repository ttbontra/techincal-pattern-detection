import os
from ultralytics import YOLO
import cv2

# Path to the image
image_path = '35.PNG'

# Load the image
frame = cv2.imread(image_path)
if frame is None:
    raise IOError("Error opening image file. Check the file path and format.")

H, W, _ = frame.shape

# Load the model
model_path = os.path.join('models', 'best.pt')
model = YOLO(model_path)

# Very low threshold for detection confidences
#threshold = 0.0000000000001 

# Perform object detection
results = model(frame)[0]

# Define a list of colors for bounding boxes
color_map = {
    'consolidation': (0, 255, 0),   
    'bullflag': (255, 105, 180),
    'mini bullflag': (0, 0, 255)     
}

# Draw bounding boxes and labels
for result in results.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = result
    class_name = results.names[int(class_id)].lower()  # Get class name in lowercase

    # Get the color for the class, default to white if class not found in color_map
    color = color_map.get(class_name, (255, 255, 255))

    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)  # Thinner outline
    cv2.putText(frame, class_name.upper(), (int(x1), int(y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)  # Smaller text

# Save the processed image
output_path = 'test_processed.png'
cv2.imwrite(output_path, frame)
