import xml.etree.ElementTree as ET
import os
import pandas as pd
import cv2
import shutil
from sklearn.model_selection import train_test_split
import yaml
from ultralytics import YOLO
import time
import numpy as np
from tqdm import tqdm
from fast_alpr import ALPR

IMAGE_DIR = 'archive/photos'
ANNOT_PATH = 'archive/annotations.xml'

def process_dataset(dataframe, split_name):
    for _, row in dataframe.iterrows():
        dw = 1.0 / row['width']
        dh = 1.0 / row['height']
        w = row['xbr'] - row['xtl']
        h = row['ybr'] - row['ytl']
        x_center = row['xtl'] + (w / 2.0)
        y_center = row['ytl'] + (h / 2.0)
        x_center *= dw
        y_center *= dh
        w *= dw
        h *= dh

        yolo_line = f"0 {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n"

        base_filename = os.path.splitext(row['image_name'])[0]

        label_path = os.path.join(LABELS_DIR, split_name, base_filename + '.txt')
        with open(label_path, 'w') as f:
            f.write(yolo_line)

        src_img_path = row['image_path']
        dst_img_path = os.path.join(IMAGES_DIR, split_name, row['image_name'])
        shutil.copy(src_img_path, dst_img_path)

def calculate_final_grade(accuracy_percent, processing_time_sec):
    if accuracy_percent < 60:
        return 2.0, "Accuracy too low (<60%)"
    if processing_time_sec > 60:
        return 2.0, "Time too high (>60s)"

    accuracy_norm = (accuracy_percent - 60) / 40
    time_norm = (60 - processing_time_sec) / 50

    accuracy_norm = max(0, min(1, accuracy_norm))
    time_norm = max(0, min(1, time_norm))

    score = 0.7 * accuracy_norm + 0.3 * time_norm

    grade = 2.0 + 3.0 * score

    final_grade = round(grade * 2) / 2
    return final_grade, "OK"

def clean_plate_text(text):
    if not text: return ""
    return "".join(c for c in text if c.isalnum()).upper()

parsed_data = []
print(f"Parsing...")

try:
    tree = ET.parse(ANNOT_PATH)
    root = tree.getroot()

    for image_elem in root.findall('image'):
        image_name = image_elem.get('name')
        image_path = os.path.join(IMAGE_DIR, image_name)
        box_elem = image_elem.find('box')

        if box_elem is not None:
            plate_number = "N_D"
            attr_elem = box_elem.find("attribute[@name='plate number']")

            if attr_elem is not None:
                value_from_text = attr_elem.text
                value_from_attr = attr_elem.get('value')

                if value_from_text is not None and value_from_text.strip() and value_from_text.strip().lower() != 'none':
                    plate_number = value_from_text.strip()
                elif value_from_attr is not None and value_from_attr.strip() and value_from_attr.strip().lower() != 'none':
                    plate_number = value_from_attr.strip()

                if plate_number.lower() == 'none':
                    plate_number = "N_D"

            image_width = int(image_elem.get('width'))
            image_height = int(image_elem.get('height'))
            label = box_elem.get('label')
            xtl = float(box_elem.get('xtl'))
            ytl = float(box_elem.get('ytl'))
            xbr = float(box_elem.get('xbr'))
            ybr = float(box_elem.get('ybr'))

            parsed_data.append({
                'image_name': image_name, 'image_path': image_path,
                'width': image_width, 'height': image_height,
                'label': label, 'xtl': xtl, 'ytl': ytl,
                'xbr': xbr, 'ybr': ybr, 'plate_number': plate_number
            })

    print(f"Parsing done. Found {len(parsed_data)} images...")

    df = pd.DataFrame(parsed_data)

except Exception as e:
    print(f"Parsing failed: {e}")

LABELS_DIR ='yolo_ds/labels'
IMAGES_DIR ='yolo_ds/images'

for split in ['train', 'test']:
    os.makedirs(os.path.join(LABELS_DIR, split), exist_ok=True)
    os.makedirs(os.path.join(IMAGES_DIR, split), exist_ok=True)

train_df, test_df = train_test_split(df, test_size=0.30, random_state=42)

print(f"{len(train_df)} training images and {len(test_df)} test images")

test_df.to_csv('test_dataset_ground_truth.csv', index=False)

process_dataset(train_df, 'train')
process_dataset(test_df, 'test')

yaml_content = {
    'path': os.path.abspath('yolo_ds'),
    'train': 'images/train',
    'val': 'images/test',
    'test': 'images/test',
    'nc': 1,
    'names': ['license_plate']
}

if not os.path.exists('yolo_ds/data.yaml'):
    with open('yolo_ds/data.yaml', 'w') as f:
        yaml.dump(yaml_content, f, default_flow_style=False)

    model = YOLO('yolov8n.pt')

    print("Training...")
    results = model.train(
        data='yolo_ds/data.yaml',
        epochs=50,
        imgsz=640,
        batch=16,
        # device='gpu',
        device='cpu',
        patience=10,
        name='tab_v8n'
    )

    print("Training done!")

model = YOLO('runs/detect/tab_v8n/weights/best.pt')

metrics = model.val(split='test')

alpr = ALPR(
    detector_model='yolo-v9-t-384-license-plate-end2end',
    ocr_model='global-plates-mobile-vit-v2-model'
)

test_samples = df.sample(100, random_state=42) if len(df) >= 100 else df

alpr_correct_count = 0
alpr_results_log = []

print(f"\nTesting on {len(test_samples)} photos ")
alpr_start_time = time.time()

for index, row in tqdm(test_samples.iterrows(), total=len(test_samples)):
    image_path = row['image_path']
    true_plate = clean_plate_text(row['plate_number'])

    img = cv2.imread(image_path)
    if img is None: continue

    detected_text = ""

    results = model.predict(img, verbose=False, conf=0.25)

    if len(results) > 0 and len(results[0].boxes) > 0:
        box = results[0].boxes[0]
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        h, w = img.shape[:2]
        pad = 10
        x1, y1 = max(0, x1-pad), max(0, y1-pad)
        x2, y2 = min(w, x2+pad), min(h, y2+pad)

        plate_crop = img[y1:y2, x1:x2]

        try:
            alpr_result = alpr.predict(plate_crop)

            if len(alpr_result) > 0:
                best_plate = alpr_result[0]
                detected_text = best_plate.ocr.text
            else:
                detected_text = ""

        except Exception as e:
            detected_text = ""

    final_text = clean_plate_text(detected_text)

    if true_plate != "N_D":
        if final_text == true_plate:
            alpr_correct_count += 1
        else:
            alpr_results_log.append({'true': true_plate, 'pred': final_text})

alpr_end_time = time.time()
processing_time= alpr_end_time - alpr_start_time
accuracy = (alpr_correct_count / len(test_samples)) * 100
print(f"Accuracy OCR using fastALPR: {accuracy:.2f}%")
print(f"Processing time: {processing_time:.2f}s")
print(calculate_final_grade(accuracy_percent=accuracy, processing_time_sec=processing_time))