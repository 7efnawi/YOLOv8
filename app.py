from flask import Flask, request, jsonify, send_from_directory
from ultralytics import YOLO
import cv2
import os
from pathlib import Path
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'result'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

model = YOLO('yolov8x.pt')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_next_exp_num(base_dir=RESULT_FOLDER):
    os.makedirs(base_dir, exist_ok=True)
    exp_dirs = [d for d in os.listdir(base_dir) if d.startswith('exp')]
    if not exp_dirs:
        return 1
    exp_nums = [int(d[3:]) for d in exp_dirs if d[3:].isdigit()]
    return max(exp_nums) + 1 if exp_nums else 1

@app.route('/detect', methods=['POST'])
def detect_api():
    print("request.files content:", request.files)  # Debug
    if 'file' not in request.files:
        return jsonify({'error': 'No image received. request.files content: ' + str(list(request.files.keys()))}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Filename is empty. Please provide a valid image file.'}), 400
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        results = model(file_path)
        if len(results) > 0:
            img = results[0].plot()
            exp_num = get_next_exp_num()
            save_dir = Path(f'{RESULT_FOLDER}/exp{exp_num}')
            os.makedirs(save_dir, exist_ok=True)
            result_img_path = save_dir / 'detection.jpg'
            cv2.imwrite(str(result_img_path), img)
            detected = []
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    cls_name = r.names[cls]
                    conf = float(box.conf[0])
                    detected.append({'name': cls_name, 'conf': conf})
            return jsonify({
                'image_url': f'/result/exp{exp_num}/detection.jpg',
                'detected': detected
            })
        else:
            return jsonify({'error': 'No objects detected in the image.'}), 200
    else:
        return jsonify({'error': 'Unsupported file format. Please upload a PNG, JPG, or JPEG image.'}), 400

@app.route('/result/<exp>/<filename>')
def result_file(exp, filename):
    return send_from_directory(os.path.join(RESULT_FOLDER, exp), filename)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Endpoint not found. Please use POST /detect with an image file in form-data under the key "file".'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed. Please use POST method for /detect endpoint.'}), 405

if __name__ == '__main__':
    app.run(debug=True)