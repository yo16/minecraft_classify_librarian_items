import pytest
import cv2

from src.readEnchantPrice import read_enchant_price

@pytest.mark.parametrize("img_path, line_number, expected", [
    # 通常
    ("./sample-data/20240823_121543.png", 1, 8),
    ("./sample-data/20240823_121548.png", 1, 18),
    ("./sample-data/20240823_121613.png", 1, 39),
    ("./sample-data/20240823_121734.png", 1, 9),
    ("./sample-data/20240823_121744.png", 1, 31),
    ("./sample-data/20240823_121750.png", 1, 31),
    ("./sample-data/20240823_121755.png", 2, 32),
    ("./sample-data/20240823_121800.png", 2, 11),
    ("./sample-data/20240823_121805.png", 2, 41),
    ("./sample-data/20240823_121810.png", 2, 20),
    ("./sample-data/20240823_121815.png", 2, 20),

    # 訂正
    ("./sample-data/20240823_185546.png", 1, 18),
    ("./sample-data/20240823_185551.png", 1, 18),
    ("./sample-data/20240823_185556.png", 1, 18),
    ("./sample-data/20240823_185601.png", 1, 18),
    ("./sample-data/20240823_185616.png", 2, 11),
    ("./sample-data/20240823_185621.png", 2, 11),
    ("./sample-data/20240823_185639.png", 1, 46),
    ("./sample-data/20240823_185644.png", 1, 46),
    ("./sample-data/20240823_185649.png", 1, 46),
    ("./sample-data/20240823_185709.png", 1, 46),
    ("./sample-data/20240823_185720.png", 2, 27),
    ("./sample-data/20240823_185725.png", 1, 33),
])
def test_classify_items(img_path, line_number, expected):
    img = cv2.imread(img_path)
    assert read_enchant_price(img, line_number) == expected

