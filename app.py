from flask import Flask, request, render_template, send_from_directory
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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file selected')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No file selected')
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            # Run YOLO detection
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
                return render_template('result.html', image_url=f'/result/exp{exp_num}/detection.jpg', detected=detected)
            else:
                return render_template('index.html', error='No objects detected')
        else:
            return render_template('index.html', error='Unsupported file format')
    return render_template('index.html')

@app.route('/result/<exp>/<filename>')
def result_file(exp, filename):
    return send_from_directory(os.path.join(RESULT_FOLDER, exp), filename)

if __name__ == '__main__':
    app.run(debug=True)