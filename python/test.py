import os

from fast_alpr import ALPR

alpr = ALPR(
    detector_model="yolo-v9-t-384-license-plate-end2end",
    ocr_model="cct-xs-v1-global-model",
)

for file in os.listdir("archive/photos"):
    # The "assets/test_image.png" can be found in repo root dir
    alpr_results = alpr.predict(f'archive/photos/{file}')
    print(alpr_results)