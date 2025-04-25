# 🌟 Aura Sense: Advanced Object Detection with YOLOv8

![YOLOv8 Demo](https://ultralytics.com/images/yolov8-sahi-demo.png)

## 🔍 Project Overview

Aura Sense is an innovative graduation project that implements state-of-the-art object detection using YOLOv8. The system provides real-time, accurate detection of objects in images through an intuitive web interface and API.

## ⚡ YOLOv8 Model

YOLOv8 represents the cutting edge in object detection technology, offering remarkable improvements over previous generations:

### 🏆 Performance Metrics

| Model   | Size   | mAP<sup>val<br>50-95 | Speed<br>(ms) | Parameters<br>(M) |
| ------- | ------ | -------------------- | ------------- | ----------------- |
| YOLOv8x | 131 MB | 53.9                 | 23.4          | 68.2              |

### 🎯 Key Features

- **State-of-the-art accuracy**: Achieves over 53.9% mAP on COCO dataset
- **Real-time processing**: Detects objects in milliseconds
- **Multi-object detection**: Identifies and localizes multiple object classes simultaneously
- **High confidence scoring**: Provides probability scores for all detections
- **Pre-trained on diverse datasets**: Recognizes 80+ common object categories

## 🚀 Implementation

Our implementation offers:

- **Web-based UI**: Simple drag-and-drop interface for image uploads
- **Visual results**: Processed images with bounding boxes and labels
- **Confidence metrics**: Detailed probability scores for all detections
- **Result storage**: Automatic saving of detection results for reference

## 🔧 API Documentation

The API provides a simple interface for object detection services:

### Endpoints

#### `POST /detect`

Upload an image for object detection.

**Request:**

- Content-Type: `multipart/form-data`
- Body: form data with `file` field containing the image

**Response:**

```json
{
  "detections": [
    {
      "class": "person",
      "confidence": 0.96,
      "bbox": [x1, y1, x2, y2]
    },
    {
      "class": "car",
      "confidence": 0.87,
      "bbox": [x1, y1, x2, y2]
    }
  ],
  "image_url": "/result/exp1/detection.jpg",
  "processing_time": "0.245s"
}
```

## 💻 Installation and Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/username/aura-sense.git
   cd aura-sense
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open your browser at `http://localhost:5000`

## 📋 Requirements

- Python 3.8+
- PyTorch
- OpenCV
- Flask
- Ultralytics YOLOv8

## 📝 Note

This repository does not include:

- `templates/` folder containing UI templates
- `uploads/` folder for temporary image storage
- Large model files (\*.pt)

These files need to be downloaded or created separately.

## 👥 Contributors

Aura Sense is a graduation project developed by [Team Members Names].

---

## 📞 Contact

For inquiries or support, please contact [contact email].
