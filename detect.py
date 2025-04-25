from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
from pathlib import Path

# Function to get the next experiment number
def get_next_exp_num(base_dir='result'):
    # Create base directory if it doesn't exist
    os.makedirs(base_dir, exist_ok=True)
    
    # Find existing exp folders
    exp_dirs = [d for d in os.listdir(base_dir) if d.startswith('exp')]
    
    # Get the highest exp number
    if not exp_dirs:
        return 1
    
    exp_nums = [int(d[3:]) for d in exp_dirs if d[3:].isdigit()]
    return max(exp_nums) + 1 if exp_nums else 1

# Load the pre-trained model
model = YOLO('yolov8x.pt') 

# Ask user for image path
print("Enter the path to your image:")
image_path = input()

# Remove quotes if present
image_path = image_path.strip('"\'')

# Run inference on an image
try:
    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}")
        exit(1)
        
    results = model(image_path)

    # Display results - results is a list, so we use the first element
    if len(results) > 0:
        # Get the image with detection boxes
        img = results[0].plot()
        
        # Convert from BGR to RGB (OpenCV uses BGR, matplotlib uses RGB)
        img_rgb = img[..., ::-1]
        
        # Create save directory
        exp_num = get_next_exp_num()
        save_dir = Path(f'result/exp{exp_num}')
        os.makedirs(save_dir, exist_ok=True)
        
        # Save the image with detections
        cv2.imwrite(str(save_dir / 'detection.jpg'), img)
        print(f"Image saved to {save_dir / 'detection.jpg'}")
        
        # Display image with detection boxes using matplotlib
        plt.figure(figsize=(12, 8))
        plt.imshow(img_rgb)
        plt.axis('off')
        plt.title(f"Object Detection Results - Experiment {exp_num}")
        
        # Print information about detected objects
        print(f"Experiment {exp_num} results:")
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                cls_name = r.names[cls]
                conf = float(box.conf[0])
                print(f"Detected: {cls_name} with confidence {conf:.2f}")
        
        # Show the plot
        plt.show()
except Exception as e:
    print(f"Error occurred: {e}")
