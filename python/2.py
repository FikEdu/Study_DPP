import os
import xml.etree.ElementTree as ET
import random
import shutil
from ultralytics import YOLO


def calculate_final_grade(accuracy_percent: float, processing_time_sec: float) -> float:
    """
    Calculates the final grade based on license plate OCR accuracy and pro
    cessing time.
    Parameters:
    - accuracy_percent: OCR accuracy as a percentage (0–100)
    - processing_time_sec: total time to process 100 images in seconds
    Returns:
    - Grade on a scale from 2.0 to 5.0 (rounded to the nearest 0.5)
    """
    # Check minimum requirements
    if accuracy_percent < 60 or processing_time_sec > 60:
        return 2.0
    # Normalize accuracy: 60% → 0.0, 100% → 1.0
    accuracy_norm = (accuracy_percent - 60) / 40
    # Normalize time: 60s → 0.0, 10s → 1.0
    time_norm = (60 - processing_time_sec) / 50
    # Compute weighted score
    score = 0.7 * accuracy_norm + 0.3 * time_norm


    grade = 2.0 + 3.0 * score
    # Round to the nearest 0.5
    return round(grade * 2) / 2

if __name__ == "__main__":
    tree = ET.parse('archive/annotations.xml')
    root = tree.getroot()

    plate_metadata = {}

    for img in root.findall('image'):
        img_name = img.get('name')
        img_w = float(img.get('width'))
        img_h = float(img.get('height'))
        txt_name = os.path.splitext(img_name)[0] + ".txt"

        with open(os.path.join('data.yaml', txt_name), 'w') as f:
            for box in img.findall('box'):

                xtl, ytl = float(box.get('xtl')), float(box.get('ytl'))
                xbr, ybr = float(box.get('xbr')), float(box.get('ybr'))

                x_center = ((xtl + xbr) / 2) / img_w
                y_center = ((ytl + ybr) / 2) / img_h
                w = (xbr - xtl) / img_w
                h = (ybr - ytl) / img_h

                f.write(f"0 {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")

                attr = box.find("attribute[@name='plate number']")
                if attr is not None:
                    plate_metadata[img_name] = attr.text

        for split in ['train', 'test']:
            os.makedirs(f'labeled_files/images/{split}', exist_ok=True)
            os.makedirs(f'labeled_files/labels/{split}', exist_ok=True)

        # Get all images
        images = [f for f in os.listdir(image_src) if f.endswith(('.jpg', '.png'))]
        random.shuffle(images)

        # Split 60 for training, rest for test
        train_imgs = images[:60]
        test_imgs = images[60:]


        def move_files(file_list, split):
            for img in file_list:
                lbl = os.path.splitext(img)[0] + '.txt'
                # Copy Image
                shutil.copy(os.path.join(image_src, img), f'{dataset_root}images/{split}/{img}')
                # Copy Label
                if os.path.exists(os.path.join(label_src, lbl)):
                    shutil.copy(os.path.join(label_src, lbl), f'{dataset_root}labels/{split}/{lbl}')


        move_files(train_imgs, 'train')
        move_files(test_imgs, 'test')


    # model = YOLO("yolo8n.pt")
    #
    # results = model.train(
    #     data="data.yaml",
    #     epochs=60,
    #     imgsz=640,
    #     device="cpu"
    # )

