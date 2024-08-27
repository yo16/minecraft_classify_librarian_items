import pytest
import cv2
import json
import os

from src.judgeTitle import judge_title


# テストデータの整理
# data_map.jsonのdataに登録されている画像をテストする
json_path = "./sample-data/data_map.json"
with open(json_path, mode="r", encoding="utf-8") as f:
    data_map = json.load(f)
test_params = []
for data_info in data_map["data"]:
    if len(data_info["file_name"]) == 0:
        continue

    base_name, ext = os.path.splitext(data_info["file_name"])
    test_params.append((
        f"./sample-data/{base_name}_text{ext}",
        data_info["enchant"]
    ))


@pytest.mark.parametrize("img_path, expected", test_params)
def test_judge_title(img_path, expected):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img_line = img.flatten()

    enchant_title = judge_title(img_line)

    assert enchant_title == expected

